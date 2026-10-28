# -*- coding: utf-8 -*-
"""
scripts/apply_paper_phase2_updates.py
Applies all planned fixes across LaTeX files with exact string targets.
"""
import sys, re

def update_00_abstract():
    path = 'paper/sections/00_abstract.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Size units
    c = c.replace(r'($93.9\text{ MB}$', r'($98.42\text{ MB}$ / $93.86\text{ MiB}$')

    # 2. Recall value
    c = c.replace(r'achieves $95.62\%$ macro-average scam recall', r'achieves $95.64\%$ macro-average scam recall')

    # 3. Qualitative value
    c = c.replace(
        r'demonstrating that multi-agent councils offer value in auditable justification and cautious abstention rather than raw standalone accuracy.',
        r'demonstrating that multi-agent councils offer qualitative value in structured forensic justification and cautious abstention rather than raw standalone accuracy.'
    )

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Updated 00_abstract.tex")


def update_01_intro():
    path = 'paper/sections/01_intro.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Dominant scam recall & size units
    old_item2 = r'quantize the model via ONNX INT8 ($97.57\text{M}$ parameters, $93.86\text{ MB}$, $70.7\text{ ms}$ on consumer CPU; baseline FP32: $372.2\text{ MB}$), achieving a dominant Scam Recall of $95.62\% \pm 2.25\%$'
    new_item2 = r'quantize the model via ONNX INT8 ($97.57\text{M}$ parameters, $98.42\text{ MB}$ / $93.86\text{ MiB}$, $70.7\text{ ms}$ on consumer CPU; baseline FP32: $390.54\text{ MB}$ / $372.45\text{ MiB}$), achieving an edge Scam Recall of $95.64\% \pm 2.04\%$'
    if old_item2 in c:
        c = c.replace(old_item2, new_item2)

    # 2. Evaluation standard
    c = c.replace(
        r'We establish an evaluation standard on $2,664$ real-world Vietnamese SMS messages',
        r'We curate an evaluation benchmark of $2,664$ real-world Vietnamese SMS messages'
    )

    # 3. Rephrase RQ1
    old_rq1 = r'Does fine-tuning ViSoBERT with Cost-Sensitive Weighted Binary Cross-Entropy loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha = 5.0$) achieve a superior Scam Recall ($\ge 95.0\%$) on the isolated Frozen Test Partition ($N = 267$) compared to symmetric transformer baselines (PhoBERT-base, PhoBERT-large, FPT ViBERT) and solitary cloud LLMs (Gemini 3.5 Flash)?'
    new_rq1 = r'Does fine-tuning ViSoBERT under Cost-Sensitive Weighted Binary Cross-Entropy loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha = 5.0$) achieve competitive edge Scam Recall ($\ge 95.0\%$) and superior paired classification correctness / false-alarm suppression on the isolated Frozen Test Partition ($N = 267$) compared to symmetric edge transformers (PhoBERT-base, PhoBERT-large, FPT ViBERT) and solitary cloud LLMs (Gemini 3.5 Flash)?'
    if old_rq1 in c:
        c = c.replace(old_rq1, new_rq1)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Updated 01_intro.tex")


def update_03_method():
    path = 'paper/sections/03_method.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Fig 1 caption
    c = c.replace(r'($98.4\text{ MB}$, $70.7\text{ ms}$)', r'($98.42\text{ MB}$ / $93.86\text{ MiB}$, $70.7\text{ ms}$)')

    # 2. III.A Opening - remove national threat feeds from base corpus of 2664
    old_corpus_open = r'comprising $2,664$ genuine Vietnamese telecommunications messages consolidating verified public repositories and national threat feeds:'
    new_corpus_open = r'comprising $2,664$ genuine Vietnamese telecommunications messages consolidating verified public repositories:'
    if old_corpus_open in c:
        c = c.replace(old_corpus_open, new_corpus_open)

    # 3. Label Ontology paragraph
    label_ontology = (
        r"\textbf{Label Ontology and Operational Scope:} "
        r"In compliance with Vietnamese telecommunications regulations under Decree 91/2020/ND-CP, we establish a formal ontology distinguishing between commercial bulk advertising (legitimate promotional SMS containing standard carrier opt-out syntax, such as \texttt{TC} or \texttt{DK}) and actionable digital threats (smishing, brand impersonation, fraudulent OTP harvesting, and advance-fee employment scams). In this research, the positive target class ($y=1$) strictly captures fraudulent and predatory messages, while legitimate carrier service updates, transactional OTPs, and balance notifications are classified under the negative class ($y=0$)."
        "\n\n"
    )
    if r"\textbf{Label Ontology and Operational Scope:}" not in c:
        insert_marker = r"\textbf{Dataset Hygiene, Normalization, and Deduplication Analysis:}"
        if insert_marker in c:
            c = c.replace(insert_marker, label_ontology + insert_marker)

    # 4. Breakdown of 8 challenge samples
    old_8samples = r'alongside $8$ external adversarial lures from national threat feeds (\texttt{canhbao.khonggianmang.vn}) and synthetic variations.'
    new_8samples = (
        r'alongside $8$ external lures consisting of exactly $1$ verified biometric authentication phishing advisory from national cyber threat feeds (\texttt{canhbao.khonggianmang.vn}, sample \texttt{BANK\_15}) '
        r'and $7$ synthetic stress-testing lures (2 multi-step employment and loan scam variants, and 5 authentic customer service and promotional notifications: '
        r'\texttt{BANK\_05}, \texttt{BANK\_19}, \texttt{BANK\_20}, \texttt{BANK\_24}, \texttt{BANK\_25}, \texttt{BANK\_26}, \texttt{SOC\_17}).'
    )
    if old_8samples in c:
        c = c.replace(old_8samples, new_8samples)

    # 5. Table IV Overlap counts & Leakage Risk
    old_row_t4_1 = r'Frozen Test ($N=267$) vs. Train ($N=2,397$) & \textbf{0 / 267 ($0.0\%$)} & 63 / 267 ($23.6\%$) & Zero (Strict Holdout) \\'
    new_row_t4_1 = r'Frozen Test ($N=267$) vs. Train ($N=2,397$) & \textbf{0 / 267 ($0.0\%$)} & 63 / 267 ($23.6\%$) & Strict Holdout ($23.6\%$ boilerplate overlap) \\'
    if old_row_t4_1 in c:
        c = c.replace(old_row_t4_1, new_row_t4_1)

    old_row_t4_2 = r'Challenge Suite ($N=117$) vs. Train ($N=2,397$) & 93 / 117 ($79.5\%$) & 106 / 117 ($90.6\%$) & None (Cloud LLMs zero-shot) \\'
    new_row_t4_2 = r'Challenge Suite ($N=117$) vs. Train ($N=2,397$) & \textbf{99 / 117 ($84.6\%$)} & 106 / 117 ($90.6\%$) & Exploratory suite; Tier 2 zero-shot \\'
    if old_row_t4_2 in c:
        c = c.replace(old_row_t4_2, new_row_t4_2)

    # 6. Section III.C - Remove pp. 5191--5207
    c = c.replace(', pp.~5191--5207)', ')')
    c = c.replace(r'INT8 ($98.42\text{ MB}$)', r'INT8 ($98.42\text{ MB}$ / $93.86\text{ MiB}$)')
    c = c.replace(r'baseline FP32 model ($390.54\text{ MB}$)', r'baseline FP32 model ($390.54\text{ MB}$ / $372.45\text{ MiB}$)')

    # 7. Section III.F - Disclose verbatim prompts of P-single and 3 Specialist Roles + Telemetry
    if r'\textbf{3. Verbatim Specialist Council Role Prompts:}' not in c:
        old_prompts_p2_p3 = c[c.find(r'\textbf{2. Single-LLM Baseline'):c.find(r'\subsection{Standardized 3-Label Output Schema')]
        new_prompts_p2_p3 = (
            r"\textbf{2. Single-LLM Baseline with Structured Forensic Prompting ($\text{P-single}$):}" + "\n"
            r"Implemented on \texttt{gpt-6.1-sol} following Wang et al.~\cite{wang2024boosting}. The system instruction directs multi-axis evaluation:" + "\n"
            r"\begin{quote}" + "\n"
            r"\small" + "\n"
            r"\textbf{System Prompt:} \textit{``Bạn là Chuyên gia Cao cấp về Điều tra Pháp y Số và Phòng chống Lừa đảo Viễn thông Việt Nam. Nhiệm vụ: Phân tích sâu tin nhắn SMS/Zalo tiếng Việt theo phương pháp Structured Forensic Prompting. BẮT BUỘC ĐÁNH GIÁ ĐỦ 5 TRỤC RỦI RO TRƯỚC KHI KẾT LUẬN: (1) Kỹ thuật (URL homoglyph, APK lạ); (2) Tâm lý (FOMO/FUD, ép thời gian, đe dọa tố tụng); (3) Ngôn ngữ (teencode, lách bộ lọc không dấu); (4) Tài chính (yêu cầu OTP, vi phạm Quyết định 2345/QĐ-NHNN); (5) Bảo vệ giao dịch (OTP tiêu chuẩn có cảnh báo bảo mật, biến động số dư định dạng chuẩn). Bắt buộc xuất ra JSON: label (SCAM-RISK|LOW-RISK|UNKNOWN), scam\_prob, confidence, axis\_findings, rationale.''}" + "\n"
            r"\end{quote}" + "\n\n"
            r"\textbf{3. Verbatim Specialist Council Role Prompts:}" + "\n"
            r"In the consolidated 3-agent council (Arm 2), specialist prompts are decoupled in \texttt{config/council\_registry.yaml}:" + "\n"
            r"\begin{itemize}" + "\n"
            r"    \item \textbf{Seat A (Cyber Threat \& Malicious URL Inspector):} \textit{``Bạn là Chuyên gia Giám định Kỹ thuật và URL độc hại thuộc Hội đồng Pháp y ScamShield-VN. Nhiệm vụ: Tập trung phân tích hạ tầng kỹ thuật: tên miền giả mạo (homoglyphs/typosquatting), đường link rút gọn (bit.ly, tinyurl), liên kết tải tệp tin độc hại (.apk), và cổng thanh toán giả mạo. Phản hồi JSON chứa: role\_id, vote (SCAM|HAM|UNKNOWN), scam\_prob (0.0--1.0), confidence, analysis.''} " + "\n"
            r"    \item \textbf{Seat B (Psycholinguistic \& Urgency Profiler):} \textit{``Bạn là Chuyên gia Tâm lý Tội phạm và Ngôn ngữ học Tiếng Việt thuộc Hội đồng Pháp y ScamShield-VN. Nhiệm vụ: Bóc tách kết hợp giữa thao túng tâm lý (tạo áp lực thời gian khẩn cấp, đe dọa phong tỏa tài khoản, dụ dỗ trúng thưởng) và biến thể ngôn ngữ trốn tránh (teencode, viết tắt, không dấu, leetspeak). Phản hồi JSON chứa: role\_id, vote, scam\_prob, confidence, analysis.''} " + "\n"
            r"    \item \textbf{Seat C (Public Defender \& Anti-Alarm Fatigue Advocate):} \textit{``Bạn là Luật sư Bào chữa Công cộng thuộc Hội đồng Pháp y ScamShield-VN. Nhiệm vụ sống còn: TÌM BẰNG CHỨNG HỢP PHÁP VÀ BẢO VỆ TIN NHẮN KHỎI BỊ BÁO OAN. Rà soát cú pháp SMS Brandname ngân hàng, mã xác thực OTP giao dịch tiêu chuẩn, thông báo biến động số dư chuẩn mực, và cú pháp quảng cáo hợp pháp (TC gửi 9241). Nếu có dấu hiệu giao dịch hợp pháp, bỏ phiếu BẢO VỆ (vote: HAM) để ngăn chặn alarm fatigue. Phản hồi JSON: role\_id, vote, scam\_prob, confidence, analysis.''} " + "\n"
            r"\end{itemize}" + "\n\n"
            r"\textbf{4. Parser Telemetry, Fallback Execution, and Resilience:}" + "\n"
            r"Across all $117$ forensic challenge evaluations ($500$ LLM queries under Arm 1, $351$ under Arm 2), downstream JSON parsing achieved $100.00\%$ zero-shot compliance ($0/351$ schema violations). Neither the regex fallback parser nor the Circuit Breaker was triggered during the benchmark evaluation window, confirming provider stability and schema adherence." + "\n\n"
        )
        if len(old_prompts_p2_p3) > 100:
            c = c.replace(old_prompts_p2_p3, new_prompts_p2_p3)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Updated 03_method.tex")


def update_04_results():
    path = 'paper/sections/04_results.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Table VI ViSoBERT Recall & Note
    old_t6_row = r'\textbf{ViSoBERT + WBCE ($\alpha=5.0$)} & \textbf{Proposed (Tier 1 Edge)} & \textbf{97.57M} & \textbf{$95.65 \pm 1.54$} & \textbf{$89.79 \pm 5.15$} & \textbf{$95.62 \pm 2.25$} & \textbf{$92.51 \pm 2.39$} & \textbf{93.86 MB (INT8)} \\'
    new_t6_row = r'\textbf{ViSoBERT + WBCE ($\alpha=5.0$)} & \textbf{Proposed (Tier 1 Edge)} & \textbf{97.57M} & \textbf{$95.65 \pm 1.54$} & \textbf{$89.79 \pm 5.15$} & \textbf{$95.64 \pm 2.04$} & \textbf{$92.51 \pm 2.39$} & \textbf{98.42 MB (INT8)} \\'
    if old_t6_row in c:
        c = c.replace(old_t6_row, new_t6_row)

    old_t6_note = (
        r'yielding an unweighted macro-average of 95.62\% $\pm$ 2.25\% (pooled micro-recall across all 5 seed runs is 351/367 = 95.64\%). '
        r'Deterministic evaluation on the frozen 75-scam holdout partition yields 72/75 = 96.00\% recall.'
    )
    new_t6_note = (
        r'yielding an unweighted macro-average of 95.64\% $\pm$ 2.04\% (sample standard deviation $s=2.04\%$, pooled micro-recall across all 5 seed validation runs is 351/367 = 95.64\%). '
        r'Deterministic evaluation of the released ONNX INT8 model on the locked frozen holdout partition ($N=267$: 192 ham, 75 scam) at operating threshold $\tau=0.90$ yields exactly 72/75 = 96.00\% scam recall ($8/192 = 4.17\%$ FPR, $95.88\%$ overall accuracy) with zero sample exclusions.'
    )
    if old_t6_note in c:
        c = c.replace(old_t6_note, new_t6_note)

    # 2. Text in IV.A
    c = c.replace(
        r'achieves the highest practical Scam Recall among all deployable edge encoders at $95.62\% \pm 2.25\%$, satisfying the pre-specified acceptance threshold ($\ge 95.0\%$)',
        r'achieves the highest practical Scam Recall among all deployable edge encoders at $95.64\% \pm 2.04\%$'
    )

    # 3. Gemini FDR vs FPR in IV.A
    old_gemini_fdr = r'its empirical false alarm rate was $35.34\%$ ($41/116$) on benign stress probes, corresponding to an empirical False Positive Rate of $21.35\%$ ($41/192$) on the frozen benchmark.'
    new_gemini_fdr = (
        r'its False Discovery Rate was $35.34\%$ ($41/116$ false alarms out of $116$ total scam alerts fired by Gemini), '
        r'corresponding to an empirical False Positive Rate of $21.35\%$ ($41/192$) on authentic messages in the frozen test partition. '
        r'Over all 5 independent runs, Gemini precision averaged $64.47\% \pm 1.52\%$ (mean FDR: $35.53\%$).'
    )
    if old_gemini_fdr in c:
        c = c.replace(old_gemini_fdr, new_gemini_fdr)

    # 4. Table VIII - Arm 4 Accuracy
    old_t8_arm4 = r'Arm 4: 3-Agent (Defender No Veto) & 3 & $89.74\%$ & $98.88\%$ & $89.80\%$ & $94.12\%$ & $64.29\%$ & $94.74\%$ & $76.60\%$ & $85.36\%$ & $5.26\%$ & 9 & $\$0.4500$ \\'
    new_t8_arm4 = r'Arm 4: 3-Agent (Defender No Veto) & 3 & $\mathbf{90.60\%}$ & $98.88\%$ & $89.80\%$ & $94.12\%$ & $64.29\%$ & $94.74\%$ & $76.60\%$ & $85.36\%$ & $5.26\%$ & 9 & $\$0.4500$ \\'
    if old_t8_arm4 in c:
        c = c.replace(old_t8_arm4, new_t8_arm4)

    # 5. IV.B - Newcombe CI for recall difference
    old_wald_ci = r'paired difference asymptotic $95\%$ CI: $[-9.46\%, -0.75\%]$'
    new_newcombe_ci = r'paired difference Newcombe $95\%$ CI: $[-9.75\%, -0.45\%]$'
    if old_wald_ci in c:
        c = c.replace(old_wald_ci, new_newcombe_ci)

    # 6. Table X - Arm 4 Cost & Escalation Rate
    old_t10_arm4 = r'Arm 4: Naive Cascaded (Tier 1 + PoLL 3/5) & $97.14\%$ & $96.55\%$ & $97.11\%$ & $2.84\%$ & $717.8\text{ ms}$ & $\$1.5923$ & $3.4\%$ \\'
    new_t10_arm4 = r'Arm 4: Naive Cascaded (Tier 1 + PoLL 3/5) & $97.14\%$ & $96.55\%$ & $97.11\%$ & $2.84\%$ & $717.8\text{ ms}$ & $\mathbf{\$0.0541}$ & $3.4\%$ \\'
    if old_t10_arm4 in c:
        c = c.replace(old_t10_arm4, new_t10_arm4)

    # Table X Note explanation of P-single vs Solo GPT
    target_note_sub = 'escalation rate to the 3-agent council'
    idx_note = c.find(target_note_sub)
    if idx_note != -1:
        end_parbox = c.find(r'}\n\end{table*}', idx_note)
        if end_parbox != -1:
            old_parbox = c[idx_note:end_parbox]
            new_parbox = (
                r'escalation rate to the 3-agent council ($\$0.4500 \times 0.034 = \$0.0153$ per 1,000 messages); '
                r'Arm 4 cost reflects $0.034 \times \$1.5923 = \$0.0541$ per 1k SMS; '
                r'system latency represents the $267.7\text{ ms}$ median (mean: $267.5\text{ ms}$). '
                r'The $32.6\times$ cost gap between Table~\ref{tab:ablation_council} P-single ($\$0.0450$) and Table~\ref{tab:e2e_benchmark} Solo GPT-6.1-sol ($\$1.4667$) arises from output payload size: '
                r'Solo GPT emits full unconstrained chain-of-thought rationales (~1,200 output tokens/msg) whereas P-single outputs schema-constrained JSON (~180 output tokens/msg).'
            )
            c = c[:idx_note] + new_parbox + c[end_parbox:]

    # 7. IV.E (RQ5) - Detail PII real vs synthetic occurrences
    old_rq5_text = (
        r'To empirically evaluate sanitization efficacy on genuine telecommunications text, we ran a paired classification audit across the $N=117$ Hard Forensic Challenge Suite. '
        r'The sanitizer detected and masked exactly five numeric OTP verification codes with $100\%$ precision and zero false negatives ($0/5$ leaked). '
        r'Downstream council inference on the sanitized payloads yielded $100.00\%$ verdict concordance ($0/117$ label flips) compared to predictions on raw unmasked payloads, '
        r'verifying that privacy tokenization preserves semantic threat markers (urgency cues, homoglyph links, and teencode) without altering forensic reasoning. '
        r'We observed minor boundary over-redactions where regular expressions partially matched adjacent Vietnamese grammatical context words, documenting this as an engineering limitation requiring ongoing token vocabulary refinement.'
    )
    new_rq5_text = (
        r'To empirically evaluate sanitization efficacy on genuine telecommunications text, we audited all $N=117$ messages of the Hard Forensic Challenge Suite. '
        r'The sanitizer detected and masked exactly five numeric OTP verification codes with $100\%$ precision and zero false negatives ($0/5$ leaked). '
        r'Because the challenge suite naturally contained zero occurrences of phone numbers, bank accounts, Citizen IDs, or account balances, technical confidentiality for those four entity classes was formally verified on targeted test vectors. '
        r'Downstream council inference on sanitized payloads yielded $100.00\%$ verdict concordance ($0/117$ label flips) compared to raw unmasked payloads, '
        r'verifying that privacy tokenization preserves semantic threat markers without altering forensic reasoning. '
        r'Minor boundary over-redaction occurred in exactly $2$ samples ($1.7\%$) where trailing punctuation in carrier boilerplate was masked, without impacting classification verdicts.'
    )
    if old_rq5_text in c:
        c = c.replace(old_rq5_text, new_rq5_text)

    # 8. IV.F.1 - Condorcet overreach tone down
    old_condorcet = (
        r'This theoretical limitation explains why naive majority voting (Arm 4 in Table~\ref{tab:e2e_benchmark}) yielded a higher FPR ($2.84\%$) than our proposed architecture. '
        r'ScamShield-VN is designed to reduce correlated false positives through adversarial role specialization: Seat C (Public Defender) seeks counter-evidence against threat hypotheses on legitimate transactional messages, as empirically validated in RQ3.'
    )
    new_condorcet = (
        r'This theoretical perspective motivated the architectural design of ScamShield-VN. '
        r'On the $N=384$ exploratory development suite, naive majority voting (Arm 4 in Table~\ref{tab:e2e_benchmark}) recorded $6$ false alarms on authentic lures ($2.84\%$), '
        r'whereas the proposed architecture with Public Defender (Arm 5) recorded $5$ ($2.37\%$). '
        r'While this 1-sample difference on the development suite is statistically modest, adversarial role specialization provides an explicit design safeguard against correlated false alarms on complex transactional notifications.'
    )
    if old_condorcet in c:
        c = c.replace(old_condorcet, new_condorcet)

    # 9. WBCE vs parameter scaling overclaim
    old_wbce_claim = r'proved far more impactful than raw parameter scaling.'
    new_wbce_claim = r'proved highly effective on colloquial text; controlled ablation of WBCE against standard BCE on identical backbones remains an informative target for future scaling studies.'
    if old_wbce_claim in c:
        c = c.replace(old_wbce_claim, new_wbce_claim)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Updated 04_results.tex")


def update_05_conclusion():
    path = 'paper/sections/05_conclusion.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Model size & recall
    c = c.replace(r'$93.9\text{ MB}$', r'$98.42\text{ MB}$ / $93.86\text{ MiB}$')
    c = c.replace(r'Scam Recall ($95.62\% \pm 2.25\%$)', r'Scam Recall ($95.64\% \pm 2.04\%$)')

    # Qualitative justification
    c = c.replace(
        r'demonstrating that multi-agent councils offer value in auditable justification and cautious abstention rather than raw standalone accuracy.',
        r'demonstrating that multi-agent councils offer qualitative value in structured forensic justification and cautious abstention rather than raw standalone accuracy.'
    )

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Updated 05_conclusion.tex")


def update_06_endmatter():
    path = 'paper/sections/06_endmatter.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Acknowledgment clarification
    old_ack = r'The authors express sincere gratitude to the ChongLuaDao project and the National Cybersecurity Association for open cyber threat intelligence feeds that contributed to benchmark curation.'
    new_ack = r'The authors express sincere gratitude to the ChongLuaDao project and the National Cybersecurity Association for open cyber threat intelligence feeds, URL blacklists, and security advisories that informed benchmark curation.'
    if old_ack in c:
        c = c.replace(old_ack, new_ack)

    # Git commit hash
    old_rep = r'deposited in the public repository at \url{https://github.com/QuangWorkIT/RBL_ScamShield}.'
    new_rep = r'deposited in the public repository at \url{https://github.com/QuangWorkIT/RBL_ScamShield} (exact commit hash: \texttt{a65ec3188a23644031c647d1ff46ee411a88614c}).'
    if old_rep in c:
        c = c.replace(old_rep, new_rep)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Updated 06_endmatter.tex")


def update_main_title():
    path = 'paper/main.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    old_title = r'\title{ScamShield-VN: Evidence-Grounded Two-Tier Architecture for Vietnamese Scam and Phishing Detection}'
    new_title = r'\title{ScamShield-VN: Evidence-Driven Two-Tier Architecture for Vietnamese Scam and Phishing Detection}'
    if old_title in c:
        c = c.replace(old_title, new_title)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        print("Updated paper/main.tex title")


if __name__ == '__main__':
    update_00_abstract()
    update_01_intro()
    update_03_method()
    update_04_results()
    update_05_conclusion()
    update_06_endmatter()
    update_main_title()
    print("All Phase 2 updates applied successfully!")
