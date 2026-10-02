# 📦 THƯ MỤC DỮ LIỆU THÔ (RAW DATASET REPOSITORY)
### Đề tài: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `data/raw/README.md`  
> **Tuân thủ:** Quality Gate E2 & Tiêu chuẩn liêm chính dữ liệu RBL

---

## 1. Nguồn Dữ Liệu Gốc (Data Sources)

Dữ liệu được thu thập và tổng hợp từ 2 kho ngữ liệu mở công khai trên Hugging Face Hub:
1. **Nguồn chính thống 1:** `uitnlp/vietnamese-sms-dataset`
   * **URL:** `https://huggingface.co/datasets/uitnlp/vietnamese-sms-dataset`
   * **Tổ chức xuất bản:** UIT-NLP (Đại học Công nghệ Thông tin - ĐHQG TP.HCM).
   * **Giấy phép (License):** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
   * **Ngày tải:** 2026-08-15.
2. **Nguồn bổ sung 2:** `vietnamese_sms_phishing_sample_300`
   * **URL:** Hugging Face Community Open Corpus.
   * **Mô tả:** Tập mẫu tin nhắn SMS mạo danh thương hiệu, thông báo trúng thưởng và tin nhắn giả mạo biến thể mới.
   * **Giấy phép (License):** Open Data Commons Attribution License (ODC-By).
   * **Ngày tải:** 2026-08-18.

---

## 2. Danh Mục Các Tệp Dữ Liệu Trong Thư Mục

| Tên tệp tin | Số lượng dòng | Cấu trúc các cột (Columns Schema) | Mục đích sử dụng |
| :--- | :---: | :--- | :--- |
| **`vietnamese_sms_merged_all.csv`** | **$2.665$ mẫu** | `message_id`, `message`, `label`, `source` | **Tập dữ liệu tổng hợp chính thức** sau khi tiền xử lý và loại bỏ bản ghi trùng lặp. |
| **`vietnamese_sms_test.csv`** | $267$ mẫu | `message`, `label` | **Tập Frozen Test Set** niêm phong cố định ($192$ Ham, $75$ Scam) dùng cho mọi mô hình. |
| `hf_vietnamese_sms_dataset.csv` | $5.983$ mẫu | `message_id`, `date`, `message`, `label` | Bản sao thô nguyên gốc từ Hugging Face. |
| `hf_vietnamese_sms_phishing_sample_300.csv` | $601$ mẫu | `message_id`, `text` | Tập mẫu bổ sung lừa đảo thực tế. |
| `vietnamese_sms_full.csv` | $2.991$ mẫu | `message_id`, `date`, `message`, `label` | Tập dữ liệu hợp nhất trung gian trước khi deduplication. |

---

## 3. Quy Ước Mã Hóa Nhãn (Label Encoding)

* **`0` $\rightarrow$ HAM:** Tin nhắn bình thường, thông báo hợp lệ từ ngân hàng/nhà mạng, mã OTP xác thực, tin nhắn cá nhân hợp pháp.
* **`1` $\rightarrow$ SCAM:** Tin nhắn lừa đảo tài chính, mạo danh đường dẫn ngân hàng (phishing link), tin nhắn trúng thưởng giả, dụ dỗ tuyển dụng lừa tiền cọc, tin nhắn spam độc hại.

---

## 4. Phân Bổ Dữ Liệu & Quy Tắc Niêm Phong (Frozen Test Set Protocol)

Tập dữ liệu hợp nhất $2.665$ mẫu (`vietnamese_sms_merged_all.csv`) gồm:
* **Ham (Nhãn 0):** $1.918$ tin nhắn ($72.0\%$).
* **Scam (Nhãn 1):** $747$ tin nhắn ($28.0\%$).

### Phân Tách Tập Dữ Liệu Cố Định:
Toàn bộ quy trình phân tách sử dụng kỹ thuật phân tầng (*Stratified Split*) với seed cố định: `random_state = 42`:
* **Tập Huấn luyện & Validation nội bộ ($90\%$):** $2.398$ mẫu ($1.726$ Ham, $672$ Scam).
* **Tập Kiểm thử Đóng băng (Frozen Test Set, $10\%$):** **$267$ mẫu** ($192$ Ham, $75$ Scam).

> [!CRITICAL]
> **Quy tắc niêm phong (Frozen Isolation Rule):**  
> 1. Tập Frozen Test Set ($N=267$) **tuyệt đối không được dùng để huấn luyện mô hình** hoặc tối ưu tham số/ngưỡng threshold.
> 2. Mọi mô hình trong bài báo (ViSoBERT, PhoBERT-base, FPT ViBERT, PhoBERT-large, Gemini 3.5 Flash) **bắt buộc phải được đánh giá trên cùng một tập $267$ mẫu này** để đảm bảo tính công bằng và điều kiện kiểm định ghép cặp (Paired McNemar Test).
> 3. Không được sửa đổi, xóa dòng hoặc chèn thêm dữ liệu vào tệp `vietnamese_sms_merged_all.csv`.
