# PRISMA 2020 Flow Diagram - Nguyen Trung Hieu

> **Protocol Version:** 1.0 (PRISMA 2020 Compliant)  
> **Reviewer:** `Nguyen Trung Hieu` (PL / LR)  
> **Topic:** Vietnamese Scam & Smishing Detection with Pre-trained Transformers and LLMs  
> **Databases Searched:** ArXiv, OpenAlex, Semantic Scholar, CrossRef, Google Scholar

---

## 1. PRISMA Flowchart Summary

```text
[Bản ghi tìm kiếm từ 5 CSDL học thuật (N = 943)]
        ↓
[Sau khi loại trùng lặp nội bộ (N = 471)]
        ↓
[Sàng lọc Vòng 1: Tiêu đề & Tóm tắt (N = 471)]
        ↓
[Loại bỏ Vòng 1 (N = 460): EC1=312, EC2=84, EC4=42, EC3=22]
        ↓
[Toàn văn được đánh giá chuyên sâu Vòng 2 (N = 11)]
        ↓
[Loại bỏ Vòng 2 (N = 0)]
        ↓
[Số lượng bài báo chính thức được đưa vào phân tích (N = 11)]
```

---

## 2. Chi Tiết Đối Soát Dữ Liệu Thực Tế
* **File `01_all_records.csv`:** $943$ dòng bản ghi thô thu thập từ các API CSDL.
* **File `02_after_screening_v1.csv`:** $943$ dòng được gán nhãn sàng lọc tiêu chuẩn.
* **File `03_final_included.csv`:** $11$ bài báo đáp ứng đầy đủ tiêu chuẩn `IC1`–`IC4`.
* **File `evidence-table.md`:** $11$ bài báo được trích xuất dữ liệu thực chứng 7 cột bắt buộc.
