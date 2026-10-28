import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_monochrome_architecture_diagram(output_path="paper/figures/pipeline_architecture.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 3000 x 1650 ultra-high resolution (10 x 5.5 inches at 300 DPI)
    width = 3000
    height = 1650
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # STRICT MONOCHROME / GRAYSCALE PALETTE (Zero colors)
    BLACK = "#000000"
    CHARCOAL = "#222222"
    DARK_GRAY = "#444444"
    MID_GRAY = "#777777"
    BORDER_GRAY = "#AAAAAA"
    LIGHT_GRAY = "#E5E7EB"
    PILL_GRAY = "#F0F2F5"
    LIGHT_BG = "#F9FAFB"
    WHITE = "#FFFFFF"

    # Typography
    try:
        font_super = ImageFont.truetype("arialbd.ttf", 34)
        font_h1 = ImageFont.truetype("arialbd.ttf", 26)
        font_h2 = ImageFont.truetype("arialbd.ttf", 22)
        font_h3 = ImageFont.truetype("arialbd.ttf", 19)
        font_body_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_body = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 16)
        font_small_bold = ImageFont.truetype("arialbd.ttf", 16)
        font_tiny = ImageFont.truetype("arial.ttf", 14)
        font_tiny_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_code = ImageFont.truetype("consola.ttf", 17)
        font_code_bold = ImageFont.truetype("consolab.ttf", 18)
    except Exception:
        font_super = ImageFont.load_default()
        font_h1 = font_super
        font_h2 = font_super
        font_h3 = font_super
        font_body_bold = font_super
        font_body = font_super
        font_small = font_super
        font_small_bold = font_super
        font_tiny = font_super
        font_tiny_bold = font_super
        font_code = font_super
        font_code_bold = font_super

    # Helper: Draw card with clean header bar
    def draw_card(x0, y0, x1, y1, title=None, header_h=34, bg=WHITE, border=BLACK, lw=2, header_bg=LIGHT_GRAY, header_fg=BLACK, header_font=font_h3, subtitle=None, title_align="center"):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=bg, outline=border, width=lw)
        if title:
            # Draw header background
            draw.rounded_rectangle([x0, y0, x1, y0 + header_h], radius=8, fill=header_bg, outline=border, width=lw)
            draw.rectangle([x0 + 1, y0 + header_h - 8, x1 - 1, y0 + header_h], fill=header_bg)
            draw.line([x0, y0 + header_h, x1, y0 + header_h], fill=border, width=lw)
            
            if subtitle:
                # Two-line header with clean vertical spacing
                tb1 = draw.textbbox((0, 0), title, font=header_font)
                tw1 = tb1[2] - tb1[0]
                tb2 = draw.textbbox((0, 0), subtitle, font=font_small_bold)
                tw2 = tb2[2] - tb2[0]
                tot_h = (tb1[3] - tb1[1]) + (tb2[3] - tb2[1]) + 4
                top_y = y0 + (header_h - tot_h) / 2
                draw.text((x0 + (x1 - x0 - tw1) / 2, top_y), title, fill=header_fg, font=header_font)
                draw.text((x0 + (x1 - x0 - tw2) / 2, top_y + (tb1[3] - tb1[1]) + 4), subtitle, fill=header_fg, font=font_small_bold)
            else:
                tb = draw.textbbox((0, 0), title, font=header_font)
                tw = tb[2] - tb[0]
                th = tb[3] - tb[1]
                if title_align == "left":
                    tx = x0 + 18
                else:
                    tx = x0 + (x1 - x0 - tw) / 2
                ty = y0 + (header_h - th) / 2 - 2
                draw.text((tx, ty), title, fill=header_fg, font=header_font)

    # Helper: Text wrap with strict bounding box checking
    def draw_wrapped(text, x, y, max_w, font, fill=BLACK, spacing=5):
        words = text.split(" ")
        lines = []
        cur_line = []
        for word in words:
            test_line = " ".join(cur_line + [word])
            tb = draw.textbbox((0, 0), test_line, font=font)
            if (tb[2] - tb[0]) <= max_w:
                cur_line.append(word)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                    cur_line = [word]
                else:
                    lines.append(word)
                    cur_line = []
        if cur_line:
            lines.append(" ".join(cur_line))

        cur_y = y
        for l in lines:
            draw.text((x, cur_y), l, fill=fill, font=font)
            tb = draw.textbbox((0, 0), l, font=font)
            cur_y += (tb[3] - tb[1]) + spacing
        return cur_y

    # Helper: Draw crisp arrow
    def draw_arrow(x0, y0, x1, y1, lw=3, color=BLACK, head_len=13, head_w=7):
        draw.line([x0, y0, x1, y1], fill=color, width=lw)
        dx = x1 - x0
        dy = y1 - y0
        angle = math.atan2(dy, dx)
        tip = (x1, y1)
        p1 = (x1 - head_len * math.cos(angle - 0.45), y1 - head_len * math.sin(angle - 0.45))
        p2 = (x1 - head_len * math.cos(angle + 0.45), y1 - head_len * math.sin(angle + 0.45))
        draw.polygon([tip, p1, p2], fill=color)

    # Helper: Draw pill / badge
    def draw_badge(x0, y0, x1, y1, text, bg=PILL_GRAY, border=BLACK, fg=BLACK, font=font_small_bold, align="center"):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=bg, outline=border, width=1)
        lines = text.split("\n")
        line_boxes = [draw.textbbox((0, 0), l, font=font) for l in lines]
        line_heights = [(b[3] - b[1]) for b in line_boxes]
        tot_h = sum(line_heights) + (len(lines) - 1) * 4
        cur_y = y0 + (y1 - y0 - tot_h) / 2
        for idx, l in enumerate(lines):
            lw_text = line_boxes[idx][2] - line_boxes[idx][0]
            if align == "center":
                cur_x = x0 + (x1 - x0 - lw_text) / 2
            else:
                cur_x = x0 + 8
            draw.text((cur_x, cur_y), l, fill=fg, font=font)
            cur_y += line_heights[idx] + 4

    # =========================================================================
    # 0. MAIN TOP TITLE BANNER
    # =========================================================================
    draw.rounded_rectangle([30, 20, 2970, 78], radius=8, fill=CHARCOAL, outline=BLACK, width=2)
    main_title = "ScamShield-VN: End-to-End Two-Tier Pipeline Architecture & Provenance Mapping"
    tb = draw.textbbox((0, 0), main_title, font=font_super)
    draw.text((1500 - (tb[2]-tb[0])/2, 49 - (tb[3]-tb[1])/2), main_title, fill=WHITE, font=font_super)

    # =========================================================================
    # 1. COLUMN 1: DATASET & PARTITION SPLIT (x: 30 to 680, width: 650)
    # =========================================================================
    draw_card(30, 95, 680, 1610, "1. DATASET & PARTITION SPLIT", header_h=44, border=BLACK, header_bg=CHARCOAL, header_fg=WHITE, header_font=font_h2)

    # 1.1 Upstream Raw Feeds
    draw_card(50, 155, 660, 365, "Upstream Raw Feeds (ScamShield-VN-2664)", header_h=34, border=DARK_GRAY)
    draw.text((70, 205), "• Primary Feed: uitnlp/vietnamese-sms-dataset", fill=BLACK, font=font_body_bold)
    draw.text((85, 230), "2,629 samples (1,918 Ham, 711 Scam) • CC BY-SA 4.0", fill=DARK_GRAY, font=font_small)
    draw.text((70, 260), "• Supplementary Feed: vietnamese_sms_phishing_300", fill=BLACK, font=font_body_bold)
    draw.text((85, 285), "35 confirmed phishing instances (0 Ham, 35 Scam) • ODC-By", fill=DARK_GRAY, font=font_small)
    draw_badge(68, 318, 642, 355, "Total Unified Corpus: N = 2,664 (100% Unique Texts)", bg=LIGHT_BG, border=BORDER_GRAY, fg=BLACK, font=font_body_bold)

    # Arrow Down
    draw_arrow(355, 365, 355, 395, lw=3)

    # 1.2 Isolated Stratified Split
    draw_card(50, 395, 660, 535, "Isolated Partitioning Protocol (Seed 42)", header_h=34, border=DARK_GRAY)
    draw.text((70, 442), "• Stratified Split: scikit-learn (test_size = 0.100187)", fill=BLACK, font=font_body_bold)
    draw.text((70, 470), "• Training / Internal Val: N = 2,397 (90%)", fill=BLACK, font=font_body)
    draw.text((85, 496), "1,726 Ham (72.0%), 671 Scam (28.0%) -> Loss fine-tuning", fill=DARK_GRAY, font=font_small)

    # Arrow Down
    draw_arrow(355, 535, 355, 565, lw=3)

    # 1.3 Evaluation Partitions
    draw_card(50, 565, 660, 1055, "Evaluation Partitions & Evidence Mapping", header_h=34, border=DARK_GRAY)

    # Sub-card A: Frozen Test
    draw.rounded_rectangle([68, 615, 642, 745], radius=6, fill=LIGHT_BG, outline=DARK_GRAY, width=1)
    draw.text((80, 626), "[A] Isolated Frozen Test Partition (N = 267)", fill=BLACK, font=font_body_bold)
    draw.text((95, 654), "192 Ham (71.9%), 75 Scam (28.1%) • SHA-256 sealed holdout", fill=DARK_GRAY, font=font_small)
    draw.text((80, 683), "• Evaluates: Tier 1 Edge Encoders & Gemini Baseline", fill=BLACK, font=font_small)
    draw.text((80, 708), "• Evidence: TABLE VI (Edge Benchmark) & TABLE VII (McNemar)", fill=BLACK, font=font_small_bold)

    # Sub-card B: Challenge Suite
    draw.rounded_rectangle([68, 760, 642, 890], radius=6, fill=LIGHT_BG, outline=DARK_GRAY, width=1)
    draw.text((80, 771), "[B] Hard Forensic Challenge Suite (N = 117)", fill=BLACK, font=font_body_bold)
    draw.text((95, 799), "98 Scam (83.8%), 19 Benign Lures (16.2%) • Boundary Ambiguity", fill=DARK_GRAY, font=font_small)
    draw.text((80, 828), "• Evaluates: Tier 2 Council Ablation, Public Defender, P-single", fill=BLACK, font=font_small)
    draw.text((80, 853), "• Evidence: TABLES VIII & IX (Council & Defender Matrix)", fill=BLACK, font=font_small_bold)

    # Sub-card C: Combined Suite
    draw.rounded_rectangle([68, 905, 642, 1035], radius=6, fill=LIGHT_BG, outline=DARK_GRAY, width=1)
    draw.text((80, 916), "[C] Combined Development Suite (N = 384)", fill=BLACK, font=font_body_bold)
    draw.text((95, 944), "267 Frozen + 117 Challenge (10 exact duplicate strings mapped)", fill=DARK_GRAY, font=font_small)
    draw.text((80, 973), "• Evaluates: End-to-End Cascaded System & Tau Sweep", fill=BLACK, font=font_small)
    draw.text((80, 998), "• Evidence: TABLES X & XI (Cascade Benchmark & Tau Profile)", fill=BLACK, font=font_small_bold)

    # Arrow Down
    draw_arrow(355, 1055, 355, 1085, lw=3)

    # 1.4 Provenance & Leakage Controls
    draw_card(50, 1085, 660, 1590, "Data Provenance & Leakage Controls", header_h=34, border=DARK_GRAY)
    y_ctrl = 1130
    y_ctrl = draw_wrapped("• Exact Holdout Integrity: 0 / 267 (0.0%) exact string overlap between Frozen Test and Training partitions.", 70, y_ctrl, 570, font_small) + 6
    y_ctrl = draw_wrapped("• Boilerplate Disclosure: 63 / 267 (23.6%) near-duplicate overlap (Jaccard >= 0.85) from carrier templates.", 70, y_ctrl, 570, font_small) + 6
    y_ctrl = draw_wrapped("• Challenge Suite Overlap: 99 / 117 (84.6%) text match with Train; evaluated zero-shot on Tier 2 LLMs.", 70, y_ctrl, 570, font_small) + 6
    y_ctrl = draw_wrapped("• Threat Advisory Lure: Exactly 1 biometric fraud lure from national feed (canhbao.khonggianmang.vn, BANK_15).", 70, y_ctrl, 570, font_small) + 6
    y_ctrl = draw_wrapped("• Synthetic Stress Lures: 7 targeted test vectors (2 multi-step scam, 5 authentic banking alerts).", 70, y_ctrl, 570, font_small) + 6
    y_ctrl = draw_wrapped("• Label Ontology: Formal distinction between commercial bulk advertising (Decree 91) and malicious fraud.", 70, y_ctrl, 570, font_small) + 6
    draw_wrapped("• Ground Truth: Upstream Cohen's kappa = 0.88 marked externally unverified due to lack of raw rater logs.", 70, y_ctrl, 570, font_small)

    # =========================================================================
    # 2 & 3. MIDDLE COLUMN: ON-DEVICE CLIENT (TIER 1 & PRIVACY GATEWAY)
    # x: 710 to 1420, width: 710, height: 1515 (y: 95 to 1610)
    # =========================================================================
    draw_card(710, 95, 1420, 1610, "2. TIER 1 EDGE SCREENER & 3. CLIENT PRIVACY GATEWAY", header_h=44, border=BLACK, header_bg=CHARCOAL, header_fg=WHITE, header_font=font_h2)

    # 2.1 ViSoBERT Box
    draw_card(730, 155, 1400, 420, "ViSoBERT + Cost-Sensitive WBCE (Tier 1 Edge Screener)", header_h=34, border=DARK_GRAY)
    draw.text((750, 202), "• Backbone Architecture: uitnlp/visobert (97.57M Params)", fill=BLACK, font=font_body_bold)
    draw.text((750, 230), "• Pretraining Corpus: 1 GB social media text (approx. 3 GB raw)", fill=DARK_GRAY, font=font_small)
    draw.text((750, 258), "• Cost-Sensitive Loss: WBCE (alpha = 5.0 penalty on missed scams)", fill=BLACK, font=font_body_bold)
    draw.text((750, 286), "• Quantized Artifact: ONNX INT8 (98.42 MB / 93.86 MiB)", fill=BLACK, font=font_body_bold)
    draw.text((750, 314), "• Inference Latency: 70.7 ms on desktop CPU (mean 70.72 ms)", fill=DARK_GRAY, font=font_small)
    draw.text((750, 342), "• Benchmark Recall: 95.64% +- 2.04% (Frozen holdout: 72/75 = 96.00%)", fill=BLACK, font=font_body_bold)
    draw.text((750, 370), "• Output Metric: Calibrated Scam Probability P_T1 in [0.0, 1.0]", fill=DARK_GRAY, font=font_small_bold)

    # Arrow Down
    draw_arrow(1065, 420, 1065, 450, lw=3)

    # 2.2 Confidence Routing Engine
    draw_card(730, 450, 1400, 585, "Confidence Routing Engine (Operating Point tau = 0.90)", header_h=34, border=DARK_GRAY)
    draw.text((750, 495), "Routing Metric: C_T1(x) = max(P_T1, 1 - P_T1)", fill=BLACK, font=font_code_bold)
    draw.text((750, 525), "• If C_T1(x) >= 0.90 -> Confident Local Resolution (96.6% traffic)", fill=BLACK, font=font_body_bold)
    draw.text((750, 553), "• If C_T1(x) < 0.90  -> Ambiguous Boundary Lure (3.4% traffic)", fill=DARK_GRAY, font=font_body_bold)

    # Two Branch Arrows from Router:
    # Left Branch Arrow (Confident -> Fast-Path)
    draw_arrow(885, 585, 885, 625, lw=3)
    # Right Branch Arrow (Ambiguous -> Escalation Gateway)
    draw_arrow(1245, 585, 1245, 625, lw=3)

    # 2.3A Fast-Path Local Edge Resolution (Left Sub-card, width: 320)
    draw_card(730, 625, 1050, 795, "Fast-Path Edge (96.6%)", header_h=30, border=DARK_GRAY)
    draw.text((745, 665), "Resolved Locally on Mobile Device:", fill=DARK_GRAY, font=font_tiny)
    draw.text((745, 690), "• SCAM-RISK (P >= 0.90): Quarantine", fill=BLACK, font=font_small_bold)
    draw.text((745, 715), "  Immediate subscriber alert", fill=DARK_GRAY, font=font_tiny)
    draw.text((745, 740), "• LOW-RISK  (P <= 0.10): Deliver", fill=BLACK, font=font_small_bold)
    draw.text((745, 765), "  Safe delivery to message inbox", fill=DARK_GRAY, font=font_tiny)

    # 2.3B Boundary Escalation Gateway (Right Sub-card, width: 320)
    draw_card(1080, 625, 1400, 795, "Escalation Gateway (3.4%)", header_h=30, border=DARK_GRAY)
    draw.text((1095, 665), "Ambiguous Boundary Lures:", fill=DARK_GRAY, font=font_tiny)
    draw.text((1095, 690), "• C_T1(x) < 0.90 triggers cloud triage", fill=BLACK, font=font_small_bold)
    draw.text((1095, 715), "• Enforces client PII sanitization", fill=DARK_GRAY, font=font_tiny)
    draw.text((1095, 740), "• Decree 13/2023 compliance", fill=BLACK, font=font_small_bold)
    draw.text((1095, 765), "• Routes to Sanitizer below", fill=DARK_GRAY, font=font_tiny)

    # DIRECT VERTICAL ESCALATION ARROW FROM 2.3B TO 3.1:
    # Arrow segments: from bottom of 2.3B (795) to top of badge (806),
    # then badge sits at 806-834, then arrow continues 834 to top border of Card 3.1 (845).
    draw.line([1240, 795, 1240, 806], fill=BLACK, width=3)
    draw_badge(1155, 806, 1325, 834, "Escalate 3.4% Traffic", bg=WHITE, border=DARK_GRAY, fg=BLACK, font=font_tiny_bold)
    draw_arrow(1240, 834, 1240, 845, lw=3)

    # 3.1 Privacy Sanitizer Box (Title aligned left to keep right side clear for incoming arrow at x=1240)
    draw_card(730, 845, 1400, 1215, "Client-Side MessagePIISanitizer (Article 25)", header_h=34, border=DARK_GRAY, title_align="left")
    draw.text((750, 892), "Local Pre-Transmission Redaction (0.03 ms latency on mobile CPU):", fill=DARK_GRAY, font=font_small)
    draw.text((750, 920), "• Phone Numbers        -> [PHONE_REDACTED]", fill=BLACK, font=font_code)
    draw.text((750, 946), "• Bank Account / Cards -> [ACCOUNT_REDACTED]", fill=BLACK, font=font_code)
    draw.text((750, 972), "• Citizen IDs (CCCD)   -> [CITIZEN_ID_REDACTED]", fill=BLACK, font=font_code)
    draw.text((750, 998), "• OTP Verification     -> [OTP_REDACTED]", fill=BLACK, font=font_code)
    draw.text((750, 1024), "• Balance Statements   -> [BALANCE_REDACTED]", fill=BLACK, font=font_code)
    draw.text((750, 1060), "Audit Verification (RQ5, Section IV.E):", fill=BLACK, font=font_body_bold)
    draw.text((765, 1085), "• 100% masking precision on real OTP tokens (5/5 detected)", fill=DARK_GRAY, font=font_small)
    draw.text((765, 1110), "• 100% verdict concordance on sanitized vs raw payloads (0 flips)", fill=DARK_GRAY, font=font_small)
    draw.text((765, 1135), "• Zero plaintext personal data leaves the mobile device", fill=BLACK, font=font_small_bold)

    # Arrow Down
    draw_arrow(1065, 1215, 1065, 1245, lw=3)

    # 3.2 Resilience & Fallback Controller
    draw_card(730, 1245, 1400, 1590, "Resilience & Fallback Controller (Section III.F)", header_h=34, border=DARK_GRAY)
    draw.text((750, 1290), "Circuit Breaker & Standby Priority Chains:", fill=DARK_GRAY, font=font_small)
    draw.text((750, 1318), "• Primary Maker Model: gpt-6.1-sol (via API endpoint)", fill=BLACK, font=font_body_bold)
    draw.text((750, 1346), "• Secondary Checker: gemini-3.5-flash-lite / gemini-3.8-flash", fill=DARK_GRAY, font=font_small)
    draw.text((750, 1374), "• Circuit Breaker: 3 consecutive fails -> 300 s cooldown", fill=BLACK, font=font_body)
    draw.text((750, 1402), "• Fallback Policy: Local rule heuristic on persistent outage", fill=DARK_GRAY, font=font_small)
    draw.text((750, 1435), "Empirical Telemetry Across 117 Challenge Cases:", fill=BLACK, font=font_body_bold)
    draw.text((765, 1460), "• Schema Parse Failures: 0 / 351 invocations (100% valid JSON)", fill=BLACK, font=font_small)
    draw.text((765, 1485), "• Circuit Breaker Triggers: 0 (Zero outages during benchmark)", fill=BLACK, font=font_small_bold)

    # =========================================================================
    # DEDICATED GUTTER ROUTING (x: 1420 to 1470, width: 50 px)
    # Sanitized payload exits Sanitizer at (1400, 970) -> gutter (1445) -> up to y=205 -> Tier 2 (1490)
    # =========================================================================
    draw.line([1400, 970, 1445, 970], fill=BLACK, width=3)
    draw.line([1445, 970, 1445, 205], fill=BLACK, width=3)
    draw_arrow(1445, 205, 1490, 205, lw=3)
    # Clean vertical badge in the generous 50px gutter with zero collisions
    draw_badge(1422, 530, 1468, 610, "Sanitized\nPayload\n(3.4%)", bg=WHITE, border=DARK_GRAY, fg=BLACK, font=font_tiny, align="center")

    # =========================================================================
    # 4. COLUMN 4: TIER 2 FORENSIC COUNCIL & VERDICT PROTOCOL (x: 1470 to 2970, width: 1500)
    # =========================================================================
    draw_card(1470, 95, 2970, 1610, "4. TIER 2: FORENSIC COUNCIL & VERDICT PROTOCOL", header_h=44, border=BLACK, header_bg=CHARCOAL, header_fg=WHITE, header_font=font_h2)

    # 4.1 Specialist Panel (Parent Card, width: 1460)
    draw_card(1490, 155, 2950, 565, "Consolidated 3-Agent Specialist Panel (Tier 2 Cloud Deliberation)", header_h=36, border=BLACK)

    # 3 Specialist Seats (width: 450 each, spacing: 35)
    # Seat A (x: 1510 to 1960)
    draw_card(1510, 205, 1960, 545, "SEAT A (w_A = 0.35)", header_h=52, border=DARK_GRAY, header_font=font_h3, subtitle="Cyber-Financial Analyst")
    draw.text((1525, 272), "• URL homoglyphs & fake portals", fill=BLACK, font=font_small)
    draw.text((1525, 298), "• Malicious .apk direct links", fill=BLACK, font=font_small)
    draw.text((1525, 324), "• Brand spoofing & typosquatting", fill=BLACK, font=font_small)
    draw.text((1525, 350), "• SBV 2345/QD-NHNN compliance", fill=BLACK, font=font_small)
    draw.text((1525, 385), "Model: gpt-6.1-sol / gemini-3.5", fill=DARK_GRAY, font=font_small_bold)
    draw.rounded_rectangle([1525, 420, 1945, 525], radius=4, fill=LIGHT_BG, outline=BORDER_GRAY, width=1)
    draw.text((1535, 432), "Deliberation Output:", fill=BLACK, font=font_small_bold)
    draw.text((1535, 458), "• Vote: SCAM | HAM | UNKNOWN", fill=BLACK, font=font_small)
    draw.text((1535, 484), "• Probability P_A in [0.0, 1.0]", fill=BLACK, font=font_small)

    # Seat B (x: 1995 to 2445)
    draw_card(1995, 205, 2445, 545, "SEAT B (w_B = 0.35)", header_h=52, border=DARK_GRAY, header_font=font_h3, subtitle="Psycholinguistic & Slang")
    draw.text((2010, 272), "• Urgency & fear extortion cues", fill=BLACK, font=font_small)
    draw.text((2010, 298), "• Police & court summons pretext", fill=BLACK, font=font_small)
    draw.text((2010, 324), "• Vietnamese teencode & leetspeak", fill=BLACK, font=font_small)
    draw.text((2010, 350), "• Diacritic omission & slang evasion", fill=BLACK, font=font_small)
    draw.text((2010, 385), "Model: gpt-6.1-sol / gemini-3.5", fill=DARK_GRAY, font=font_small_bold)
    draw.rounded_rectangle([2010, 420, 2430, 525], radius=4, fill=LIGHT_BG, outline=BORDER_GRAY, width=1)
    draw.text((2020, 432), "Deliberation Output:", fill=BLACK, font=font_small_bold)
    draw.text((2020, 458), "• Vote: SCAM | HAM | UNKNOWN", fill=BLACK, font=font_small)
    draw.text((2020, 484), "• Probability P_B in [0.0, 1.0]", fill=BLACK, font=font_small)

    # Seat C (x: 2480 to 2930)
    draw_card(2480, 205, 2930, 545, "SEAT C (w_C = 0.30)", header_h=52, border=DARK_GRAY, header_font=font_h3, subtitle="Public Defender Advocate")
    draw.text((2495, 272), "• Anti-Alarm Fatigue shield", fill=BLACK, font=font_small)
    draw.text((2495, 298), "• Authentic OTP syntax validation", fill=BLACK, font=font_small)
    draw.text((2495, 324), "• Standard bank balance feeds", fill=BLACK, font=font_small)
    draw.text((2495, 350), "• Adversarial counter-evidence", fill=BLACK, font=font_small)
    draw.text((2495, 385), "Model: gpt-6.1-sol / gemini-3.8", fill=DARK_GRAY, font=font_small_bold)
    draw.rounded_rectangle([2495, 420, 2915, 525], radius=4, fill=LIGHT_BG, outline=BORDER_GRAY, width=1)
    draw.text((2505, 432), "Deliberation Output:", fill=BLACK, font=font_small_bold)
    draw.text((2505, 458), "• Vote: HAM protection vote", fill=BLACK, font=font_small)
    draw.text((2505, 484), "• Veto Flag: delta_defender = 0.25", fill=BLACK, font=font_small_bold)

    # Arrow Down from Panel to Consensus
    draw_arrow(2220, 565, 2220, 605, lw=3)

    # 4.2 Weighted Consensus Aggregation & Defender Veto
    draw_card(1490, 605, 2950, 835, "Weighted Consensus Aggregation & Public Defender Veto (Section III.D)", header_h=36, border=BLACK)
    draw_badge(2000, 650, 2440, 692, "P_council = sum(w_j * P_j) - delta_defender", bg=LIGHT_BG, border=BLACK, fg=BLACK, font=font_code_bold)

    y_agg = 708
    y_agg = draw_wrapped("• Weighted Fusion: P_raw = 0.35 * P_A + 0.35 * P_B + 0.30 * P_C (Specialist weights reflect empirical validation precision).", 1520, y_agg, 1400, font_body) + 6
    y_agg = draw_wrapped("• Public Defender Veto: delta_defender = 0.25 offset applied when Seat C votes HAM with confidence >= 0.80 on verified templates.", 1520, y_agg, 1400, font_body_bold) + 6
    draw_wrapped("• Empirical Validation (Table IX): Arms 1, 2, and P-single achieve 0.00% False Positive Rate on authentic banking lures (N=19).", 1520, y_agg, 1400, font_small_bold)

    # Arrow Down
    draw_arrow(2220, 835, 2220, 870, lw=3)

    # 4.3 Standardized 3-Label Verdict Protocol
    draw_card(1490, 870, 2950, 1175, "Standardized 3-Label Verdict Protocol (Section III.G)", header_h=36, border=BLACK)

    # Verdict 1: SCAM-RISK (width: 450)
    draw_card(1510, 920, 1960, 1155, "SCAM-RISK", header_h=34, border=BLACK, header_bg=CHARCOAL, header_fg=WHITE, header_font=font_h3)
    draw_badge(1620, 966, 1850, 1000, "P_council >= 0.60", bg=LIGHT_BG, border=BLACK, fg=BLACK, font=font_code_bold)
    draw.text((1530, 1018), "• Threat: High / Critical Smishing", fill=BLACK, font=font_body_bold)
    draw.text((1530, 1046), "• Action: Immediate User Block", fill=BLACK, font=font_body_bold)
    draw.text((1530, 1074), "• Quarantine suspicious payload", fill=DARK_GRAY, font=font_small)
    draw.text((1530, 1100), "• Push threat signature to carrier", fill=DARK_GRAY, font=font_small)

    # Verdict 2: LOW-RISK (width: 450)
    draw_card(1995, 920, 2445, 1155, "LOW-RISK", header_h=34, border=BLACK, header_bg=LIGHT_GRAY, header_fg=BLACK, header_font=font_h3)
    draw_badge(2105, 966, 2335, 1000, "P_council < 0.40", bg=LIGHT_BG, border=BLACK, fg=BLACK, font=font_code_bold)
    draw.text((2015, 1018), "• Status: Authentic Notification", fill=BLACK, font=font_body_bold)
    draw.text((2015, 1046), "• Action: Deliver Safely to Inbox", fill=BLACK, font=font_body_bold)
    draw.text((2015, 1074), "• Verified banking OTP / balance", fill=DARK_GRAY, font=font_small)
    draw.text((2015, 1100), "• Carrier promotion (Decree 91)", fill=DARK_GRAY, font=font_small)

    # Verdict 3: UNKNOWN (width: 450)
    draw_card(2480, 920, 2930, 1155, "UNKNOWN", header_h=34, border=BLACK, header_bg=PILL_GRAY, header_fg=BLACK, header_font=font_h3)
    draw_badge(2570, 966, 2840, 1000, "0.40 <= P_council < 0.60", bg=LIGHT_BG, border=BLACK, fg=BLACK, font=font_code_bold)
    draw.text((2500, 1018), "• Status: Boundary Ambiguity", fill=BLACK, font=font_body_bold)
    draw.text((2500, 1046), "• Action: Cautious Abstention", fill=BLACK, font=font_body_bold)
    draw.text((2500, 1074), "• Route to Async Human Audit", fill=DARK_GRAY, font=font_small)
    draw.text((2500, 1100), "• Prevent forced classification", fill=DARK_GRAY, font=font_small)

    # Arrow Down
    draw_arrow(2220, 1175, 2220, 1210, lw=3)

    # 4.4 Council Trade-off & P-single Baseline Context (Table VIII)
    draw_card(1490, 1210, 2950, 1590, "Council Trade-off & Baseline Comparison Matrix (Evidence: Table VIII & Section IV.B)", header_h=36, border=BLACK)
    y_ctx = 1260
    y_ctx = draw_wrapped("• Full 5-Agent Council (Arm 1): Accuracy 94.87%, Recall 93.88%, Macro-F1 91.60%, 4 UNKNOWN verdicts, $0.7500 / 1k SMS.", 1520, y_ctx, 1400, font_body) + 6
    y_ctx = draw_wrapped("• Proposed 3-Agent Council (Arm 2): Accuracy 90.60%, Recall 88.78%, Macro-F1 85.80%, 10 UNKNOWN verdicts, $0.4500 / 1k SMS (40% token expenditure saving vs Arm 1).", 1520, y_ctx, 1400, font_body) + 6
    y_ctx = draw_wrapped("• McNemar Paired Test (Arm 2 vs Arm 1): p = 0.0625 (exact binomial), chi2 = 3.2000 (p = 0.0736) -> No statistically significant difference detected, though five discordant pairs provide insufficient evidence of equivalence.", 1520, y_ctx, 1400, font_body_bold) + 6
    y_ctx = draw_wrapped("• Single-LLM Baseline P-single (Wang et al., ACL 2024): Accuracy 96.58%, Recall 95.92%, Macro-F1 94.20%, 2 UNKNOWN verdicts, $0.0450 / 1k SMS (10x cheaper than Arm 2).", 1520, y_ctx, 1400, font_body_bold) + 6
    draw_wrapped("• Academic Positioning: P-single achieves higher raw accuracy at lower cost; the multi-agent council's value rests on auditable multi-perspective qualitative rationale and cautious abstention on legally sensitive boundaries rather than standalone accuracy.", 1520, y_ctx, 1400, font_small)

    # Save to both locations
    img.save(output_path, "PNG", dpi=(300, 300))
    alt_path = "figures/pipeline_architecture.png"
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    img.save(alt_path, "PNG", dpi=(300, 300))
    print(f"Generated clean monochrome architecture diagram at:\n  - {output_path}\n  - {alt_path}")

if __name__ == "__main__":
    create_monochrome_architecture_diagram()
