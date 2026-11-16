"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    run_id = make_run_id("single", claim_id, seed)
    trace = Trace(run_id)

    def done(status: str, proposal: int, reason: str | None) -> RunResult:
        trace.add("decision", {"status": status, "proposal_amount": int(proposal), "reason": reason})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    # 1. Read the claim through the view (ticket is user data, never traced in full beyond the view).
    budget.add_tool(tool_cost())
    claim = get_claim_view(conn, claim_id)
    if not claim.get("found"):
        return done("failed", 0, "unknown_claim")
    trace.add("claim", {"claim_id": claim_id, "has_order_id": bool(claim.get("order_id"))})
    if not claim.get("order_id"):
        complete(budget, seed=seed, purpose="draft", prompt="needs_info")
        return done("needs_info", 0, "missing_order_id")

    principal_id = claim["principal_id"]
    order_id = claim["order_id"]
    state: dict[str, object] = {"order": {}, "policy_count": 0}

    def decide(seen: dict) -> dict:
        # Step 1: resolve the order row. This is the source of truth, never the ticket.
        if "last_tool" not in seen:
            return {
                "tool": "lookup_order",
                "args": {"order_id": order_id, "principal_id": principal_id},
            }
        last_tool = seen.get("last_tool")
        last_result = seen.get("last_result") or {}
        if last_tool == "lookup_order":
            if not last_result.get("visible"):
                return {"final": {"status": "escalated", "reason": last_result.get("reason")}}
            state["order"] = dict((last_result.get("order") or {}))
            return {"tool": "lookup_policy", "args": {}}
        if last_tool == "lookup_policy":
            policies = (last_result.get("policies") or [])
            state["policy_count"] = len(policies)
            return {"tool": "lookup_refund_history", "args": {"order_id": order_id, "principal_id": principal_id}}
        if last_tool == "lookup_refund_history":
            order = state.get("order") or {}
            return {"tool": "compute_compensation", "args": {"order": dict(order)}}
        # Quote is ready; stop the loop.
        return {"final": {"status": "quoted"}}

    outcome = run_react(
        conn,
        budget,
        observation={"claim": claim},
        decide=decide,
        max_steps=8,
        worker=True,
    )
    trace.add("react", safe_dump({"stopped": outcome.get("stopped"), "final": outcome.get("final")}))
    if outcome.get("stopped") == "step_cap":
        complete(budget, seed=seed, purpose="draft", prompt="step_cap")
        return done("failed", 0, "step_cap")

    final = outcome.get("final") or {}
    if final.get("status") == "escalated":
        complete(budget, seed=seed, purpose="draft", prompt="escalated")
        return done("escalated", 0, final.get("reason"))

    obs = outcome.get("observation") or {}
    quote = obs.get("last_result") or {}
    if obs.get("last_tool") != "compute_compensation" or "amount_vnd" not in quote:
        return done("failed", 0, "missing_quote")

    order_view = {"order": state.get("order"), "policy_count": state.get("policy_count")}
    trace.add("investigator", safe_dump({"lookup_order": state.get("order"), "policy_count": state.get("policy_count")}))
    trace.add("quote", safe_dump(quote))
    _ = order_view
    complete(budget, seed=seed, purpose="draft", prompt=f"proposal={quote.get('amount_vnd', 0)}")

    proposal = int(quote.get("amount_vnd", 0))
    if proposal <= 0:
        return done("denied", 0, quote.get("reason"))

    try:
        refund = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    trace.add("refund_outcome", safe_dump(refund))
    if refund["ok"]:
        return done("resolved", proposal, None)
    return done("failed" if refund.get("conflict") else "denied", proposal, refund.get("reason"))
