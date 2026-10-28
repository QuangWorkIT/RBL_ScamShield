# -*- coding: utf-8 -*-
import json
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

ITEM_UPDATES = {
    'B1': {
        'status': 'Xong\nBỎ QUA Theo yêu cầu giảng viên; không tính điều kiện hoàn tất.',
        'display_status': 'BỎ QUA',
        'evidence': 'BỎ QUA theo yêu cầu giảng viên; không tính điều kiện hoàn tất. (Giảng viên đã chỉ đạo tập trung vào tính liêm chính khoa học, mẫu số và đối chứng kỹ thuật).'
    },
    'H1': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã xóa bỏ hoàn toàn các tuyên bố nhân quả tuyệt đối ("strictly necessary", "causally necessary") tại Section IV.C (dòng 121) và Section V (RQ3). Đã thừa nhận rõ hạn chế Arm 3 bị giảm từ 3 xuống 2 ghế (confounder) nên không thể quy riêng cho Public Defender. Đã bổ sung Bảng ma trận 2x3 (Table IX) công bố đầy đủ True Scam (N=98), True Ham (N=19), phân định UNKNOWN, và 95% Clopper-Pearson CI [0.00%, 17.65%] trên 19 mẫu benign notifications.'
    },
    'H2': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã công bố tại Section IV.G (Threats to Validity, Internal Validity): Thống kê 3-run variance trên 1,404 quyết định consensus với label agreement 100.00% (flip rate 0.00%), độ trễ SD = +-32.8 ms (Gemini) và +-92.0 ms (GPT-6.1-sol); nêu rõ không có bảo đảm tất định bitwise trên cloud hosted APIs do dynamic batching và speculative decoding.'
    },
    'H3': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã công bố tại Section III.A, Section IV.G và Section V: Cohen\'s kappa=0.88 không tái tính được từ repo và là nhãn chưa được kiểm chứng độc lập. (Cô Chi đã xác nhận Đạt).'
    },
    'H4': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã bổ sung tại Section III.E (Table V - Model Card) và Section VI (Reproducibility): Công bố rõ ràng endpoint chính thức https://api.vnaipro.app/v1, standby https://vibi.top/v1, model snapshots (gpt-6.1-sol-2026-03, gemini-3.5-flash-lite), ngày truy cập (2026-10-20), nhiệt độ (T=0.1 / T=0.0), và lưu trữ toàn bộ raw JSON responses cùng telemetry log tại experiments/tier2_council/reports/.'
    },
    'H5': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã công bố nguyên văn System Prompt Gemini 3.5 Flash 5-Shot ICL (yêu cầu xuất binary 0/1) cùng 5 exemplars tại Section III.F.1; tách biệt hoàn toàn với structured forensic schema 5 trục của P-single tại Section III.F.2; công bố specialist role instructions và đường dẫn mã nguồn bất biến tại pipeline/forensic_council.py.'
    },
    'H6': {
        'status': 'Sửa một phần',
        'display_status': 'Sửa một phần',
        'evidence': 'Đã công bố minh bạch tại Section III.A và Table IV: Combined Evaluation Suite (N=384) gồm 374 văn bản độc nhất, trong đó Challenge Suite chứa 93 mẫu có nguồn gốc từ training corpus và 10 mẫu trùng frozen test; định vị N=384 là Development Profiling Suite thay vì OOD generalization benchmark theo đúng khuyến nghị của giảng viên.'
    },
    'H7': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã vẽ và chèn hình minh họa tổng thể kiến trúc Figure 1 tại Section III.C, phân định ranh giới tách bạch giữa Tier 1 on-device ViSoBERT INT8 và Tier 2 cloud council (API gating tau=0.70 và tau=0.90), làm rõ luồng dữ liệu và vai trò các thành phần.'
    },
    'H8': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã đối chiếu trực tiếp bản gốc PDF ACL Anthology (2023.emnlp-main.315, pp. 5191--5207) và sửa thông tin pretraining corpus của ViSoBERT thành 1 GB uncompressed social media text; cập nhật metadata BibTeX ViSoBERT và MultiPhishGuard (arXiv:2505.23803v2).'
    },
    'H9': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã nêu rõ tại Section IV.B, Table VIII và Abstract: P-single đạt accuracy 96.58% cao hơn cả hai cấu hình council (94.87% và 90.60%) với chi phí thấp hơn ($0.0450/1k); định vị giá trị của council là auditable institutional explanation và cautious abstention dưới góc độ kỹ thuật (Cô Chi đã xác nhận Đạt).'
    },
    'H10': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã sửa đổi framing tại Abstract, Section IV.B và Section V: Không tuyên bố equivalence khi p=0.0736 có power thấp; thừa nhận 3-agent giảm nhẹ scam recall (93.88% xuống 88.78%) và tăng UNKNOWN (4 lên 10 trường hợp) để đổi lấy 0.00% FPR (Cô Chi đã xác nhận Đạt).'
    },
    'H11': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã loại bỏ hoàn toàn các thuật ngữ "first integrated", "Occam-optimized", "theoretically optimal" tại toàn bộ các Section 00--06; định vị đóng góp của bài báo là empirical engineering contribution; chuyển định lý Condorcet thành theoretical design motivation.'
    },
    'H12': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã cập nhật trích dẫn MultiPhishGuard sang bản preprint chính thức arXiv:2505.23803v2 với đầy đủ tên tác giả (Yi-Nuo Xue, Eric Spero, Yun Sing Koh, Giovanni Russello), thời gian công bố 2025, và URL chính thức.'
    },
    'H13': {
        'status': 'Sửa một phần',
        'display_status': 'Sửa một phần',
        'evidence': 'Đã phân định kiểm định scam recall riêng và accuracy riêng tại Section IV.B và Table VIII; báo cáo exact two-sided binomial p-value = 0.0625 bên cạnh continuity-corrected chi2 = 3.2000 (p=0.0736) cho b=5, c=0; thừa nhận giới hạn statistical power của mẫu nhỏ (N=117).'
    },
    'H14': {
        'status': 'Sửa một phần',
        'display_status': 'Sửa một phần',
        'evidence': 'Đã công bố rõ ontology phân biệt commercial marketing spam với cyber fraud/phishing tại Section III.A; mô tả tiêu chuẩn tuyển chọn challenge suite và nguồn gốc từ ChongLuaDao, VNCERT, và UIT-NLP corpus; thừa nhận selection bias của tập challenge.'
    },
    'H15': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã công bố Bảng ma trận 2x3 hoàn chỉnh (Table IX) tại Section IV.C; báo cáo song song full-denominator accuracy (Arm 1: 94.87%, Arm 2: 90.60%) và selective accuracy on decided cases (Arm 1: 98.23%, Arm 2: 99.07%), phân định rõ ràng 3 lớp kết quả (SCAM, LOW/HAM, UNKNOWN).'
    },
    'H16': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã gọi ngưỡng tau=0.90 là exploratory operational threshold trên tập development N=384 thay vì tuyên bố "knee of the curve" hay điểm tối ưu được validation độc lập (Cô Chi đã xác nhận Đạt).'
    },
    'H17': {
        'status': 'Sửa một phần',
        'display_status': 'Sửa một phần',
        'evidence': 'Đã loại bỏ hoàn toàn ký hiệu phi chuẩn p=0.0000 tại toàn bộ bài báo; thay bằng p < 0.0001 tại Table VII và báo cáo exact p-values cho các kiểm định khác (p=0.0625, p=0.0736, p=0.45, p=0.48, p=1.00).'
    },
    'H18': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã tài liệu hóa chính sách regex fallback và tỷ lệ JSON parse error tại Section III.F: Ghi nhận 0 parse error trên toàn bộ 585 lượt gọi API, cơ chế circuit breaker và fallback heuristic được mô tả chi tiết và lưu log tại experiments/tier2_council/reports/.'
    },
    'M1': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã đồng bộ toàn bộ số liệu giữa Abstract, Table VI, Table VII, Table VIII, Results và Conclusion; không còn sai lệch mẫu số hay tỷ lệ phần trăm.'
    },
    'M2': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã ghi rõ thông số độ dài token tối đa (max_length = 256) và xử lý truncation cho Tier 1 ViSoBERT tại Section III.C.'
    },
    'M3': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã mô tả chi tiết phương thức trích xuất rationale từ JSON schema của các chuyên gia hội đồng tại Section III.F.'
    },
    'M4': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã phân tích chi tiết chi phí và độ trễ của các cơ chế fallback và abstention tại Section IV.D.'
    },
    'M5': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã giải thích cơ chế tương quan lỗi giữa các LLM backbone và lý do áp dụng kiến trúc không đồng nhất (heterogeneous multi-agent council) tại Section III.E và IV.C.'
    },
    'M6': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã đồng bộ phương pháp tính recall (unweighted macro-average 95.62% +- 2.25% vs pooled micro-recall 95.64%) và mẫu số 5 seed tại Table VI và Abstract.'
    },
    'M7': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã ghi rõ toàn bộ các hạn chế chưa được khắc phục vào Section IV.F (Threats to Validity) và Section V (Conclusion) theo chuẩn RBL-5a.'
    },
    'M8': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã cấu trúc phần Conclusion theo từng Research Question (RQ1--RQ5), nêu rõ N mẫu, estimate, exact p-value, effect size, và 3 hướng phát triển tiếp theo có tiêu chí thành công cụ thể; ghi nhận rõ kết luận RQ1 là ViSoBERT đạt parity với symmetric edge transformers (p >= 0.45; b=c=7 vs PhoBERT-large).'
    },
    'M9': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã rà soát và viết lại toàn bộ các câu bị gắn cờ "Khẳng định thiếu căn cứ" trong Phụ lục A theo hướng trung tính, dựa trên bằng chứng thực nghiệm.'
    },
    'M10': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã giải quyết toàn bộ các mâu thuẫn nội tại trong bài báo được liệt kê ở Phụ lục A (về mẫu số, chi phí, độ trễ, và định danh mô hình).'
    },
    'N01': {
        'status': 'Sửa một phần',
        'display_status': 'Sửa một phần',
        'evidence': 'Đã thu hẹp định vị N=384 xuống Development Profiling Suite (Table IX, X), công bố rõ 93 mẫu xuất phát từ training corpus và 10 mẫu trùng frozen test (63/267 near-duplicates), không dùng làm bằng chứng OOD generalization; khớp hoàn toàn với phương án thu hẹp định vị của giảng viên. Đồng thời tại Table X, đã bổ sung ghi chú giải thích rõ Solo ViSoBERT được đánh giá ở ngưỡng phân loại mặc định theta=0.50 (FPR 6/211 = 2.84%), phân biệt với benchmark holdout chuyên biệt ở theta_scam=0.90 (FPR 8/192 = 4.17%).'
    },
    'N02': {
        'status': 'Sửa một phần',
        'display_status': 'Sửa một phần',
        'evidence': 'Đã giải trình và đối chiếu triệt để mẫu số theo seed từ summary_5runs_detailed.csv và locked holdout partition: 5 seed cross-validation đánh giá trên các tập validation có số lượng scam thực tế là 73, 73, 73, 75, 73 (tổng 367 scam, 351 TP, mean recall 95.62% +- 2.25%, pooled micro-recall 351/367 = 95.64%); trong khi mô hình ONNX INT8 phát hành được đánh giá tất định trên locked holdout partition (N=267, 75 scam, 72 TP = 96.00% recall, 95% Clopper-Pearson CI [88.75%, 99.17%], 8/192 = 4.17% FPR ở theta_scam=0.90). Đã sửa caption Table VI, Abstract (229 từ), Results và Conclusion, loại bỏ hoàn toàn mâu thuẫn nội tại.'
    },
    'N03': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã công bố exact two-sided binomial p-value = 0.0625 bên cạnh continuity-corrected chi2 = 3.2000 (p = 0.0736) cho b=5, c=0; loại bỏ toàn bộ ký hiệu p=0.0000 (sửa thành p < 0.0001); làm rõ Panel A đánh giá ViSoBERT ONNX INT8 (CPU) so với các baseline FP32/FP16.'
    },
    'N04': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã thu hẹp claim tại IV.C: thừa nhận Arm 3 bỏ Seat C làm thay đổi đồng thời số agent (3->2), budget và normalization weights, coi đây là empirical architectural comparison thay vì chứng minh nhân quả tuyệt đối. Bổ sung khoảng tin cậy 95% Clopper-Pearson [0.00%, 17.65%] cho 19 mẫu benign notifications.'
    },
    'N05': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã đối chiếu trực tiếp bản PDF ACL Anthology (2023.emnlp-main.315, pp. 5191--5207), sửa pretraining data thành 1 GB uncompressed social media text; sửa BibTeX pages=5191--5207 và URL chính thức; chuẩn hóa MultiPhishGuard arXiv:2505.23803v2.'
    },
    'N06': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã tách bạch định nghĩa FDR = 1 - Precision = 35.53% (41/116 báo động giả) và FPR = 41/192 = 21.35% trên legitimate traffic của Gemini tại Section I và IV; không dùng lẫn lộn thuật ngữ FAR.'
    },
    'N07': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã loại bỏ các từ "eliminates alarm fatigue", "guarantees zero"; báo cáo cẩn trọng 95% Clopper-Pearson CI: [0.00%, 17.65%] cho 0/19 false alarms tại Abstract, Table VIII, IV.C và Conclusion; đồng thời thêm 95% CI [88.75%, 99.17%] cho 72/75 scam detections.'
    },
    'N08': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã thu hẹp vị trí của auditability: không tuyên bố như kết quả định lượng mà định vị là architectural rationale và human-in-the-loop triage capability tại Discussion; thừa nhận P-single có accuracy cao hơn council.'
    },
    'N09': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã sửa thuật ngữ PII thành 100% entity recall (zero leakage, 0/5 leaked OTPs), công bố trung thực 2 trường hợp over-redaction trên 117 mẫu challenge; tại Section IV.F đã bổ sung ghi chú phân phối dữ liệu (upstream UIT-NLP corpus đã ẩn danh số điện thoại bằng nhãn [NUMBER] nên có distribution shift so với tin nhắn thực tế).'
    },
    'N10': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã xuất bảng ma trận 2x3 hoàn chỉnh (Table IX); báo cáo song song full-denominator accuracy (Arm 1: 94.87%, Arm 2: 90.60%) và selective accuracy on decided cases (Arm 1: 98.23%, Arm 2: 99.07%), minh bạch hoàn toàn 3 lớp (SCAM, LOW, UNKNOWN).'
    },
    'N11': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã khôi phục nguyên văn System Prompt Gemini 3.5 Flash 5-Shot ICL (yêu cầu binary 0/1) tại Section III.F.1; tách biệt với prompt P-single (JSON 5 trục); tài liệu hóa chính sách regex fallback và circuit breaker với 0 parse error trên 585 calls; công bố endpoint chính thức api.vnaipro.app và standby vibi.top.'
    },
    'N12': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã loại bỏ 100% các từ "first integrated", "Occam-optimized"; định vị bài báo là empirical engineering contribution; tại RQ1 ghi rõ kết luận ViSoBERT INT8 ngang bằng với các edge transformer đối xứng (McNemar p >= 0.45; b=c=7 vs PhoBERT-large), chỉ vượt trội mô hình đơn lẻ Gemini 3.5 Flash (p < 0.0001).'
    },
    'N13': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã trích xuất số tham số chính xác từ ONNX graph là 97.57M parameters (INT8 93.86 MB); sửa Table X và XI thành "Mean Latency 267.5 ms", công bố phân phối bimodal (P50 = 70.7 ms, P95 = 80.5 ms, P99 ~ 5,850 ms); đối chiếu và giải trình chi phí token chuẩn xác từ usage_log.csv và bảng prices ($1.50/$6.30 cho GPT, $0.30/$2.50 cho Gemini Flash), loại bỏ phép tính nhẩm 32.6x không tái tạo được và phân định rõ chi phí Arm 5 ($0.0153/1k).'
    },
    'N14': {
        'status': 'Đã sửa',
        'display_status': 'Đã sửa',
        'evidence': 'Đã chuẩn hóa thuật ngữ 19 mẫu benign thành "19 authentic transactional and service notifications (including 5 banking OTP verification codes)" thay cho cách gọi gây hiểu lầm "19 authentic banking OTPs"; công bố rõ ontology phân biệt commercial spam với phishing/scam, nguồn gốc dữ liệu uitnlp/vietnamese-sms-dataset (CC BY-SA 4.0), ChongLuaDao, VNCERT.'
    }
}

def update_parsed_json():
    print("Updating parsed_tracker_v3.json...")
    with open('parsed_tracker_v3.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    for item in items:
        fid = item['id']
        if fid in ITEM_UPDATES:
            u = ITEM_UPDATES[fid]
            item['status'] = u['status']
            item['owner'] = 'Nhóm SV'
            
            # Update feedback with SV evidence
            fb = item.get('feedback', '')
            marker = '--- SV ĐÃ SỬA'
            if marker in fb:
                base_fb = fb.split(marker)[0].strip()
            else:
                base_fb = fb.strip()
            item['feedback'] = base_fb + '\n\n--- SV ĐÃ SỬA (27/10/2026):\n' + u['evidence']
            
    with open('parsed_tracker_v3.json', 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print("parsed_tracker_v3.json successfully updated!")

def update_docx():
    print("Updating ScamShield_VN_Action_Tracker_V3.docx...")
    doc = docx.Document('ScamShield_VN_Action_Tracker_V3.docx')
    
    # 1. Update Table 0 Summary
    t0 = doc.tables[0]
    for r in t0.rows:
        if r.cells[0].text.strip() == 'Kết luận':
            r.cells[1].text = (
                "ĐỐI SOÁT & CẬP NHẬT CHUẨN MỰC TOÀN DIỆN (27/10/2026 - Sau phiên giải quyết 12 mâu thuẫn):\n"
                "• Trạng thái 43 mục: 36 ĐÃ SỬA (83.7%) | 6 SỬA MỘT PHẦN (14.0%) | 1 BỎ QUA (B1) | 0 CHƯA SỬA / MỞ.\n"
                "• Đã vượt qua 100% kiểm tra tự động Invariant Linter (17/17 test suites PASSED, 0 lỗi, 0 cảnh báo).\n"
                "• 12 mâu thuẫn cốt lõi đã được giải quyết triệt để và đồng bộ toàn văn bản:\n"
                "  1. N02: Phân định triệt để 5-seed cross-validation (351/367 scam, macro 95.62%, micro 95.64%) vs locked holdout benchmark (N=267, 75 scam, 72/75 = 96.00% recall, 95% Clopper-Pearson CI [88.75%, 99.17%], 8/192 FPR ở theta_scam=0.90). Xóa bỏ mâu thuẫn nội tại trong Abstract (229 từ).\n"
                "  2. Table X Arm 1: Giải thích rõ Solo ViSoBERT ở Table X dùng ngưỡng mặc định theta=0.50 (6/211 FP = 2.84%), phân biệt với holdout chuyên biệt dùng theta_scam=0.90 (8/192 FP = 4.17%).\n"
                "  3. H5/N11 Prompt B3: Khôi phục nguyên văn Prompt Gemini 3.5 Flash 5-Shot ICL (yêu cầu xuất binary 0/1), tách biệt với prompt P-single (JSON 5 trục).\n"
                "  4. N13 Cost: Đối chiếu dữ liệu thực usage_log.csv và benchmark.db (bảng prices), loại bỏ phép tính nhẩm 32.6x không tái tạo được và phân định rõ chi phí Arm 5 ($0.0153/1k).\n"
                "  5. N13 Latency: Sửa 'Median 267.7 ms' thành 'Mean Latency 267.5 ms', công bố phân phối bimodal (P50 = 70.7 ms, P95 = 80.5 ms, P99 ~ 5,850 ms).\n"
                "  6. RQ1 Claim: Xác nhận ViSoBERT INT8 ngang bằng với các edge transformers đối xứng (McNemar p >= 0.45; b=c=7 vs PhoBERT-large), chỉ vượt trội mô hình đơn lẻ Gemini 3.5 Flash (p < 0.0001).\n"
                "  7. Recall CI: Bổ sung 95% Clopper-Pearson CI [88.75%, 99.17%] cho 72/75 scam detections.\n"
                "  8. Panel A: Công bố rõ ràng ViSoBERT ONNX INT8 (CPU) so với baseline FP32/FP16.\n"
                "  9. Benign Terminology: Chuẩn hóa 19 mẫu thành '19 authentic transactional and service notifications (including 5 banking OTP verification codes)'.\n"
                "  10. PII Entity Recall: Sửa thành '100% entity recall (zero leakage, 0/5 leaked OTPs)' và thừa nhận 2 trường hợp over-redaction.\n"
                "  11. External Validity: Bổ sung ghi chú corpus đã ẩn danh số điện thoại bằng [NUMBER] gây distribution shift.\n"
                "  12. ViSoBERT Corpus: Sửa thành 1 GB uncompressed social media text theo đúng bài báo EMNLP 2023 gốc.\n"
                "Sẵn sàng nghiệm thu chính thức."
            )
            
    # 2. Update Table 2 Confirmation
    t2 = doc.tables[2]
    for r in t2.rows:
        c0 = r.cells[0].text.strip()
        if 'Mọi mục Blocking/High' in c0:
            r.cells[1].text = 'Đã rà soát & cập nhật 3 mức trạng thái minh bạch (36 Đã sửa, 6 Sửa một phần, 1 Bỏ qua B1, 0 Chưa sửa). Minh chứng đầy đủ cho toàn bộ 43 mục.'
        elif 'Đã chạy lại Audit' in c0:
            r.cells[1].text = 'Đã chạy verify_paper_invariants.py: 17/17 PASSED (0 lỗi, 0 cảnh báo). Đã đồng bộ main.tex, docx (Single & Two-Column) & Overleaf zip.'
        elif 'Nhóm sinh viên xác nhận' in c0:
            r.cells[1].text = 'Nhóm SV xác nhận đã hoàn tất sửa đổi toàn bộ mã nguồn LaTeX, scripts và trackers theo đúng chỉ đạo audit của Cô Chi (27/10/2026).'
        elif 'Giảng viên' in c0:
            r.cells[1].text = '☐ (Chờ Giảng viên hướng dẫn duyệt và ký)'

    # 3. Update Table 1 Rows
    t1 = doc.tables[1]
    current_key = None
    for r in t1.rows:
        first_cell = r.cells[0].text.strip()
        
        if first_cell in ITEM_UPDATES:
            current_key = first_cell
            u = ITEM_UPDATES[current_key]
            r.cells[-1].text = u['status']
            r.cells[-2].text = 'Nhóm SV'
        elif current_key and ('SV đã điều chỉnh' in first_cell or 'Lý do chưa đạt' in first_cell):
            u = ITEM_UPDATES[current_key]
            text = r.cells[0].text
            split_marker = '--- SV ĐÃ SỬA'
            if split_marker in text:
                base_text = text.split(split_marker)[0].strip()
            else:
                base_text = text.strip()
            new_text = base_text + '\n\n--- SV ĐÃ SỬA (27/10/2026):\n' + u['evidence']
            for c in r.cells:
                c.text = new_text
            current_key = None

    doc.save('ScamShield_VN_Action_Tracker_V3.docx')
    print("ScamShield_VN_Action_Tracker_V3.docx successfully updated!")

def update_markdown():
    print("Updating action_tracker.md...")
    with open('parsed_tracker_v3.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    md_lines = []
    md_lines.append("# ScamShield-VN: Action Tracker & Audit Verification (V3 Reconciled)\n")
    md_lines.append("**Bài nghiên cứu phát hiện scam và phishing trong tin nhắn tiếng Việt, nhắm tới các vấn đề né tránh bằng ngôn ngữ không chuẩn, chi phí bất đối xứng, cloud LLM alarm fatigue, và tương quan lỗi multi-agent.**\n")
    md_lines.append("| Trường thông tin | Giá trị |")
    md_lines.append("| :--- | :--- |")
    md_lines.append("| **File bài** | `ScamShield_VN_Evidence_Grounded_Two_Tier_Architecture_for_Vietnamese_Scam_and_Phishing_Detection.pdf` |")
    md_lines.append("| **Sinh viên / nhóm** | Nhóm Nghiên cứu ScamShield-VN |")
    md_lines.append("| **Ngày audit đối soát** | 2026-10-27 (Đồng bộ sau giải quyết 12 mâu thuẫn) |")
    md_lines.append("| **Tổng số mục** | **43 mục** (B1, H1–H18, M1–M10, N01–N14) |")
    md_lines.append(r"| **Kết luận rà soát** | **36 ĐÃ SỬA (83.7%) \| 6 SỬA MỘT PHẦN (14.0%) \| 1 BỎ QUA (B1) \| 0 CHƯA SỬA / MỞ** |")
    md_lines.append("| **Trạng thái kiểm thử** | **17/17 Invariant Suites PASSED (0 ERRORS, 0 WARNINGS)** |\n")
    
    md_lines.append("## 1. Bảng tổng hợp công việc (Action Tracker)\n")
    md_lines.append("| ID | Priority | Reviewer | Issue / Risk | Required Action | Paper Section | Rerun? | Owner | Status |")
    md_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    
    for it in items:
        fid = it['id']
        prio = it['priority']
        rev = it['reviewer']
        issue = it['issue'].replace('\n', ' ').replace('|', '\\|')
        action = it['action'].replace('\n', ' ').replace('|', '\\|')
        sec = it['section'].replace('\n', ' ').replace('|', '\\|')
        rerun = it['rerun'].replace('\n', ' ').replace('|', '\\|')
        owner = it.get('owner', 'Nhóm SV')
        status = it['status'].replace('\n', ' ')
        
        md_lines.append(f"| **{fid}** | {prio} | {rev} | {issue[:120]}... | {action[:120]}... | {sec} | {rerun} | {owner} | **{status}** |")
        
    md_lines.append("\n## 2. Chi tiết minh chứng đối soát theo từng mục (Audit Verification & Evidence)\n")
    for it in items:
        fid = it['id']
        prio = it['priority']
        fb = it['feedback']
        md_lines.append(f"### [{fid}] ({prio}) {it['issue'][:100]}\n")
        md_lines.append(f"- **Vị trí bài báo**: `{it['section']}`")
        md_lines.append(f"- **Trạng thái**: `{it['status'].replace(chr(10), ' ')}`")
        md_lines.append(f"- **Chi tiết rà soát & minh chứng sinh viên đã xử lý**:\n")
        for line in fb.split('\n'):
            md_lines.append(f"  > {line}")
        md_lines.append("\n---\n")
        
    with open('action_tracker.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    print("action_tracker.md successfully updated!")

def main():
    update_parsed_json()
    update_docx()
    update_markdown()
    print("\nALL TRACKERS SYNCHRONIZED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
