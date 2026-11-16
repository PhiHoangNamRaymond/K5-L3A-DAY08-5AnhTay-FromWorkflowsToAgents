# Team

## Thông tin nhóm

- Tên nhóm: 5AnhTay
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-5AnhTay-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/PhiHoangNamRaymond/K5-L3A-DAY08-5AnhTay-FromWorkflowsToAgents.git, nhánh main

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Hải Anh | 2A202603484 | haianh29112@gmail.com | haianh02034 | Workflow (Shape A) |
|   2 |        |      |       |        |         |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Hải Anh | workflow | 54917fd | src/tests/test_workflow_shape.py |

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

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
