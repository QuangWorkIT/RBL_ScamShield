# Báo Cáo Đo Lường Benchmark Suy Luận ONNX trên CPU (Tier 1 Edge)

## 1. Môi Trường Thực Nghiệm và Phần Cứng
- **Hệ điều hành:** Windows-11-10.0.26200-SP0
- **Bộ xử lý (CPU):** Intel64 Family 6 Model 141 Stepping 1, GenuineIntel
- **Kiến trúc:** AMD64
- **Số nhân vật lý / logic:** 6 nhân vật lý / 12 luồng logic
- **RAM tổng cộng:** 15.78 GB
- **Phiên bản Runtime:** Python 3.14.0, ONNXRuntime v1.31.0
- **Tập dữ liệu đầu vào:** Cố định $N=267$ mẫu (`data\processed\frozen_test_267.csv`)
- **Số lượt warm-up:** 50 lượt; **Số lần đo lường:** 534 lần (2 vòng lặp qua 267 mẫu)

## 2. Bảng Đối Soát Kích Thước và Độ Trễ Tái Lập Được

| Mô hình Artifact | Định dạng Trọng số | Dung lượng File (MiB) | Dung lượng File (MB thập phân) | Mean Latency (ms) | Median Latency (ms) | P95 Latency (ms) | P99 Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| FP32_Baseline | FP32 | 372.45 MiB | 390.54 MB | 150.6 ms | 150.43 ms | 167.57 ms | 180.28 ms |
| INT8_Quantized | INT8 Dynamic | 93.86 MiB | 98.42 MB | 70.72 ms | 70.66 ms | 80.48 ms | 86.64 ms |

