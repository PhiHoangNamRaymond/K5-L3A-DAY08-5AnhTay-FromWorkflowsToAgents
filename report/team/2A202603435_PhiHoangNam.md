# Báo cáo cá nhân Lab 8 — Phí Hoàng Nam

## 1. Thông tin thành viên

- Họ tên: Phí Hoàng Nam
- MSSV: 2A202603435
- Email: phinamyb2004@gmail.com
- GitHub: PhiHoangNamRaymond
- Nhóm: 5AnhTay, lớp L3A

## 2. Phần việc phụ trách

Tích hợp và kiểm thử an toàn các kiến trúc xử lý yêu cầu hoàn phí của LogiX-VN. Phần việc của tôi tập trung vào quyền hoàn tiền, khả năng chạy lại sau crash và dữ liệu được ghi vào trace.

## 3. Đóng góp cụ thể

- Bổ sung ca crash tại `after_checkpoint`. Test xác nhận refund và checkpoint đã được ghi trước khi mô phỏng lỗi, rồi chạy lại cùng claim, seed và SQLite DB để kiểm tra hệ thống giữ đúng số tiền và chỉ có một refund cùng một audit `refund_committed`.
- Kiểm tra A–C khi claim trỏ đến approval hợp lệ của một claim khác. Kết quả yêu cầu là `denied`, giữ nguyên mức hoàn đề xuất, ledger có 0 refund và audit ghi `approval_claim_mismatch`.
- Đặt một chuỗi nhận diện bí mật giả trong ticket để kiểm tra kết quả, trace và stdout/stderr. Test tái hiện việc Workflow ghi nguyên ticket vào trace. Bản sửa chỉ giữ mã claim và cờ cho biết claim có mã đơn.
- Tái tạo bằng chứng từ benchmark và crash suite. Thử bật và tắt đúng một lượt đọc lịch sử hoàn tiền trong Orchestrator để đo chi phí với cùng dữ liệu, seed, bảng giá và bộ chấm.

## 4. Bằng chứng

- Commit kỹ thuật: `f76645f`.
- Test tích hợp: [test_safety_integration.py](../../src/tests/test_safety_integration.py). Trước khi sửa có 1 ca fail ở Workflow. Sau khi sửa, 10 ca tích hợp và toàn bộ 318 test đều pass.
- Crash suite chính thức đạt 20/20 cho các kịch bản của host và Swarm. Các ca T11, T12 và `after_checkpoint` trên A–C có bằng chứng riêng trong pytest. [Crash report](../../src/reports/crash.json).
- Workflow đạt 70/70 trial public và 27,86 VND mô phỏng trên mỗi lần thành công. Run ID đối chiếu là `R-workflow-C-001-s11`. [Benchmark](../../src/reports/benchmark.json) · [ADR](decision_adr.md).

## 5. Công cụ AI đã dùng

Dùng Codex để đọc hợp đồng của lab, giải thích seed và các mốc crash, soạn test, rà code và hỗ trợ tổng hợp báo cáo. Bằng chứng được kiểm tra bằng pytest, tool sinh JSON của lab và đối chiếu trạng thái, ledger, audit và trace trong các test.

Các lệnh để tự đối chiếu từ thư mục `src/`:

```text
python -m pytest -q -m student -o addopts= tests/test_safety_integration.py
python -m lab8.crash_test --count 20 --out reports/crash.json
python -m lab8.check_submission
```

## 6. Tự đánh giá

Kết quả phần tích hợp có thể kiểm tra qua test và file báo cáo được sinh từ công cụ. Với lỗi crash, việc đối chiếu một khoản hoàn tiền và một audit trên cùng DB cho bằng chứng trực tiếp về khả năng chạy lại. Với lỗi rò dữ liệu, test trước và sau bản sửa cho thấy trường `ticket` là nguyên nhân. Phạm vi kiểm chứng là bộ public và các ca tích hợp nêu trên. Bộ hidden do giảng viên chạy.
