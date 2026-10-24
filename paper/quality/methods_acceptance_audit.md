# Bảng kiểm đối chiếu nghiệm thu Phần Vật liệu và Phương pháp

**Phạm vi:** Đối chiếu yêu cầu trong `check paper.docx` với bằng chứng trong repository. Bảng kiểm phân biệt thông tin đã xác minh với yêu cầu chưa được triển khai hoặc chưa có đủ căn cứ. Tài liệu yêu cầu không được xem là bằng chứng cho kết quả thực nghiệm.

## Dữ liệu và các tập đánh giá

| Yêu cầu | Bằng chứng trong repository | Trạng thái |
|---|---|---|
| Dataset hợp nhất N=2.664; 1.918 mẫu lành tính và 746 mẫu lừa đảo | Đọc CSV bằng `csv.DictReader`: 2.664 bản ghi; nhãn 0=1.918, nhãn 1=746. | Đã xác minh số bản ghi và phân bố nhãn. |
| Khử trùng lặp dataset | CSV có 2.630 giá trị `message_id` duy nhất. | Sai khác: có 34 bản ghi trùng ID; chỉ từ ID không thể kết luận nội dung trùng nhau. |
| Frozen test N=267, gồm 192 Ham và 75 Scam | Có `vietnamese_sms_test.csv`; E2E runner tái tạo tập test từ CSV hợp nhất với `test_size=0.100187`, `random_state=42`, phân tầng theo nhãn. | Đã ghi nhận cách chia và số lượng theo lớp yêu cầu; chưa đối chiếu từng dòng giữa CSV frozen được đặt tên và tập tái tạo. |
| Tập huấn luyện/validation 90%, N=2.397 | 2.664 - 267 = 2.397. README dữ liệu lại ghi nguồn có 2.665 mẫu và tập train 2.398 mẫu. | N=2.397 khớp dataset hiện tại và kích thước test; README đã cũ hoặc không nhất quán. |
| Cohen's kappa=0,88 | Có nhắc trong bản xem trước bài báo và phần hạn chế; chưa tìm thấy hồ sơ gán nhãn hoặc dữ liệu đầu vào để tính. | Chưa xác minh; không trình bày như số liệu đã được kiểm chứng độc lập. |
| Hard Forensic Suite N=117; 98 mẫu lừa đảo, 19 mẫu hợp lệ | `master_test_suite.jsonl`: 117 bản ghi, nhãn chuẩn SCAM=98 và HAM=19. | Đã xác minh số lượng và nhãn. Thành phần OTP/dịch vụ cần rà nội dung để xác nhận. |
| E2E suite tổng hợp N=384 | E2E runner ghép 267 mẫu test tái tạo với 117 mục trong suite. | Mã runner hỗ trợ cách tính tổng; chưa xác minh có trùng mẫu giữa hai tập hay đã loại trùng. |

## WBCE, huấn luyện và ONNX

| Yêu cầu | Bằng chứng trong repository | Trạng thái |
|---|---|---|
| WBCE ở Công thức (1) và đạo hàm theo logit ở Công thức (2) | Hàm mất mát trong bản thảo là BCE có trọng số theo lớp. Đạo hàm theo logit cần giữ hệ số ngoài `1/N` của hàm mất mát. | Đã sửa công thức trong phần Phương pháp để có `1/N`; đạo hàm mỗi mẫu được nhân hệ số này. |
| Giải thích alpha=5 | Thành phần loss của lớp dương được nhân 5. | Không khẳng định gradient của mọi lỗi lớp dương luôn lớn gấp 5; tỷ lệ còn phụ thuộc xác suất dự đoán và trường hợp so sánh. **Chưa xác minh $\\alpha=5.0$ trong lần huấn luyện thực tế.** Phép toán xác nhận được ý nghĩa của hệ số trong công thức; nhưng để khẳng định mô hình đã được huấn luyện với giá trị này, cần cấu hình hoặc log huấn luyện làm bằng chứng. |
| Learning rate, warmup, weight decay, số epoch và batch size | Các giá trị có trong tài liệu nghiệm thu và bản Phương pháp cũ, nhưng chưa tìm thấy cấu hình/nhật ký huấn luyện trong các đường dẫn đã rà. | Chưa xác minh bằng artifact của lần chạy; cần liên kết với cấu hình hoặc log được lưu trước khi coi là quy trình thực nghiệm đã xác nhận. |
| ONNX INT8 dung lượng 390 MB, latency 15,8 ms | Bản Phương pháp nêu các số này; bộ phân loại cục bộ có thể nạp thư mục release hoặc đường dẫn ONNX. Chưa tìm thấy artifact ONNX tương ứng và log benchmark. | Chưa xác minh. Không gọi mô hình là INT8 hoặc nói latency đã được tái lập nếu thiếu artifact và thông tin môi trường đo. |

## Hội đồng và bảo vệ dữ liệu

| Yêu cầu | Bằng chứng trong repository | Trạng thái |
|---|---|---|
| Occam 3-agent, trọng số 0,35/0,35/0,30, defender delta 0,25 | `pipeline/forensic_council.py` và `config/council_registry.yaml` triển khai năm chuyên gia với trọng số riêng; mức điều chỉnh veto của Public Defender là 0,25. | Sai khác: mã hiện có là 5-agent, không phải cấu hình 3-agent trong yêu cầu. Không báo cáo kết quả 3-agent như thể được tạo bởi mã này. |
| Ba nhãn SCAM-RISK / LOW-RISK / UNKNOWN với ngưỡng 0,60/0,40 | Mã xuất nhãn SCAM / HAM / SUSPICIOUS_REVIEW với ngưỡng 0,60 và 0,40. | Sai khác: bộ nhãn không khớp; mã hiện tại không dùng nhãn UNKNOWN. |
| Điều 25 Nghị định 13/2023/NĐ-CP và che PII | Mã hội đồng đã rà gửi nội dung tin nhắn làm prompt. `runner.py` che bí mật trong thông báo lỗi/ghi vết API; thao tác đó không phải khử PII trong nội dung tin nhắn. | Chưa có bằng chứng về khử PII trong nội dung trước khi gửi tới mô hình/API. Chưa nên tuyên bố tuân thủ pháp lý khi chưa ghi nhận quy trình khử và xử lý dữ liệu. |

## Các việc cần hoàn tất

1. Làm rõ các ID lặp và xác định bản ghi có trùng nội dung hay không trước khi tuyên bố dataset đã khử trùng; giữ nguyên CSV nguồn và ghi nhận riêng mọi dataset dẫn xuất.
2. Đối chiếu CSV frozen được nêu tên với tập test do runner tạo; lưu manifest có thể kiểm tra gồm ID mẫu, seed, phương pháp phân tầng và checksum.
3. Bổ sung cấu hình/log lần chạy huấn luyện, dữ liệu đầu vào tính độ nhất trí giữa người gán nhãn, cùng metadata artifact/benchmark ONNX cho các tuyên bố tương ứng.
4. Xác minh giá trị $\\alpha=5.0$ đã dùng trong lần huấn luyện bằng cấu hình hoặc log của lần chạy; chỉ khẳng định mô hình được huấn luyện với giá trị này khi có bằng chứng truy xuất được.
5. Thiếu checkpoint ViSoBERT và artifact ONNX đã xuất; nếu chưa có artifact, xuất ONNX INT8 từ checkpoint đã dùng trong thí nghiệm. Kiểm tra kiểu dữ liệu/trọng số để xác nhận lượng tử hóa INT8 và đo kích thước artifact thực tế. Sau đó chạy benchmark suy luận trên CPU với tập đầu vào cố định, ghi lại lệnh chạy, phần cứng, phiên bản runtime/thư viện, số lượt warm-up, số lần đo và cách tính latency. Lưu artifact cùng log kết quả vào thư mục thí nghiệm; cập nhật Phần III bằng số đo tái lập được, hoặc bỏ/đánh dấu chưa xác minh các số 390 MB và 15,8 ms nếu không thể tái tạo.
6. Xác nhận cấu hình hội đồng nào là chuẩn nghiệm thu. Nếu bắt buộc 3-agent, cần triển khai và benchmark cấu hình đó trước khi mô tả kết quả; nếu không, cập nhật yêu cầu nghiệm thu theo quy trình phê duyệt của dự án.
7. Triển khai và kiểm tra việc khử PII khỏi nội dung tin nhắn trước khi gọi API bên ngoài; ghi lại quy trình lưu giữ/xử lý dữ liệu và đề nghị người phụ trách dự án rà soát diễn giải pháp lý trước khi tuyên bố tuân thủ Nghị định.

## Các tệp nguồn đã kiểm tra

- `data/raw/vietnamese_sms_merged_all.csv`
- `data/raw/vietnamese_sms_test.csv`
- `data/raw/README.md`
- `experiments/tier2_council/data/master_test_suite.jsonl`
- `experiments/e2e_two_tier/runner_e2e_benchmark.py`
- `pipeline/forensic_council.py`
- `config/council_registry.yaml`
- `pipeline/local_classifier.py`
- `paper/sections/03_method.tex`
