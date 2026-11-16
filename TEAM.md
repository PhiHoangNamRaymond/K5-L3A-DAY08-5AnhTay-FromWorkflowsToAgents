# Team

## Thông tin nhóm

- Tên nhóm: 5AnhTay
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-5AnhTay-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/PhiHoangNamRaymond/K5-L3A-DAY08-5AnhTay-FromWorkflowsToAgents.git, nhánh main, commit `c1d6059`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Hải Anh | 2A202603484 | haianh29112@gmail.com | haianh02034 | Workflow (Shape A) |
|   2 | Nguyễn Ngọc Hiếu | 2A202603502 | hieunn3003@gmail.com | robyvn | Orchestrator + handoff (Shape C) |
|   3 | Bùi Văn Lâm | 2A202603400 | 26ai.lambv@vinuni.edu.vn | buivanlam | Single (Shape B) |
|   4 | Vũ Quang Dũng | 2A202603486 | vuquangdung2309@gmail.com | https://github.com/qdung2003 | Kiểm thử Shape B và C (test C8) |
|   5 | Phí Hoàng Nam | 2A202603435 | phinamyb2004@gmail.com | PhiHoangNamRaymond | Tích hợp và kiểm thử an toàn |


Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Hải Anh | workflow | 54917fd | `src/tests/test_workflow_shape.py::test_workflow_idempotency_retry` |
| Nguyễn Ngọc Hiếu | Orchestrator và tích hợp Shape B | 3565f22, f9966e2, f5505ed | `src/tests/test_orchestrator_boundaries.py::test_trace_records_sanitized_handoff_only` |
| Bùi Văn Lâm | Single ReAct | da5a5f2 (nhánh buivanlam), tích hợp qua f9966e2 | Ma trận student kiểm tra Shape B. Chờ commit test do Lâm thêm hoặc sửa. |
| Vũ Quang Dũng | Kiểm thử Shape B và C | 726d632 | `src/tests/test_orchestrator_shape.py::test_orchestrator_crash_then_resume_yields_single_refund`, `src/tests/test_single_shape.py::test_single_crash_then_resume_yields_single_refund` |
| Phí Hoàng Nam | Tích hợp và kiểm thử an toàn | f76645f, c1d6059 | `src/tests/test_safety_integration.py::test_resume_after_checkpoint_keeps_one_refund`, `test_approval_for_another_claim_is_denied_at_shape_entry`, `test_ticket_secret_is_absent_from_result_trace_and_stdout` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603484_NguyenHaiAnh

### Phần việc phụ trách

- Shape A: Deterministic Workflow (`src/lab8/shapes/workflow.py`).
- Kiểm thử toàn diện và bảo mật dữ liệu cho Shape A (`src/tests/test_workflow_shape.py`).

### Đóng góp cụ thể

- Hiện thực toàn bộ hàm `run_claim` cho Shape A (`workflow.py`):
  + Đọc claim an toàn qua `get_claim_view` (bảo vệ `parent_secret` và `raw_headers`).
  + Xử lý trường hợp thiếu `order_id` (trả về trạng thái `needs_info`, không ghi ledger).
  + Kiểm tra quyền sở hữu đơn hàng với `lookup_order` (trả về `escalated` khi ngoài phạm vi, bảo mật thông tin PII: SĐT, địa chỉ, hàng hóa, ghi chú).
  + Tính toán bồi hoàn chuẩn xác bằng code thuần `compute_compensation`, độc lập với LLM và loại bỏ hoàn toàn số ngày trễ người dùng tự khai báo trong ticket.
  + Gửi quote đầy đủ qua cổng host `durability.issue_refund` để host tự xử lý trần bồi hoàn theo đơn.
  + Xử lý an toàn Idempotency (gọi lại cùng claim) và chuyển tiếp ngoại lệ `InjectedCrash` (ghi trace trước khi ném ngoại lệ để đảm bảo crash safety).
- Thêm bộ test chuyên biệt `src/tests/test_workflow_shape.py` gồm 6 bài test bao quát các trường hợp biên.

### Bằng chứng

- Commit: `54917fd` (`feat(workflow): implement Shape A deterministic workflow with safety guardrails`)
- Test suite: `src/tests/test_workflow_shape.py` (6/6 tests passed)
- Ma trận student: `pytest -q -m student -o addopts= -k workflow` (62/62 tests passed)
- Báo cáo chi tiết: `report/team/2A202603484_NguyenHaiAnh.md`
- Công cụ kiểm tra nộp bài: `python -m lab8.check_submission` ghi nhận `[ OK ] shape workflow: format đúng, 12/12 claim public pass ở seed 11`.

## 2A202603502_NguyenNgocHieu

### Phần việc phụ trách

- Shape C: orchestrator và investigator chỉ đọc (`src/lab8/shapes/orchestrator.py`), gồm dựng handoff theo allowlist.

### Đóng góp cụ thể

- Hiện thực `run_claim` cho Shape C:
  + Orchestrator đọc claim qua `get_claim_view`; chữ trong ticket không được ghi vào trace, không dùng để chọn đơn hay số ngày trễ.
  + Dựng handoff bằng `make_handoff` với `facts={}` và chỉ tool đọc (`lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`); trace chỉ ghi handoff đã sanitize.
  + Investigator chạy qua `run_readonly_investigators`; tiền do `compute_compensation` tính, MockLLM chỉ soạn chữ.
  + Chỉ orchestrator gọi `durability.issue_refund` với quote đầy đủ và `crash_at`; `InjectedCrash` được ghi trace rồi ném lại.

### Bằng chứng

- Commit: `3565f22` (`feat(shape-c): implement orchestrator with read-only investigators`)
- Test tự viết: `src/tests/test_orchestrator_boundaries.py` (19/19 passed)
- Test của vudung2003: `src/tests/test_orchestrator_shape.py` (commit `726d632`; 5/5 passed trên code Shape C)
- Ma trận student: `pytest -q -m student -o addopts= -k orchestrator` (62/62 passed)
- `python -m lab8.check_submission`: `[ OK ] shape orchestrator: format đúng, 12/12 claim public pass ở seed 11`
- Báo cáo chi tiết: `report/team/2A202603502_NguyenNgocHieu.md`

## 2A202603400_BuiVanLam

- Shape B dùng vòng ReAct tối đa 8 bước, công cụ đọc và cổng ghi hoàn tiền của host.
- Báo cáo cá nhân: [2A202603400_BuiVanLam.md](report/team/2A202603400_BuiVanLam.md).

## 2A202603435_PhiHoangNam

- Tích hợp và kiểm thử các ca crash sau checkpoint, approval cấp cho claim khác và secret trong ticket.
- Sửa trace Workflow và chạy lại test, benchmark, crash suite trước khi chốt ADR.
- Báo cáo cá nhân: [2A202603435_PhiHoangNam.md](report/team/2A202603435_PhiHoangNam.md).

## 2A202603486_VuQuangDung

- Kiểm thử riêng Shape B và C, gồm ca crash ở cả ba mốc ghi hoàn tiền.
- Báo cáo cá nhân: [2A202603486_VuQuangDung.md](report/team/2A202603486_VuQuangDung.md).
