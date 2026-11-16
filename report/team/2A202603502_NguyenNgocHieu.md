# Báo cáo cá nhân — 2A202603502_NguyenNgocHieu

## 1. Thông tin thành viên

- Họ tên: Nguyễn Ngọc Hiếu
- MSSV: 2A202603502
- Email: hieunn3003@gmail.com
- GitHub: NguyenNgocHieu03502
- Vai trò: Orchestrator + handoff (Shape C)

## 2. Phần việc phụ trách

- Shape C — orchestrator và investigator chỉ đọc: `src/lab8/shapes/orchestrator.py`.
- Ranh giới handoff giữa orchestrator và investigator (allowlist, tool chỉ đọc) và nội dung trace của Shape C.

## 3. Đóng góp cụ thể

**Commit chính:** `3565f22` — `feat(shape-c): implement orchestrator with read-only investigators`.

**Luồng xử lý đã cài:**

| Bước | Ai làm | Kết quả |
| --- | --- | --- |
| Đọc claim qua `get_claim_view` | Orchestrator | Không tìm thấy → `failed` (`unknown_claim`); thiếu `order_id` → `needs_info` |
| Dựng handoff bằng `make_handoff` | Orchestrator | `facts={}`, `allowed_tools` chỉ gồm tool đọc |
| `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation` | Investigator (`run_readonly_investigators`) | Đơn không visible → `escalated` |
| Lấy quote từ `compute_compensation` | Orchestrator | Quote = 0 → `denied`, không gọi `issue_refund` |
| `durability.issue_refund(conn, claim_id, quote, crash_at=crash_at)` | Orchestrator (duy nhất) | `resolved` / `denied` (host ghi `policy_denied`) / `failed` khi conflict |

**Quyết định kỹ thuật:**

1. **Ranh giới code / model.** Số tiền do `compute_compensation` tính từ order row. MockLLM chỉ được gọi một lần với `purpose="draft"` để soạn chữ, không ảnh hưởng số tiền hay trạng thái. Investigator không có tool ghi: `make_handoff` từ chối tool ngoài `READONLY_TOOLS`, và `dispatch(worker=True)` chặn `issue_refund`.
2. **`facts={}` trong handoff.** Investigator tự đọc dữ kiện từ DB. Không đưa số ngày trễ hay mã đơn lấy từ ticket vào handoff, để tránh lặp lại điểm yếu `REFERENCE_WEAKNESS` của swarm (tin số ngày trong ticket).
3. **Kiểm claim trước khi dựng handoff.** Nếu để investigator tự đọc claim không tồn tại, kết quả sẽ là `escalated` thay vì `failed` như contract yêu cầu.
4. **Truyền quote đầy đủ.** `lookup_refund_history` chỉ được đọc và ghi vào trace; orchestrator không tự trừ phần đã hoàn. Host trừ theo đơn, nên nếu shape trừ trước thì host trừ hai lần và T14 fail.
5. **Crash.** `crash_at` được truyền thẳng vào `issue_refund`. Khi gặp `InjectedCrash`, shape ghi trace rồi `raise` lại, không nuốt lỗi (T12).
6. **Mọi nhánh return đi qua `common.finish()`**, nên luôn có trace mới với `run_id` đúng, và `refund_effects` / `committed_audit_count` lấy từ ledger chứ không tự điền.

**Field cố ý không ghi vào trace:** nội dung `ticket`, claim row thô (`parent_secret`, `raw_headers`), order row thô (SĐT, địa chỉ, tên hàng, ghi chú nội bộ). Trace chỉ ghi: `claim_id` và cờ có/không có `order_id`, handoff đã sanitize, order view đã qua `ORDER_FIELDS`, lịch sử hoàn tiền (số lần, tổng tiền), số policy hiện hành, quote và quyết định cuối.

**Test:** test riêng cho Shape C do thành viên khác trong nhóm phụ trách; phần của tôi được kiểm bằng ma trận student và các lần chạy thử ghi ở mục 4.

## 4. Bằng chứng

- `git show 3565f22` — commit thuộc tác giả `NguyenNgocHieu03502`.
- `python -m pytest -q -m student -o addopts= -k orchestrator`: **62 passed** (T01–T10, T13, T14 × 5 seed, cộng T11 retry và T12 crash).
- `python -m pytest -q` (cổng host): xanh, không có dòng `failed`.
- `python -m lab8.check_submission`: `[ OK ] shape orchestrator: format đúng, 12/12 claim public pass ở seed 11`.
- Chạy thử crash rồi resume claim `C-012` (seed 11) ở cả 3 điểm `before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`: lần nào crash cũng xảy ra thật; sau resume là `resolved`, 1 dòng ledger, 1 audit `refund_committed`. Run id: `R-orchestrator-C-012-s11`.
- Quét 62 file trace `traces/R-orchestrator-*.json` với 55 chuỗi cấm lấy từ dữ liệu (secret, SĐT, địa chỉ, ghi chú, tên hàng, `CANARY_SECRET_`): **0 lần trùng**.

## 5. Công cụ AI đã dùng

- **Công cụ:** Claude Code (Anthropic).
- **Dùng vào việc:** đọc và phân tích đề bài, contract và code host (`runtime.py`, `handoff.py`, `durability.py`, `tools.py`); đề xuất cấu trúc cho `orchestrator.py`; viết script kiểm crash/resume và quét trace; hỗ trợ soạn báo cáo này.
- **Cách tự kiểm tra:**
  - Đối chiếu từng nhánh return với bảng output contract trong `docs/contracts.md` và luật trong `docs/business_rules.md`.
  - Chạy ma trận student cho orchestrator (62/62) và cổng host trên Python 3.12 (venv riêng, vì máy mặc định là Python 3.15, ngoài khoảng 3.11–3.13 của lab).
  - Tự chạy crash ở cả 3 điểm và đếm dòng ledger / audit trực tiếp trong SQLite.
  - Quét trace theo giá trị secret/PII thật trong dữ liệu thay vì chỉ tìm chuỗi `CANARY`.
  - Không dùng AI để tạo số liệu benchmark hay run id; mọi số trong báo cáo lấy từ lệnh chạy thật.

## 6. Tự đánh giá

- Hoàn thành Shape C: qua toàn bộ ma trận student, đúng contract `RunResult` và Trace contract v1, không lộ secret/PII trong trace.
- Không sửa file thước đo (`metrics.py`, `durability.py`, `policy.py`, `config/`, `data/`).
- Còn thiếu: test riêng cho Shape C do chính tôi viết (hiện do thành viên khác phụ trách).
