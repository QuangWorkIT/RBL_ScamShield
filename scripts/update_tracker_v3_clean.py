# -*- coding: utf-8 -*-
import docx
import sys

def main():
    print("=== UPDATING ACTION TRACKER V3 WITH 3-TIER STATUS & EXACT EVIDENCE ===")
    doc = docx.Document('ScamShield_VN_Action_Tracker_V3.docx')

    # 1. Update Table 0 (Summary)
    t0 = doc.tables[0]
    for r in t0.rows:
        if r.cells[0].text.strip() == 'Kết luận':
            r.cells[1].text = (
                "ĐỐI SOÁT & CẬP NHẬT CHUẨN MỰC (27/10/2026): "
                "Đã cập nhật minh bạch 3 mức trạng thái (Đã sửa: 22 mục / Sửa một phần: 6 mục / Chưa sửa: 0 mục / Bỏ qua: 1 mục B1). "
                "Đã hoàn thành sửa toàn diện mã nguồn LaTeX (Sections 00--06, References.bib, và main.tex) vượt qua 100% kiểm thử tự động invariant linter (0 lỗi tồn đọng). "
                "Rút bỏ toàn bộ các claim vô căn cứ (causally necessary, strictly necessary, Occam, first integrated, 60GB, 0.0000, 35.53%). "
                "Bổ sung bảng ma trận 2x3 (Table IX), 95% Clopper-Pearson CI [0.00%, 17.65%], exact p=0.0625, 97.57M params, INT8 93.86 MB, "
                "sửa chi phí Arm 5 thành $0.0153/1k, và chuẩn hóa metadata BibTeX ViSoBERT (ACL Anthology) và MultiPhishGuard (arXiv). "
                "Các mục liên quan đến tính chất không hoàn toàn disjoint của Combined Suite (10 duplicate texts, 99 training payloads) "
                "và mẫu số 5-seed cross-validation được phân loại trung thực là 'Sửa một phần' kèm disclosure hạn chế đầy đủ trong bài. "
                "Chờ Giảng viên đánh giá và nghiệm thu."
            )

    # 2. Update Table 2 (Confirmation)
    t2 = doc.tables[2]
    for r in t2.rows:
        c0 = r.cells[0].text.strip()
        if 'Mọi mục Blocking/High' in c0:
            r.cells[1].text = 'Đã rà soát & cập nhật 3 mức trạng thái minh bạch (22 Đã sửa, 6 Sửa một phần, B1 bỏ qua). Không tự nhận hoàn tất tuyệt đối.'
        elif 'Đã chạy lại Audit' in c0:
            r.cells[1].text = 'Đã chạy verify_paper_invariants.py: 100% PASSED (0 lỗi tồn đọng). Đã đồng bộ main.tex & Overleaf zip.'
        elif 'Nhóm sinh viên xác nhận' in c0:
            r.cells[1].text = 'Nhóm SV xác nhận đã hoàn thành sửa mã nguồn LaTeX theo đúng audit của Cô Chi (27/10/2026).'
        elif 'Giảng viên' in c0:
            r.cells[1].text = '☐ (Chờ Giảng viên hướng dẫn duyệt và ký)'

    # 3. Item Evidence & Status Mapping
    # Dictionary of exact evidence matching the "Minh chứng để xác nhận đạt" column
    updates = {
        'H1': (
            'Đã sửa',
            'Đã sửa: Đã xóa bỏ hoàn toàn các tuyên bố nhân quả tuyệt đối ("strictly necessary", "causally necessary") tại Section IV.C (dòng 121) và Section V (RQ3). Đã thừa nhận rõ hạn chế Arm 3 bị giảm từ 3 xuống 2 ghế (confounder) nên không thể quy riêng cho Public Defender. Đã bổ sung Bảng ma trận 2x3 (Table IX) công bố đầy đủ True Scam (N=98), True Ham (N=19), phân định UNKNOWN, và 95% Clopper-Pearson CI [0.00%, 17.65%] trên 19 mẫu benign.'
        ),
        'H2': (
            'Đã sửa',
            'Đã sửa: Đã công bố tại Section IV.G (Threats to Validity, Internal Validity): Thống kê 3-run variance trên 1,404 quyết định consensus với label agreement 100.00% (flip rate 0.00%), độ trễ SD = +-32.8 ms (Gemini) và +-92.0 ms (GPT-6.1-sol); nêu rõ không có bảo đảm tất định bitwise trên cloud hosted APIs do dynamic batching và speculative decoding.'
        ),
        'H3': (
            'Đã sửa',
            'Đã sửa: Đã công bố tại Section III.A, Section IV.G và Section V: Cohen\'s kappa=0.88 không tái tính được từ repo và là nhãn chưa được kiểm chứng độc lập. (Cô Chi đã xác nhận Đạt).'
        ),
        'H4': (
            'Đã sửa',
            'Đã sửa: Đã bổ sung tại Section III.E (Table V - Model Card) và Section VI (Reproducibility): Công bố rõ ràng endpoint chính thức https://api.vnaipro.app/v1, standby https://vibi.top/v1, model snapshots (gpt-6.1-sol-2026-03, gemini-3.5-flash-lite), ngày truy cập (2026-10-20), nhiệt độ (T=0.1 / T=0.0), và lưu trữ toàn bộ raw JSON responses cùng telemetry log tại experiments/tier2_council/reports/.'
        ),
        'H5': (
            'Đã sửa',
            'Đã sửa: Đã công bố nguyên văn System Prompt Gemini cùng 5 exemplars tại Section III.F, mô tả chi tiết structured forensic schema (P-single) và specialist role instructions, kèm đường dẫn commit mã nguồn bất biến tại pipeline/forensic_council.py và experiments/tier2_council/data/tasks/.'
        ),
        'H6': (
            'Sửa một phần',
            'Sửa một phần: Đã công bố chi tiết Bảng Table III và Table IV (Partition Overlap Matrix): Frozen test có 0 exact overlap nhưng có 63/267 near-duplicates với train; Challenge Suite (N=117) có 10 văn bản trùng exact với frozen test và 99 mẫu từ training split; giải trình rõ nguy cơ data leakage qua Tier 1 trong Section IV.G (Construct Validity) và rút tên thành "Exploratory Development Suite" (N=384).'
        ),
        'H7': (
            'Đã sửa',
            'Đã sửa: Fig. 1 (pipeline_architecture.png) và caption chi tiết tại Section III: Thể hiện rõ ràng ranh giới phân vùng (corpus vs feeds), Tier 1 edge screening, confidence threshold routing (tau=0.90), module PII Sanitizer client-side, hội đồng 3-agent, và standardized 3-label output (SCAM-RISK, LOW-RISK, UNKNOWN).'
        ),
        'H8': (
            'Đã sửa',
            'Đã sửa: Đã bổ sung trích dẫn và thảo luận Cost-Sensitive BERT (Madabushi et al., NLP4IF 2019, trang 125--134) tại Section II.B; scikit-learn v1.9.1 (Pedregosa et al.) và ONNX Runtime v1.31.0 tại Section III.H và Section VI; Edwards continuity correction (1948) tại Section III.H. Toàn bộ metadata BibTeX đã được xác minh chính xác từ nguồn gốc.'
        ),
        'H9': (
            'Đã sửa',
            'Đã sửa: Đã công bố tại Section IV.B (Table VIII & text) và Abstract: P-single đạt accuracy 96.58% với chi phí rẻ hơn 10 lần ($0.0450/1k), nêu rõ giá trị của council là auditable multi-perspective reasoning và cautious abstention chứ không phải standalone accuracy. (Cô Chi đã xác nhận Đạt).'
        ),
        'H10': (
            'Đã sửa',
            'Đã sửa: Đã công bố đồng bộ tại Abstract, Section IV.B, Section V: Hội đồng 3-agent tiết kiệm 40% chi phí nhưng Scam Recall giảm 5.10 điểm phần trăm (93.88% -> 88.78%, paired asymptotic 95% CI: [-9.46%, -0.75%]) và UNKNOWN tăng từ 4 lên 10. (Cô Chi đã xác nhận Đạt).'
        ),
        'H11': (
            'Đã sửa',
            'Đã sửa: Bảng Table II (Novelty Matrix) đã phân định rõ phần kế thừa (Inherited) và phần đóng góp kỹ thuật (Modified / Synthesized); Section II.D phân tích định lý Condorcet là động lực thiết kế lý thuyết (theoretical motivation) và chỉ ra sự sụp đổ khi có correlated errors (Kim et al., 2025; Smit et al., 2024); đã loại bỏ hoàn toàn các từ "first integrated" và "Occam-optimized".'
        ),
        'H12': (
            'Đã sửa',
            'Đã sửa: Đã sửa chính xác metadata BibTeX của MultiPhishGuard (arXiv:2505.23803: tác giả Yi-Nuo Xue, Eric Spero, Yun Sing Koh, Giovanni Russello); phân tích so sánh 4 điểm khác biệt cốt lõi của ScamShield-VN so với MultiPhishGuard tại Section II.D; xóa bỏ hoàn toàn con số sai 60 GB khỏi Section II.B và Section IV.F.'
        ),
        'H13': (
            'Sửa một phần',
            'Sửa một phần: Đã chuẩn hóa Section I.B (RQ1--RQ5) gắn với outcome metric, H0/H1 marginal homogeneity, statistical test; đã xóa bỏ các từ "pre-specified / prevent HARKing" tránh gây phản cảm khi RQ bổ sung sau audit; đã làm rõ RQ1 kiểm định overall paired classification correctness trên các cặp discordant thay vì chỉ cô lập recall.'
        ),
        'H14': (
            'Sửa một phần',
            'Sửa một phần: Đã công bố chi tiết tại Section III.A (Table III & paragraph) và Section IV.G: Challenge suite gồm 109 mẫu corpus (99 train, 10 frozen) + 8 external feeds; giải trình rõ Tier 1 fine-tuned trên train nên Combined Suite mang tính chất exploratory development benchmark; thừa nhận hạn chế này trong Threats to Validity.'
        ),
        'H15': (
            'Đã sửa',
            'Đã sửa: Đã sửa tiêu đề cột Table VI thành Scam-F1 (%) và ghi chú rõ unweighted Macro-F1 (94.51% +- 0.96%); Table VIII đã sửa Scam-F1 và Macro-F1 riêng biệt (Arm 1 Macro-F1 91.60%, Arm 2 Macro-F1 85.80%, P-single 94.20%); Abstract và Conclusion đã đồng bộ chuẩn xác.'
        ),
        'H16': (
            'Đã sửa',
            'Đã sửa: Section I, Section III, Section IV.D và Section V đều gọi tau in [0.70, 0.95] là exploratory operating-point sensitivity profiling trên reporting suite chứ không phải externally validated global optimum. (Cô Chi đã xác nhận Đạt).'
        ),
        'H17': (
            'Sửa một phần',
            'Sửa một phần: Đã công bố tại Section IV.B, Section IV.G và Section V: Thừa nhận paired test có b+c=5 có công suất thống kê thấp (low power), không đủ bằng chứng để khẳng định equivalence; đã bỏ toàn bộ các khẳng định "tuân thủ hoàn toàn Điều 25 Nghị định 13", chỉ nêu đây là kiến trúc kỹ thuật hỗ trợ quyền riêng tư và cần đánh giá pháp lý riêng biệt.'
        ),
        'H18': (
            'Đã sửa',
            'Đã sửa: Đã có Model Card chi tiết (Table V), Hình kiến trúc hệ thống (Fig. 1), công bố Cohen\'s kappa=0.88 unverified, công bố rõ ràng cơ chế timeout và fallback tại Section III.F.'
        ),
        'M1': (
            'Đã sửa',
            'Đã sửa: Table V phân loại rõ ràng các model thực chạy benchmark (ViSoBERT, PhoBERT, ViBERT, Gemini 3.5 Flash, GPT-6.1-sol) với đầy đủ endpoint, access date, temperature; các model khác (Zhou et al., Banda et al.) được định vị rõ ở Table I là số liệu trích dẫn từ công trình gốc.'
        ),
        'M2': (
            'Đã sửa',
            'Đã sửa: Section III.A đã công bố URL nguồn và giấy phép (uitnlp: CC BY-SA 4.0, phishing_sample_300: ODC-By); mô tả chuẩn hóa NFC, loại bỏ zero-width characters, giải trình 34 duplicate keys do collision ID của 2 upstream feeds và công bố manifest deduplicated độc lập.'
        ),
        'M3': (
            'Đã sửa',
            'Đã sửa: Section III.F đã tài liệu hóa timeout (30 s per call), exponential backoff (1 s, 2 s, 4 s, max 3 retries), fallback schema, và ghi nhận tỷ lệ lỗi phân tích cú pháp (parse error: 0% trên structured output).'
        ),
        'M4': (
            'Đã sửa',
            'Đã sửa: Section III.H và Section IV.D đã phân định rạch ròi đơn vị và phương pháp: Phân định Mean latency (267.5 ms) và Median latency (267.7 ms), độ trễ edge đo trên CPU ONNX INT8 (70.7 ms median, 70.72 ms mean, 80.48 ms P95); công thức paired McNemar chi2_cont = (|b-c|-1)^2/(b+c) và exact binomial test.'
        ),
        'M5': (
            'Đã sửa',
            'Đã sửa: Toàn bộ các claim đã được rà soát và thu hẹp: Xóa bỏ hoàn toàn "first integrated", "Occam-optimized", "strictly necessary", "causally necessary"; mọi số liệu đều có bảng chứng minh kèm integer sample count.'
        ),
        'M6': (
            'Đã sửa',
            'Đã sửa: Section IV tổ chức mạch lạc theo 5 RQ; ghi rõ attempted N=267, analyzed N=267 (zero exclusion) ở Table VI; attempted N=117, analyzed N=117 ở Table VII & IX; attempted N=384, analyzed N=384 ở Table X.'
        ),
        'M7': (
            'Đã sửa',
            'Đã sửa: Section IV.G (Threats to Validity) đã công bố toàn bộ 4 góc hạn chế: Internal (hosted nondeterminism, variance), External (tiếng Việt, chưa kiểm định pháp lý), Construct (overlap 63 near-dup, 10 duplicate strings, kappa unverified, tau exploratory), Conclusion (low power b+c=5).'
        ),
        'M8': (
            'Đã sửa',
            'Đã sửa: Table VII đã công bố chi phí tính toán độc lập cho từng arm: Arm 1 ($0.7500/1k), Arm 2 ($0.4500/1k), Arm 3 ($0.3000/1k), P-single ($0.0450/1k); Table X sửa chi phí Arm 5 thành $0.0153/1k theo đúng tỷ lệ escalation 3.4% x $0.4500.'
        ),
        'M9': (
            'Đã sửa',
            'Đã sửa: Section III.G và Table IX đã mô tả chi tiết giao thức 3 nhãn: UNKNOWN được kích hoạt khi consensus margin < delta_margin hoặc sau khi trừ veto offset mà điểm số nằm trong vùng trung dung [0.40, 0.60]; penalize UNKNOWN như non-positive classification trong conservative evaluation.'
        ),
        'M10': (
            'Đã sửa',
            'Đã sửa: Số tham số đã kiểm tra trực tiếp từ ONNX graph: chính xác 97,566,721 parameters (97.57M params, INT8 size: 93.86 MB); toàn bộ cross-references trong text và các bảng Table I đến Table XI đã được kiểm tra khớp 100%.'
        ),
        'N01': (
            'Sửa một phần',
            'Sửa một phần: Đã đổi tên thành "Combined Exploratory Development Suite" (N=384), công bố tại Table III và Table IV có 10 văn bản trùng exact với frozen test và 99 mẫu lấy từ train split; thừa nhận trong Section IV.G rằng Tier 1 đã fine-tune trên train nên có rủi ro data leakage, không coi đây là benchmark độc lập mà là bài kiểm tra khả năng phối hợp 2 tầng.'
        ),
        'N02': (
            'Sửa một phần',
            'Sửa một phần: Table VI đã đổi cột thành Scam-F1 (%) và ghi rõ unweighted Macro-F1 là 94.51%; note dưới bảng giải trình chi tiết: 5-seed cross-validation có tổng 351 TP trên 367 scam (95.62% +- 2.25% unweighted macro-average, 351/367 = 95.64% pooled micro-recall), trong khi đánh giá trên tập frozen cố định 75 scam đạt recall 72/75 = 96.00%.'
        ),
        'N03': (
            'Đã sửa',
            'Đã sửa: Table VII đã sửa p-value của Gemini từ 0.0000 thành p < 0.001 (p = 3.1 x 10^-8); đã bổ sung hàng kiểm định McNemar Arm 2 vs Arm 1 với exact two-sided binomial p = 0.0625 (b=5, c=0) và Edwards\' corrected chi2_cont = 3.2000 (p approx 0.0736).'
        ),
        'N04': (
            'Đã sửa',
            'Đã sửa: Section IV.C (dòng 121) đã xóa bỏ toàn bộ chữ "strictly necessary", công bố rõ ràng: Arm 3 giảm từ 3 xuống 2 ghế nên việc tăng FPR lên 10.53% bị confounded giữa số lượng agent và vai trò của Public Defender, không thể quy riêng cho Defender.'
        ),
        'N05': (
            'Đã sửa',
            'Đã sửa: Đã xóa sạch 60 GB khỏi Section II.B và Section IV.F (sửa thành 1 GB social media corpus, pp. 5191--5207); cập nhật file paper/references.bib với tác giả chuẩn của ViSoBERT (Nam Nguyen, Thang Phan, Duc-Vu Nguyen, Kiet Nguyen - ACL 2023) và MultiPhishGuard (Yi-Nuo Xue, Eric Spero, Yun Sing Koh, Giovanni Russello - arXiv 2025).'
        ),
        'N06': (
            'Đã sửa',
            'Đã sửa: Section I, Section IV.A và Section IV.F đã sửa chuẩn xác: Gemini 3.5 Flash có FDR = 35.53% (1 - Precision), tương ứng với tỷ lệ báo động giả trên test ngoại suy là 35.34% (41/116) và FPR = 21.35% (41/192) trên 192 mẫu benign của Frozen Test.'
        ),
        'N07': (
            'Đã sửa',
            'Đã sửa: Đã tính toán và bổ sung khoảng tin cậy chính xác hai phía 95% Clopper-Pearson [0.00%, 17.65%] cho 0/19 false alarms tại Abstract, Section I, Table VIII, Table IX (bảng ma trận 2x3), Section IV.C và Section V; không bao giờ tuyên bố "guaranteed zero".'
        ),
        'N08': (
            'Đã sửa',
            'Đã sửa: Section IV.B đã rút bớt nhận định: Thừa nhận P-single đạt accuracy 96.58% cao hơn council, định vị giá trị của council là auditable institutional justification và cautious abstention dưới góc độ kỹ thuật chứ không tự suy ra chất lượng vượt trội.'
        ),
        'N09': (
            'Đã sửa',
            'Đã sửa: Section IV.E (RQ5) và Section V đã bổ sung số liệu thực nghiệm định lượng trên 117 mẫu challenge: Che giấu thành công 5/5 mã OTP (0 false negatives), downstream verdict concordance đạt 100.00% (0/117 label flips), đồng thời thừa nhận hạn chế regex over-redaction trên một số từ ngữ ngữ pháp tiếng Việt.'
        ),
        'N10': (
            'Đã sửa',
            'Đã sửa: Đã chèn Bảng Table IX mới tại Section IV.C: Công bố chi tiết ma trận 2x3 (True Scam N=98: Pred Scam, Pred Ham, Pred UNKNOWN; True Ham N=19: Pred Scam, Pred Ham, Pred UNKNOWN) kèm 95% Clopper-Pearson CI cho FPR trên cả 5 cấu hình.'
        ),
        'N11': (
            'Đã sửa',
            'Đã sửa: Đã cập nhật Section III.F: Công bố rõ ràng structured schema, zero parse error, cơ chế fallback circuit breaker, lưu trữ raw responses tại experiments/tier2_council/reports/.'
        ),
        'N12': (
            'Đã sửa',
            'Đã sửa: Đã xóa sạch 100% các từ "first integrated" và "Occam-optimized" khỏi Abstract, Intro, Related Work, Method, Results và Conclusion; định vị bài báo là empirical engineering contribution.'
        ),
        'N13': (
            'Đã sửa',
            'Đã sửa: Số tham số đã được trích xuất từ ONNX graph: chính xác 97.57M parameters (97,566,721 params, INT8 size: 93.86 MB); Table X sửa độ trễ Arm 1 thành 70.7 ms (CPU INT8 feasibility), sửa chi phí Arm 5 thành $0.0153/1k (3.4% x $0.4500), phân định rõ mean 267.5 ms vs median 267.7 ms.'
        ),
        'N14': (
            'Đã sửa',
            'Đã sửa: Đã sửa tên bộ dữ liệu SMS thành uitnlp/vietnamese-sms-dataset (CC BY-SA 4.0), xóa bỏ hoàn toàn từ nhầm lẫn "UIT-VSMEC" (vốn là tập cảm xúc); công bố rõ ontology phân biệt commercial marketing spam với cyber fraud/phishing.'
        ),
    }

    # 4. Update Table 1 Rows
    t1 = doc.tables[1]
    current_key = None
    for r in t1.rows:
        first_cell = r.cells[0].text.strip()
        
        # Check if row is item header row (e.g. 'H1', 'M2', 'N05')
        if first_cell in updates:
            current_key = first_cell
            status, note = updates[current_key]
            # Column 9 is Status
            r.cells[-1].text = status
        elif current_key and ('SV đã điều chỉnh' in first_cell or 'Lý do chưa đạt' in first_cell):
            # This is the detailed audit row
            status, note = updates[current_key]
            
            # Find if there was already an appended '--- SV ĐÃ SỬA' note
            text = r.cells[0].text
            split_marker = '--- SV ĐÃ SỬA'
            if split_marker in text:
                base_text = text.split(split_marker)[0].strip()
            else:
                base_text = text.strip()
                
            new_text = base_text + '\n\n--- SV ĐÃ SỬA (27/10/2026):\n' + note
            for c in r.cells:
                c.text = new_text
            current_key = None

    doc.save('ScamShield_VN_Action_Tracker_V3.docx')
    print("Successfully updated ScamShield_VN_Action_Tracker_V3.docx with 3-tier status and exact evidence!")

if __name__ == '__main__':
    main()
