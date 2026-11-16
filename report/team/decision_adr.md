# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: c1d6059
- Run id dẫn chứng: R-workflow-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000 - 1.000 / 0.000000
- Cost per success (mô phỏng, VND): 27.86 VND
- Crash safety: 20/20 trên suite host và Swarm (src/reports/crash.json). Workflow qua T11, T12 và after_checkpoint trong pytest.
- Secret leak / approval bypass: 0 / 0 trong các ca public và test tích hợp tương ứng của Workflow.

## Vì sao shape này

Chọn Workflow (Shape A) theo tiêu chí dùng mức tự chủ thấp nhất đáp ứng yêu cầu. Trên cùng 14 claim và 5 seed, Workflow, Single và Orchestrator đều đạt 70/70, pass^5 bằng 1 và phương sai bằng 0. Workflow có chi phí mỗi lần thành công thấp nhất, 27,86 VND mô phỏng, so với 39,53 của Single và 56,52 của Orchestrator. [Benchmark](../../src/reports/benchmark.json).

## Có đáng đổi lấy multi-agent không

Trên bộ public, Orchestrator có cùng tỷ lệ pass với Workflow ở chi phí cao hơn. Swarm đạt 69/70 và sai T02 ở seed 55 khi dùng số ngày trễ trong ticket. Có thể xem xét lại lựa chọn nếu dữ liệu mới có nhiều bước xác minh độc lập chạy song song và phép đo trên cùng bộ claim cho thấy lợi ích đủ bù chi phí điều phối.

## Trace và bằng chứng

Workflow ghi các sự kiện `claim`, `lookup_order`, `quote` và `decision` hoặc `refund_outcome` theo nhánh xử lý. Nhánh lỗi ghi `error` hoặc `crash`. Sự kiện `claim` chỉ giữ mã claim và cờ có mã đơn. Dữ liệu đơn đi qua các trường đã cho phép của `lookup_order`.

Trace của lần chạy có tên theo `run_id`. Test tích hợp đặt một secret giả trong ticket, rồi kiểm tra kết quả, các file scanner đọc và stdout/stderr. Ca approval cấp cho claim khác xác nhận không có refund hoặc audit `refund_committed`, và có audit `policy_denied` với lý do `approval_claim_mismatch`. [Test tích hợp](../../src/tests/test_safety_integration.py).

## Giới hạn

MockLLM và chi phí là mô phỏng. Latency được ghi là `unavailable`. Số bước trong benchmark là số sự kiện trace. Các kết quả trên thuộc bộ public và các ca tích hợp. Điểm hidden do giảng viên đo.
