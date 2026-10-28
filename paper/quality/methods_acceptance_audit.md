# Bảng kiểm đối chiếu nghiệm thu Phần Vật liệu và Phương pháp (Đã Cập Nhật Nghiệm Thu)

**Phạm vi:** Đối chiếu yêu cầu trong `check paper.docx` với bằng chứng trong repository sau đợt cập nhật và đồng bộ hóa thực nghiệm.

## 1. Dữ liệu và các tập đánh giá

| Yêu cầu | Bằng chứng trong repository | Trạng thái |
|---|---|---|
| Dataset hợp nhất N=2.664; 1.918 mẫu lành tính và 746 mẫu lừa đảo | `data/raw/vietnamese_sms_merged_all.csv`: 2.664 bản ghi; nhãn 0=1.918, nhãn 1=746. | **Đã xác minh**: Đúng số bản ghi và tỷ lệ nhãn. |
| Khử trùng lặp dataset & giải trình ID lặp | Script kiểm tra phát hiện: 2.664 tin nhắn có nội dung văn bản độc nhất 100% (`df['message'].nunique() == 2664`, 0 trùng lặp nội dung). 34 ID trùng là do xung đột không gian tên (namespace collision) giữa 2 nguồn upstream khi cùng gán tiền tố `COM_`. File nguồn được giữ nguyên gốc; manifest dẫn xuất đã lưu riêng. | **Đã giải quyết**: Đã giải trình rõ bản chất xung đột ID và bảo toàn CSV nguồn. |
| Frozen test N=267, gồm 192 Ham và 75 Scam | Script `scripts/generate_frozen_test_manifest.py` đã trích xuất cố định `data/processed/frozen_test_267.csv` và `data/processed/frozen_test_manifest.json` ghi rõ seed 42, `test_size=0.100187`, phân tầng nhãn, cùng mã băm SHA-256. | **Đã giải quyết**: Đã có manifest và CSV cố định để kiểm tra đối chiếu độc lập. |
| Tập huấn luyện/validation 90%, N=2.397 | 2.664 - 267 = 2.397 (1.726 Ham, 671 Scam). Đã ghi nhận trong manifest và Section III. | **Đã xác minh**: Khớp kích thước và phân bố nhãn. |
| Cohen's kappa=0,88 | Hồ sơ gán nhãn thô của 2 người gán nhãn không nằm trong repo mã nguồn; đã cập nhật diễn đạt trong Section III xem đây là chỉ số trong báo cáo chú giải ban đầu của nhóm nghiên cứu, không khẳng định như số liệu log độc lập từ repo. | **Đã giải quyết**: Minh bạch hóa phạm vi dữ liệu. |
| Hard Forensic Suite N=117; 98 mẫu lừa đảo, 19 mẫu hợp lệ | `experiments/tier2_council/data/master_test_suite.jsonl`: đúng 117 bản ghi, nhãn SCAM=98 và HAM=19. | **Đã xác minh**: Khớp 100%. |
| E2E suite tổng hợp N=384 | Ghép 267 mẫu Frozen Test và 117 mẫu Forensic Challenge Suite. | **Đã xác minh**: Khớp cấu trúc $267 + 117 = 384$. |

## 2. WBCE, huấn luyện và ONNX

| Yêu cầu | Bằng chứng trong repository | Trạng thái |
|---|---|---|
| WBCE ở Công thức (1) và đạo hàm theo logit ở Công thức (2) | Đã cập nhật đầy đủ hệ số $1/N$ ở cả Công thức (1) và (2) trong `03_method.tex` và `main.tex`. | **Đã giải quyết**: Công thức toán học chuẩn xác. |
| Giải thích và xác minh $\alpha=5.0$ | Đã tìm thấy bằng chứng tại `models/scamshield_config.json` (`pos_weight_alpha: 5.0`) và `pipeline/local_classifier.py`. Section III đã giải thích rõ tác động gradient. | **Đã xác minh**: Có bằng chứng cấu hình truy xuất được. |
| Siêu tham số huấn luyện (LR, warmup, weight decay, epochs, batch size) | Đã truy xuất từ `models/training_args.bin`: `learning_rate=2e-5`, `epochs=4`, `per_device_train_batch_size=32`, `warmup_ratio=0.0`, `weight_decay=0.01`, `fp16=True`, `seed=42`. Đã đính chính batch size 32 và warmup 0.0 trong Section III. | **Đã giải quyết**: Đã đồng bộ với cấu hình thực tế. |
| ONNX INT8 dung lượng và latency | Đã xuất mô hình INT8 thực sự `models/visobert_tier1_int8.onnx` (dung lượng 98,42 MB / 93,86 MiB, chứa trọng số INT8/UINT8). Chạy benchmark CPU độc lập (`scripts/benchmark_onnx_inference.py`, 534 lượt đo trên 267 mẫu frozen): Median latency INT8 là 70,66 ms (so với 150,43 ms của FP32 390,5 MB). Đã ghi log đầy đủ tại `experiments/tier1_edge/reports/onnx_cpu_benchmark_report.json` và cập nhật Section III. | **Đã giải quyết**: Đã có artifact INT8, log benchmark và số đo tái lập được. |

## 3. Hội đồng và bảo vệ dữ liệu

| Yêu cầu | Bằng chứng trong repository | Trạng thái |
|---|---|---|
| Cấu hình hội đồng (3-agent vs 5-agent) | Section III đã làm rõ cả 2 cấp: (1) Kiến trúc tham chiếu tổng quát 5 chuyên gia (`config/council_registry.yaml`), và (2) Cấu hình tối ưu sản xuất Occam 3-Agent (`runner_ablation_3v5.py`) với trọng số 0,35/0,35/0,30 và Public Defender veto 0,25. McNemar xác nhận không suy giảm ý nghĩa thống kê ($p=0.0736$). | **Đã giải quyết**: Phân định rõ kiến trúc tham chiếu và cấu hình nghiệm thu sản xuất. |
| Ba nhãn SCAM-RISK / LOW-RISK / UNKNOWN | Đã chuẩn hóa bộ 3 nhãn trong `pipeline/forensic_council.py`, `runner_ablation_3v5.py` và Section III theo ngưỡng $\ge 0.60$ (SCAM-RISK), $< 0.40$ (LOW-RISK), và $[0.40, 0.60)$ (UNKNOWN). | **Đã giải quyết**: Khớp 100% giữa lý thuyết và code. |
| Điều 25 Nghị định 13/2023/NĐ-CP và khử PII | Đã triển khai module `MessagePIISanitizer` (`pipeline/pii_sanitizer.py`) tích hợp vào `pipeline/forensic_council.py`, tự động che SĐT, STK, CCCD, OTP, số dư. Đã viết bộ unit test (`tests/test_pii_sanitizer.py`) kiểm thử đạt 100%. Đã điều chỉnh cách diễn giải pháp lý trong Section III theo hướng tuân thủ nguyên tắc kỹ thuật an toàn dữ liệu. | **Đã giải quyết**: Đã triển khai module thực tế và hoàn tất kiểm thử. |

## 4. Danh mục Artifact mới bổ sung

- `data/processed/frozen_test_267.csv`: Tập frozen test 267 mẫu cố định.
- `data/processed/frozen_test_manifest.json`: Manifest kiểm định checksum SHA-256 của tập frozen test.
- `models/visobert_tier1_int8.onnx`: Artifact mô hình ViSoBERT INT8 lượng tử hóa thực tế (98,42 MB).
- `visobert_5runs_release/visobert_tier1_int8.onnx`: Bản sao artifact INT8 trong thư mục release.
- `scripts/benchmark_onnx_inference.py`: Script đo lường benchmark độ trễ suy luận ONNX trên CPU.
- `experiments/tier1_edge/reports/onnx_cpu_benchmark_report.json`: Báo cáo vi mô benchmark ONNX CPU.
- `experiments/tier1_edge/reports/onnx_cpu_benchmark_report.md`: Báo cáo chi tiết môi trường phần cứng và độ trễ.
- `pipeline/pii_sanitizer.py`: Module khử PII (SĐT, STK, OTP, CCCD, số dư) phía client.
- `tests/test_pii_sanitizer.py`: Bộ kiểm thử tự động cho module khử PII.
- `paper/sections/03_method.tex` và `paper/main.tex`: Toàn văn Section III đã được cập nhật chuẩn xác.
