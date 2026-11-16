# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R1 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Kim và cộng sự (2026, bản v2), [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296v2), preprint thực nghiệm có benchmark đối chứng. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Trên tác vụ lập kế hoạch tuần tự PlanCraft, các cấu hình nhiều agent được thử có hiệu năng giảm 39–70% so với single agent. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Tỷ lệ giảm thuộc PlanCraft trong thiết lập nghiên cứu. Lab đo 14 claim LogiX-VN với MockLLM và giá mô phỏng. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Tắt lượt đọc lịch sử hoàn tiền trong investigator của Orchestrator sẽ giảm khoảng 9–10 VND mô phỏng trên mỗi lần thành công. Dự đoán pass rate giữ nguyên vì host tự kiểm tra lịch sử trước khi ghi tiền. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ cùng runner Orchestrator, MockLLM, registry công cụ, 14 claim, 5 seed chuẩn, database mới mỗi trial, bảng giá và evaluator. Biến thay đổi là investigator có gọi `lookup_refund_history` hay không. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | So pass rate, pass^5, seed variance và cost/success. Theo dõi T13 và T14 vì hai ca có khoản hoàn trước đó và kiểm tra trần hoàn tiền theo đơn. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m scripts.ablate_investigator_refund_history --out reports/investigator_ablation.json`
- Run id / file report: `R-orchestrator-C-001-s11` là trial mẫu của cả hai điều kiện trong [investigator_ablation.json](../../src/reports/investigator_ablation.json).
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: Đúng trên dữ liệu public. Chi phí giảm từ 56,52 xuống 47,23 VND mỗi lần thành công, tương đương giảm 9,29 VND. Hai điều kiện đều pass 70/70, trong đó có T13 và T14 ở cả năm seed. Pass^5 đều bằng 1 và seed variance bằng 0.
- Giới hạn: Phép đo chỉ thay đổi một lượt đọc trong Orchestrator. Kết quả phản ánh 14 claim public, MockLLM và giá mô phỏng. Latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
