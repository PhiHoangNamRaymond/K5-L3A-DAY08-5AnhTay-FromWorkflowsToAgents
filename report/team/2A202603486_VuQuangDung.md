# Báo cáo cá nhân — 2A202603486_VuQuangDung

## 1. Thông tin thành viên

- Họ tên: Vũ Quang Dũng
- MSSV: 2A202603486
- Email: vuquangdung2309@gmail.com
- GitHub: https://github.com/qdung2003
- Vai trò: Kiểm thử Shape C (Orchestrator) — test C8 bắt buộc + verify ma trận student/cổng host

## 2. Phần việc phụ trách

- Viết test bắt buộc C8 cho Shape C: `src/tests/test_orchestrator_shape.py` (handoff từ chối tool ghi, trace không lộ secret, crash cả 3 điểm rồi resume vẫn 1 refund).
- Verify thực tế: chạy test mới, ma trận student orchestrator, cổng host; gỡ conflict merge `single.py`/`benchmark.json`; tái sinh `reports/benchmark.json` + `reports/crash.json`.

## 3. Đóng góp cụ thể

- Commit chính: `726d632` (`update` — thêm `src/tests/test_orchestrator_shape.py`, `src/tests/test_single_shape.py`; tái sinh `benchmark.json`/`crash.json`).
- Test đã thêm: `src/tests/test_orchestrator_shape.py` gồm 5 test:
  + `test_handoff_rejects_write_tool`: `make_handoff(allowed_tools=[..., "issue_refund"])` → `HandoffError`.
  + `test_orchestrator_trace_has_no_parent_secret`: chạy `run_claim("C-001")`, quét trace — không chứa `CANARY_SECRET_` / `parent_secret` / `raw_headers`.
  + `test_orchestrator_crash_then_resume_yields_single_refund[3 điểm]`: parametrize `before_effect`, `after_effect_before_checkpoint`, `after_checkpoint` — lần 1 expect `InjectedCrash`, lần 2 resume `resolved`, ledger 1 row, `amount == proposal_amount`, 1 audit `refund_committed`.
- Quyết định kỹ thuật: mỗi crash-point dùng store riêng (`_fresh_store`) để lần resume chạy đúng trên cùng DB với lần crash; dùng claim `C-001` (approval A-001 valid, quote 35000) làm chuẩn.

## 4. Bằng chứng

- `python -m pytest tests/test_orchestrator_shape.py -v` → **5 passed**.
- `python -m pytest -q -m student -o addopts= -k orchestrator` → **62 passed**.
- `python -m pytest -q` (cổng host) → **65 passed** (thời điểm verify), không regression.
- `python -m lab8.check_submission`: 3 shape `[ OK ]` (workflow/single/orchestrator 12/12 claim public seed 11), `benchmark.json` 4 shape × 14 claim × 5 seed, `crash.json` 20/20.
- Benchmark public: orchestrator pass 1.000 / pass^5 1.000 / variance 0 / cost 56.52 (`src/reports/benchmark.json`).

## 5. Công cụ AI đã dùng

- Công cụ: Claude (Claude Opus 5.5).
- Dùng vào việc gì: đọc `orchestrator.py`, `handoff.py`, `durability.py`, dữ liệu C-001/O-107 để thiết kế 5 test C8; review logic crash-resume trước khi chạy.
- Tự kiểm tra: chạy pytest thực tế (lần đầu kẹt quyền `pytest-of-LAPTOP` → dùng `--basetemp=.pytest-tmp`); mọi số liệu lấy từ output lệnh thật, không bịa.

## 6. Tự đánh giá

- Hoàn thành test C8 bắt buộc cho Shape C (điều kiện C8): test do tôi viết, pass 5/5, ma trận shape 62/62.
- Không sửa file đo lường (`metrics.py`, `durability.py`, `policy.py`, `config/`, `data/`).
