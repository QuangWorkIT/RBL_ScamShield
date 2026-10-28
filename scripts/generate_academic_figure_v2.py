import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

def create_publication_figure(output_png="paper/figures/pipeline_architecture.png", dpi=300):
    # Set academic font styling
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'mathtext.fontset': 'dejavusans',
        'text.color': '#0F172A',
        'figure.autolayout': False,
    })

    # Dimensions: 16.0 inches x 8.2 inches (Publication Grade)
    fig, ax = plt.subplots(figsize=(16.0, 8.2), dpi=dpi)
    ax.set_xlim(0, 16.0)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    # Color Palette - Professional Academic / IEEE Style
    NAVY = "#0F2A4A"
    STEEL = "#1E5AA0"
    SLATE_DARK = "#0F172A"
    SLATE_MED = "#475569"
    SLATE_LIGHT = "#94A3B8"
    BG_CLIENT = "#F8FAFC"
    BG_CLOUD = "#F8FAFC"
    BORDER_CLIENT = "#64748B"
    BORDER_CLOUD = "#2563EB"
    
    # Risk Colors
    SCAM_RED = "#DC2626"
    SCAM_BG = "#FEF2F2"
    SCAM_BORDER = "#EF4444"
    SCAM_TEXT = "#991B1B"
    
    HAM_GREEN = "#16A34A"
    HAM_BG = "#F0FDF4"
    HAM_BORDER = "#10B981"
    HAM_TEXT = "#065F46"
    
    WARN_AMBER = "#D97706"
    WARN_BG = "#FFFBEB"
    WARN_BORDER = "#F59E0B"
    WARN_TEXT = "#92400E"

    PURPLE_BORDER = "#8B5CF6"
    PURPLE_BG = "#FAF5FF"
    PURPLE_TEXT = "#6D28D9"

    # Helper function to draw an academic card with a crisp header bar
    def draw_academic_card(x, y, w, h, title, header_bg=STEEL, header_h=0.38, bg="#FFFFFF", border="#CBD5E1", lw=1.2, radius=0.08):
        # Base card
        card = FancyBboxPatch((x, y), w, h,
                              boxstyle=f"round,pad=0,rounding_size={radius}",
                              facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
        ax.add_patch(card)
        
        # Header banner (clipped to top of card)
        header = FancyBboxPatch((x, y + h - header_h), w, header_h,
                               boxstyle=f"round,pad=0,rounding_size={radius}",
                               facecolor=header_bg, edgecolor=header_bg, linewidth=0, zorder=3)
        ax.add_patch(header)
        fill_rect = Rectangle((x, y + h - header_h), w, header_h * 0.4,
                              facecolor=header_bg, edgecolor=header_bg, linewidth=0, zorder=3)
        ax.add_patch(fill_rect)
        
        # Header text
        ax.text(x + w / 2.0, y + h - header_h / 2.0, title,
                fontsize=8.0, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=4)

    # Helper function to draw clean straight arrows
    def draw_arrow(x1, y1, x2, y2, color="#475569", lw=1.6, zorder=6):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle="-|>",
                                mutation_scale=12,
                                color=color, linewidth=lw, zorder=zorder)
        ax.add_patch(arrow)

    # =========================================================================
    # 0. MAIN FIGURE TITLE BANNER
    # =========================================================================
    title_box = FancyBboxPatch((0.4, 7.50), 15.2, 0.48,
                               boxstyle="round,pad=0,rounding_size=0.08",
                               facecolor=NAVY, edgecolor=NAVY, linewidth=0, zorder=2)
    ax.add_patch(title_box)
    ax.text(8.0, 7.74, "ScamShield-VN: Two-Tier Edge-Cloud Architecture & Triage Operational Flow",
            fontsize=11.0, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=3)

    # =========================================================================
    # 1. TIER BOUNDARY CONTAINERS (DEVICE vs CLOUD)
    # =========================================================================
    # Left Boundary: Client Mobile Device
    dev_box = FancyBboxPatch((0.4, 0.35), 6.6, 6.95,
                             boxstyle="round,pad=0,rounding_size=0.15",
                             facecolor=BG_CLIENT, edgecolor=BORDER_CLIENT, linewidth=1.5, linestyle="--", zorder=1)
    ax.add_patch(dev_box)
    
    ax.text(0.65, 7.08, "CLIENT MOBILE DEVICE BOUNDARY (TIER 1 SCREENING)",
            fontsize=9.2, fontweight='bold', color=SLATE_DARK, ha='left', va='center', zorder=3)
    ax.text(0.65, 6.86, "On-Device Inference  •  Sub-100 ms CPU Latency  •  Local Privacy Preservation",
            fontsize=7.6, color=SLATE_MED, ha='left', va='center', zorder=3)

    # Right Boundary: Secure Cloud Infrastructure
    cloud_box = FancyBboxPatch((7.3, 0.35), 8.3, 6.95,
                               boxstyle="round,pad=0,rounding_size=0.15",
                               facecolor=BG_CLOUD, edgecolor=BORDER_CLOUD, linewidth=1.5, linestyle="--", zorder=1)
    ax.add_patch(cloud_box)
    
    ax.text(7.55, 7.08, "SECURE CLOUD BACKEND BOUNDARY (TIER 2 FORENSIC COUNCIL)",
            fontsize=9.2, fontweight='bold', color=BORDER_CLOUD, ha='left', va='center', zorder=3)
    ax.text(7.55, 6.86, "Escalated Ambiguous Lures (3.4%)  •  Multi-Agent Deliberation  •  Adversarial Public Defender Veto",
            fontsize=7.6, color=SLATE_MED, ha='left', va='center', zorder=3)

    # =========================================================================
    # 2. DEVICE: TOP ROW - INGESTION, SCREENING, ROUTING
    # =========================================================================
    # Card 1: Incoming SMS Input
    draw_academic_card(0.6, 4.30, 1.4, 2.30, "1. Incoming SMS", header_bg=NAVY)
    ax.text(1.30, 5.80, "SMS Message $x$", fontsize=8.2, fontweight='bold', color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(1.30, 5.20, "Raw message stream:\n- Vietnamese text\n- Slang & teencode\n- URLs / Shortlinks\n- Banking OTP lures",
            fontsize=7.0, color=SLATE_MED, ha='center', va='center', zorder=4)
    ax.text(1.30, 4.55, "[ Mobile Client ]", fontsize=6.5, fontstyle='italic', color=SLATE_LIGHT, ha='center', va='center', zorder=4)

    # Arrow 1 -> 2
    draw_arrow(2.0, 5.45, 2.35, 5.45, color=STEEL, lw=1.8)

    # Card 2: Tier 1 ViSoBERT Edge Screener
    draw_academic_card(2.35, 4.10, 2.2, 2.50, "2. Tier 1 Edge Screener", header_bg=STEEL)
    ax.text(3.45, 6.18, "ViSoBERT INT8", fontsize=8.5, fontweight='bold', color="#1E3A8A", ha='center', va='center', zorder=4)
    ax.text(3.45, 5.90, "Cost-Sensitive Loss ($\\alpha = 5.0$)", fontsize=7.4, fontweight='bold', color=BORDER_CLOUD, ha='center', va='center', zorder=4)
    ax.text(3.45, 5.25, "- 110M Parameters (98.4 MB)\n- CPU Latency: 70.7 ms (ONNX)\n- 5x loss weight on missed scams\n- Frozen Test Scam Recall: 95.62%",
            fontsize=6.8, color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(3.45, 4.45, "Output: Score $P_{\\mathrm{T1}} \\in [0, 1]$\nConfidence: $C_{\\mathrm{T1}} = \\max(P, 1-P)$",
            fontsize=7.0, fontweight='bold', color=SLATE_DARK, ha='center', va='center', zorder=4)

    # Arrow 2 -> 3
    draw_arrow(4.55, 5.45, 4.90, 5.45, color=STEEL, lw=1.8)

    # Card 3: Confidence Router
    draw_academic_card(4.90, 4.30, 1.85, 2.30, "3. Confidence Router", header_bg=SLATE_DARK)
    ax.text(5.82, 5.85, "Operating Point $\\tau = 0.90$", fontsize=7.8, fontweight='bold', color=BORDER_CLOUD, ha='center', va='center', zorder=4)
    ax.text(5.82, 5.25, "Routing Rule:\nIs $C_{\\mathrm{T1}}(x) \\geq \\tau$?\n\nHigh Confidence\nvs. Ambiguous Lure",
            fontsize=7.0, color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(5.82, 4.55, "[ Exploratory Setpoint ]", fontsize=6.5, fontstyle='italic', color=SLATE_LIGHT, ha='center', va='center', zorder=4)

    # =========================================================================
    # 3. DEVICE: BOTTOM ROW - FAST PATH & CLIENT PII SANITIZER
    # =========================================================================
    # Fast Path Branch (YES, 96.6%): Arrow from Router down-left to Fast Path Card
    draw_arrow(5.35, 4.30, 5.35, 3.85, color=HAM_GREEN, lw=1.8)
    draw_arrow(5.35, 3.85, 3.85, 3.85, color=HAM_GREEN, lw=1.8)
    draw_arrow(3.85, 3.85, 3.85, 3.55, color=HAM_GREEN, lw=1.8)
    ax.text(4.60, 4.02, "Yes: Confident (96.6%)", fontsize=7.0, fontweight='bold', color=HAM_GREEN, ha='center', va='bottom', zorder=6)

    # Card 4: Fast-Path Local Decision
    draw_academic_card(0.6, 0.60, 3.3, 2.85, "Fast-Path Edge Resolution (96.6% Local)", header_bg=HAM_GREEN, bg=HAM_BG, border=HAM_BORDER)
    ax.text(2.25, 3.00, "Confident Edge Decision ($C_{\\mathrm{T1}} \\geq 0.90$)", fontsize=7.6, fontweight='bold', color=HAM_TEXT, ha='center', va='center', zorder=4)
    ax.text(2.25, 2.65, "Sub-100 ms Total Latency  •  Zero Cloud API Cost", fontsize=7.0, color=HAM_TEXT, ha='center', va='center', zorder=4)
    
    # Sub-card: High-Risk Scam
    draw_academic_card(0.75, 1.65, 3.0, 0.85, "High-Risk Scam ($P_{\\mathrm{T1}} \\geq 0.90$)", header_bg=SCAM_RED, header_h=0.28, bg=SCAM_BG, border=SCAM_BORDER)
    ax.text(2.25, 1.95, "Immediate Local Quarantine & Threat Alert", fontsize=6.7, fontweight='bold', color=SCAM_TEXT, ha='center', va='center', zorder=4)

    # Sub-card: Benign Alert
    draw_academic_card(0.75, 0.70, 3.0, 0.85, "Benign Alert ($P_{\\mathrm{T1}} \\leq 0.10$)", header_bg=HAM_GREEN, header_h=0.28, bg=HAM_BG, border=HAM_BORDER)
    ax.text(2.25, 1.00, "Normal Delivery to Subscriber Inbox", fontsize=6.7, fontweight='bold', color=HAM_TEXT, ha='center', va='center', zorder=4)

    # Escalation Branch (NO, 3.4%): Arrow from Router down to PII Sanitizer
    draw_arrow(6.30, 4.30, 6.30, 3.55, color=WARN_AMBER, lw=1.8)
    ax.text(6.35, 3.90, "No: Ambiguous (3.4%)\nEscalate to Council", fontsize=7.0, fontweight='bold', color=WARN_AMBER, ha='left', va='center', zorder=6)

    # Card 5: Client-Side Privacy Sanitizer
    draw_academic_card(4.15, 0.60, 2.6, 2.85, "4. Privacy Sanitizer", header_bg="#1E40AF", bg="#EFF6FF", border="#93C5FD")
    ax.text(5.45, 3.00, "MessagePIISanitizer", fontsize=7.8, fontweight='bold', color="#1E3A8A", ha='center', va='center', zorder=4)
    ax.text(5.45, 2.65, "Local Pre-Transmission Redaction:\n(0.03 ms Regex Latency)", fontsize=6.8, color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(5.45, 1.85, "- Phone $\\rightarrow$ [PHONE_REDACTED]\n- Bank Acct $\\rightarrow$ [ACCT_REDACTED]\n- Citizen ID $\\rightarrow$ [ID_REDACTED]\n- OTP Code $\\rightarrow$ [OTP_REDACTED]",
            fontsize=6.7, color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(5.45, 1.00, "Zero plaintext credentials\nleave the mobile client\n(Article 25 Motivation)", fontsize=6.5, fontstyle='italic', color=BORDER_CLOUD, ha='center', va='center', zorder=4)

    # Sanitized Lure crosses Boundary into Cloud
    draw_arrow(6.75, 2.00, 7.50, 2.00, color=BORDER_CLOUD, lw=2.2)
    ax.text(7.12, 2.22, "Sanitized Lure\n(3.4% Traffic)", fontsize=7.0, fontweight='bold', color=BORDER_CLOUD, ha='center', va='bottom', zorder=6)

    # =========================================================================
    # 4. CLOUD: 3 COLUMNS (SPECIALISTS -> CONSENSUS -> 3-LABEL VERDICTS)
    # =========================================================================
    
    # ------------------ COLUMN 1: 3 SPECIALIST SEATS -------------------------
    # Ingress distribution bus: from (7.50, 2.00) distribute to 3 seats
    draw_arrow(7.50, 2.00, 7.50, 5.75, color=BORDER_CLOUD, lw=1.6)
    draw_arrow(7.50, 5.75, 7.65, 5.75, color=STEEL, lw=1.5) # to Seat A
    draw_arrow(7.50, 3.80, 7.65, 3.80, color=PURPLE_TEXT, lw=1.5) # to Seat B
    draw_arrow(7.50, 2.00, 7.65, 2.00, color=SCAM_RED, lw=1.5) # to Seat C

    # Seat A: Cyber-Financial Analyst
    draw_academic_card(7.65, 4.80, 2.55, 1.90, "Seat A: Cyber-Financial ($w_A = 0.35$)", header_bg=STEEL)
    ax.text(8.92, 5.95, "- Brand spoofing & domain typos\n- Malicious link structure & APKs\n- Fake OTT / VNeID app lures\n- SBV 2345/QD-NHNN compliance",
            fontsize=6.6, color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(8.92, 5.08, "Output: Score $P_A \\in [0, 1]$\n+ Technical Forensics", fontsize=6.6, fontweight='bold', color="#1E3A8A", ha='center', va='center', zorder=4)

    # Seat B: Psycholinguistic Specialist
    draw_academic_card(7.65, 2.70, 2.55, 1.90, "Seat B: Psycholinguistic ($w_B = 0.35$)", header_bg="#6D28D9")
    ax.text(8.92, 3.85, "- Urgency & fear extortion cues\n- Police / court summon pretext\n- Vietnamese teencode & slang\n- Emotional manipulation trace",
            fontsize=6.6, color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(8.92, 2.98, "Output: Score $P_B \\in [0, 1]$\n+ Behavioral Traces", fontsize=6.6, fontweight='bold', color="#5B21B6", ha='center', va='center', zorder=4)

    # Seat C: Public Defender Advocate
    draw_academic_card(7.65, 0.60, 2.55, 1.90, "Seat C: Public Defender ($w_C = 0.30$)", header_bg="#B91C1C")
    ax.text(8.92, 1.75, "- Anti-Alarm Fatigue shield\n- Authentic OTP syntax match\n- Carrier notification templates\n- Adversarial counter-evidence",
            fontsize=6.6, color=SLATE_DARK, ha='center', va='center', zorder=4)
    ax.text(8.92, 0.88, "Output: Score $P_C \\in [0, 1]$\n+ Defender Veto Flag", fontsize=6.6, fontweight='bold', color="#991B1B", ha='center', va='center', zorder=4)

    # ------------------ COLUMN 2: CONSENSUS ENGINE & DEFENDER VETO -----------
    # Arrows from 3 seats into Consensus Engine
    draw_arrow(10.20, 5.75, 10.55, 5.75, color=STEEL, lw=1.5)
    draw_arrow(10.20, 3.65, 10.55, 3.65, color=PURPLE_TEXT, lw=1.5)
    draw_arrow(10.20, 1.55, 10.55, 1.55, color=SCAM_RED, lw=1.5)

    # Consensus Engine Card (Spans vertical height of all 3 seats!)
    draw_academic_card(10.55, 0.60, 2.35, 6.10, "Consensus & Veto Engine", header_bg=SLATE_DARK, header_h=0.42)
    ax.text(11.72, 6.25, "Weighted Fusion", fontsize=8.0, fontweight='bold', color=BORDER_CLOUD, ha='center', va='center', zorder=4)
    ax.text(11.72, 5.65, r"$P_{\mathrm{raw}} = \sum_{j} w_j P_j$" + "\n\n$w_A = 0.35$\n$w_B = 0.35$\n$w_C = 0.30$",
            fontsize=7.2, fontweight='bold', color=SLATE_DARK, ha='center', va='center', zorder=4)
    
    # Separator line inside engine
    ax.plot([10.75, 12.70], [4.65, 4.65], color="#CBD5E1", lw=1.0, zorder=4)
    
    ax.text(11.72, 4.30, "Public Defender Veto", fontsize=8.0, fontweight='bold', color=SCAM_RED, ha='center', va='center', zorder=4)
    ax.text(11.72, 3.45, "If Seat C certifies\nauthentic alert:\n\n" + r"$\delta_{\mathrm{defender}} = 0.25$" + "\n\nOffset applied to\nsuppress false alarms\n(0.00% FPR on OTPs)",
            fontsize=6.8, color=SLATE_DARK, ha='center', va='center', zorder=4)
    
    # Separator line
    ax.plot([10.75, 12.70], [2.25, 2.25], color="#CBD5E1", lw=1.0, zorder=4)
    
    ax.text(11.72, 1.95, "Final Council Score", fontsize=8.0, fontweight='bold', color="#047857", ha='center', va='center', zorder=4)
    ax.text(11.72, 1.30, r"$P_{\mathrm{council}} =$" + "\n" + r"$P_{\mathrm{raw}} - \delta_{\mathrm{def}}$",
            fontsize=7.8, fontweight='bold', color=SLATE_DARK, ha='center', va='center', zorder=4)

    # ------------------ COLUMN 3: STANDARDIZED 3-LABEL VERDICTS --------------
    # Arrows from Consensus Engine to 3 Verdict Cards
    draw_arrow(12.90, 5.75, 13.25, 5.75, color=SCAM_RED, lw=1.6)
    draw_arrow(12.90, 3.65, 13.25, 3.65, color=WARN_AMBER, lw=1.6)
    draw_arrow(12.90, 1.55, 13.25, 1.55, color=HAM_GREEN, lw=1.6)

    # Verdict 1: SCAM-RISK
    draw_academic_card(13.25, 4.80, 2.15, 1.90, "SCAM-RISK", header_bg=SCAM_RED, bg=SCAM_BG, border=SCAM_BORDER)
    ax.text(14.32, 6.10, r"$P_{\mathrm{council}} \geq 0.60$", fontsize=8.2, fontweight='bold', color=SCAM_RED, ha='center', va='center', zorder=4)
    ax.text(14.32, 5.45, "Critical Threat Level\n\nImmediate Threat Alert\nand Quarantine\nof SMS Message",
            fontsize=6.8, color=SCAM_TEXT, ha='center', va='center', zorder=4)

    # Verdict 2: UNKNOWN
    draw_academic_card(13.25, 2.70, 2.15, 1.90, "UNKNOWN", header_bg=WARN_AMBER, bg=WARN_BG, border=WARN_BORDER)
    ax.text(14.32, 4.00, r"$0.40 \leq P_{\mathrm{c}} < 0.60$", fontsize=7.8, fontweight='bold', color=WARN_AMBER, ha='center', va='center', zorder=4)
    ax.text(14.32, 3.35, "Ambiguous Boundary\n\nCautious Abstention\nAsync Security Triage\n& Human Inspection",
            fontsize=6.8, color=WARN_TEXT, ha='center', va='center', zorder=4)

    # Verdict 3: LOW-RISK
    draw_academic_card(13.25, 0.60, 2.15, 1.90, "LOW-RISK", header_bg=HAM_GREEN, bg=HAM_BG, border=HAM_BORDER)
    ax.text(14.32, 1.90, r"$P_{\mathrm{council}} < 0.40$", fontsize=8.2, fontweight='bold', color=HAM_GREEN, ha='center', va='center', zorder=4)
    ax.text(14.32, 1.25, "Authentic Notification\n\nVerified Bank / OTP\nDelivered Safely to\nSubscriber Inbox",
            fontsize=6.8, color=HAM_TEXT, ha='center', va='center', zorder=4)

    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    plt.savefig(output_png, dpi=dpi, bbox_inches='tight', pad_inches=0.04)
    plt.close()
    print(f"Publication-grade architecture diagram saved cleanly to {output_png}!")

if __name__ == "__main__":
    create_publication_figure()
