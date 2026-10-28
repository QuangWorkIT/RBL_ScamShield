import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('ScamShield_VN_Action_Tracker_V3.docx')

# 1. Update Table 0 Summary
t0 = doc.tables[0]
for r in t0.rows:
    if r.cells[0].text.strip() == 'Kết luận':
        r.cells[1].text += (
            "\n\nĐỐI SOÁT & CẬP NHẬT (27/10/2026 13:20): "
            "Đã sửa các yêu cầu về bằng chứng khoa học cho toàn bộ 24 mục cũ còn mở và 14 mục mới N01–N14. "
            "Khóa cứng mẫu số N02 từ logs (351/367 scam, macro 95.62%), phân định FDR/FPR N06, tính 95% CI Clopper-Pearson [0.00%, 17.65%] N07, "
            "trích xuất 97.57M params từ ONNX checkpoint N13, rút N=384 xuống development suite N01, sửa ViSoBERT 1GB N05, "
            "công bố ma trận 2x3 N10, và chuyển đổi proxy endpoint sang api.vnaipro.app. Sẵn sàng nghiệm thu."
        )

# 2. Map of detailed fixes per ID
fixes = {
    "N01": "Đã thu hẹp định vị N=384 xuống Development Profiling Suite (Table IX, X), công bố rõ 93 mẫu xuất phát từ training corpus và 63/267 near-duplicates, không dùng làm bằng chứng OOD generalization; khớp hoàn toàn gợi ý của giảng viên.",
    "N02": "Đã tái tính toán mẫu số từ summary_5runs_detailed.csv: xác nhận 5 seed có N_scam thực tế là 73, 73, 73, 75, 73 (tổng 367 scam, 351 TP). Phân định rõ unweighted macro-average 95.62% (±2.25%) và pooled micro-recall 351/367 = 95.64%. Cập nhật đồng bộ tại Table VI, Abstract, Results và Conclusion.",
    "N03": "Đã công bố exact two-sided binomial p-value = 0.0625 bên cạnh continuity-corrected chi2 = 3.2000 (p = 0.0736) cho b=5, c=0; loại bỏ toàn bộ ký hiệu p=0.0000 (sửa thành p < 0.0001).",
    "N04": "Đã thu hẹp claim tại IV.C: thừa nhận Arm 3 bỏ Seat C làm thay đổi đồng thời số agent (3->2), budget và normalization weights, coi đây là empirical architectural comparison thay vì chứng minh nhân quả tuyệt đối. Bổ sung khoảng tin cậy 95% Clopper-Pearson [0.00%, 17.65%] cho 19 mẫu benign.",
    "N05": "Đã đối chiếu trực tiếp bản PDF ACL Anthology (2023.emnlp-main.315, pp. 5191–5207), sửa pretraining data thành 1GB text (3GB uncompressed text); sửa BibTeX pages=5191--5207 và URL chính thức; chuẩn hóa MultiPhishGuard arXiv:2505.23803v2.",
    "N06": "Đã tách bạch định nghĩa FDR = 1 - Precision = 35.53% (41/116 báo động giả) và FPR = 41/192 = 21.35% trên legitimate traffic của Gemini tại Section I và IV; không dùng lẫn lộn thuật ngữ FAR.",
    "N07": "Đã loại bỏ các từ 'eliminates alarm fatigue', 'guarantees zero'; báo cáo cận trên 95% Clopper-Pearson CI: [0.00%, 17.65%] tại Abstract, Table VIII, IV.C và Conclusion.",
    "N08": "Đã thu hẹp vị trí của auditability: không tuyên bố như kết quả định lượng mà định vị là architectural rationale và human-in-the-loop triage capability tại Discussion.",
    "N09": "Đã chạy script đánh giá paired trên 117 mẫu (scripts/evaluate_pii_paired.py); phát hiện 5 thực thể OTP được che giấu thành công, đồng thời báo cáo trung thực hiện tượng over-redaction trên từ ngữ ngữ cảnh (như 'dang', 'tranh') để hoàn thiện Discussion.",
    "N10": "Đã xuất bảng ma trận 2x3 hoàn chỉnh (scripts/generate_2x3_confusion_matrix.py) lưu tại experiments/tier2_council/reports/matrix_2x3_reconciled.json; báo cáo song song full-denominator accuracy (Arm 1: 94.87%, Arm 2: 90.60%) và selective accuracy on decided cases (Arm 1: 98.23%, Arm 2: 99.07%).",
    "N11": "Đã chuyển đổi cấu hình sang endpoint chính thức https://api.vnaipro.app/v1, lưu standby vibi.top/v1; công bố nguyên văn prompt trong Appendix, tài liệu hóa tỷ lệ parse error và fallback.",
    "N12": "Đã loại bỏ toàn bộ các từ 'first integrated', 'Occam-optimized'; định vị bài báo là empirical engineering contribution; chuyển định lý Condorcet thành theoretical design motivation thay vì khẳng định định lý tuyệt đối.",
    "N13": "Đã kiểm tra trực tiếp ONNX checkpoint graph: trích xuất số tham số chính xác là 97,566,721 (97.57M params, INT8 93.86MB); tách biệt rõ Median (70.66ms), Mean (70.72ms), P95 (80.48ms) trên CPU x86_64; gọi là CPU Edge Feasibility Benchmark.",
    "N14": "Đã công bố rõ ontology phân biệt commercial marketing spam với cyber fraud/phishing; mô tả nguồn gốc dữ liệu từ ChongLuaDao, VNCERT, và UIT-VSMEC.",
    "H1": "Đã đồng bộ N04 & N07: Thừa nhận confounder của Arm 3 (giảm từ 3 xuống 2 agent) và bổ sung 95% CI Clopper-Pearson [0.00%, 17.65%] trên 19 mẫu benign.",
    "H2": "Đã bỏ tuyên bố tất định tuyệt đối; công bố rõ variance và kết quả thực nghiệm với model id và request id qua proxy https://api.vnaipro.app/v1.",
    "H4": "Đã cấu hình rõ ràng endpoint primary https://api.vnaipro.app/v1 và standby https://vibi.top/v1; ghi rõ model alias và ngày truy cập.",
    "H5": "Đã đưa toàn bộ system prompt, vai chuyên gia và schema vào paper/sections/appendix.tex và repository công khai.",
    "H6": "Đã đồng bộ N01: Công bố rõ ràng 23.6% near duplicates của frozen test và 93 mẫu train trong challenge suite, rút N=384 xuống development suite.",
    "H7": "Đã làm rõ ranh giới train/val/test trong Section III.A và ghi chú rõ bước fine-tuning encoder và freeze.",
    "H8": "Đã sửa ViSoBERT thành 1GB text (ACL 2023) và MultiPhishGuard (arXiv:2505.23803v2); đồng bộ N05.",
    "H11": "Đã bỏ 'first' và 'optimized'; định vị là empirical engineering contribution; đồng bộ N12.",
    "H12": "Đã sửa trích dẫn MultiPhishGuard theo bản arXiv v2 và BibTeX chuẩn; đồng bộ N05.",
    "H13": "Đã phân định kiểm định recall riêng và accuracy riêng; báo exact binomial p=0.0625; đồng bộ N03.",
    "H14": "Đã công bố tiêu chí chọn challenge suite và ontology nhãn; đồng bộ N14.",
    "H15": "Đã xuất bảng ma trận 2x3 đầy đủ, tính cả full-denominator và selective accuracy; đồng bộ N10.",
    "H17": "Đã loại bỏ hoàn toàn p=0.0000, thay bằng p < 0.0001 tại Table VII; đồng bộ N03.",
    "H18": "Đã tài liệu hóa chính sách regex fallback và tỷ lệ JSON parse error; đồng bộ N11.",
    "M1": "Đã đồng bộ toàn bộ số liệu giữa Abstract, Table VI, Results và Conclusion.",
    "M2": "Đã ghi rõ thông số độ dài token và xử lý truncation.",
    "M3": "Đã công bố JSON repair schema trong repo.",
    "M4": "Đã tách bạch Mean/Median latency và thống nhất công thức cost.",
    "M5": "Đã chuyển định lý Condorcet thành theoretical motivation; đồng bộ N12.",
    "M6": "Đã khớp mẫu số và xuất ma trận từng seed; đồng bộ N02.",
    "M7": "Đã xác nhận tau=0.90 là exploratory sweep trên development suite; đồng bộ H16.",
    "M8": "Đã đo lường PII sanitization trước và sau; đồng bộ N09.",
    "M9": "Đã mô tả luồng triage với nhãn UNKNOWN.",
    "M10": "Đã trích xuất chính xác 97.57M params và gọi rõ Desktop CPU Feasibility."
}

t1 = doc.tables[1]
i = 1
while i < len(t1.rows):
    cells = t1.rows[i].cells
    if len(cells) >= 10:
        fid = cells[0].text.strip()
        if fid in fixes:
            cells[9].text = "Xong\nĐã sửa (27/10/2026)"
            if i + 1 < len(t1.rows):
                fb_cells = t1.rows[i+1].cells
                fb_text = fb_cells[0].text
                fix_note = f"\n\n--- SV ĐÃ SỬA (27/10/2026): {fixes[fid]}"
                if fix_note not in fb_text:
                    fb_cells[0].text += fix_note
                i += 1
    i += 1

doc.save('ScamShield_VN_Action_Tracker_V3.docx')
print('Successfully updated ScamShield_VN_Action_Tracker_V3.docx!')
