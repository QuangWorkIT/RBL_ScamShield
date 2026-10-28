import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

def create_monochrome_publication_figure(output_png="paper/figures/pipeline_architecture.png", dpi=300):
    # Set strict academic font styling
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'mathtext.fontset': 'dejavusans',
        'text.color': '#000000',
        'figure.autolayout': False,
    })

    # Dimensions: 16.0 inches x 8.4 inches (Publication Grade Monochrome)
    fig, ax = plt.subplots(figsize=(16.0, 8.4), dpi=dpi)
    ax.set_xlim(0, 16.0)
    ax.set_ylim(0, 8.4)
    ax.axis('off')

    # Strict Grayscale Palette
    BLACK = "#000000"
    CHARCOAL = "#262626"      # Very dark gray / near black for headers
    DARK_GRAY = "#404040"     # Borders and subheaders
    MID_GRAY = "#737373"      # Secondary annotations
    LIGHT_GRAY = "#E5E5E5"    # Subtle background fill / dividers
    VERY_LIGHT_GRAY = "#F5F5F5"# Card body background
    WHITE = "#FFFFFF"

    # Helper function to draw an academic card with clean header and border
    def draw_mono_card(x, y, w, h, title, header_bg=CHARCOAL, header_fg=WHITE, header_h=0.38, bg=WHITE, border=BLACK, lw=1.2, radius=0.06):
        # Base card
        card = FancyBboxPatch((x, y), w, h,
                              boxstyle=f"round,pad=0,rounding_size={radius}",
                              facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
        ax.add_patch(card)
        
        # Header banner (clipped to top of card)
        header = FancyBboxPatch((x, y + h - header_h), w, header_h,
                               boxstyle=f"round,pad=0,rounding_size={radius}",
                               facecolor=header_bg, edgecolor=border, linewidth=lw, zorder=3)
        ax.add_patch(header)
        fill_rect = Rectangle((x, y + h - header_h), w, header_h * 0.4,
                              facecolor=header_bg, edgecolor=header_bg, linewidth=0, zorder=3)
        ax.add_patch(fill_rect)
        # Separator line under header
        ax.plot([x, x + w], [y + h - header_h, y + h - header_h], color=border, linewidth=lw, zorder=4)
        
        # Header text
        ax.text(x + w / 2.0, y + h - header_h / 2.0, title,
                fontsize=8.0, fontweight='bold', color=header_fg, ha='center', va='center', zorder=5)

    # Helper function to draw crisp straight arrows
    def draw_mono_arrow(x1, y1, x2, y2, color=BLACK, lw=1.5, zorder=6):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle="-|>",
                                mutation_scale=12,
                                color=color, linewidth=lw, zorder=zorder)
        ax.add_patch(arrow)

    # =========================================================================
    # 0. MAIN FIGURE TITLE BANNER
    # =========================================================================
    title_box = FancyBboxPatch((0.4, 7.70), 15.2, 0.48,
                               boxstyle="round,pad=0,rounding_size=0.06",
                               facecolor=CHARCOAL, edgecolor=BLACK, linewidth=1.2, zorder=2)
    ax.add_patch(title_box)
    ax.text(8.0, 7.94, "ScamShield-VN: Two-Tier Edge-Cloud Architecture & Triage Operational Flow",
            fontsize=11.0, fontweight='bold', color=WHITE, ha='center', va='center', zorder=3)

    # =========================================================================
    # 1. TIER BOUNDARY CONTAINERS (DEVICE vs CLOUD) - MONOCHROME
    # =========================================================================
    # Left Boundary: Client Mobile Device
    dev_box = FancyBboxPatch((0.4, 0.35), 6.6, 7.15,
                             boxstyle="round,pad=0,rounding_size=0.12",
                             facecolor=WHITE, edgecolor=DARK_GRAY, linewidth=1.5, linestyle="--", zorder=1)
    ax.add_patch(dev_box)
    
    ax.text(0.65, 7.28, "CLIENT MOBILE DEVICE BOUNDARY (TIER 1 SCREENING)",
            fontsize=9.2, fontweight='bold', color=BLACK, ha='left', va='center', zorder=3)
    ax.text(0.65, 7.04, "On-Device Inference  •  Sub-100 ms CPU Latency  •  Local Privacy Preservation",
            fontsize=7.6, color=DARK_GRAY, ha='left', va='center', zorder=3)

    # Right Boundary: Secure Cloud Infrastructure
    cloud_box = FancyBboxPatch((7.3, 0.35), 8.3, 7.15,
                               boxstyle="round,pad=0,rounding_size=0.12",
                               facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, linestyle="--", zorder=1)
    ax.add_patch(cloud_box)
    
    ax.text(7.55, 7.28, "SECURE CLOUD BACKEND BOUNDARY (TIER 2 FORENSIC COUNCIL)",
            fontsize=9.2, fontweight='bold', color=BLACK, ha='left', va='center', zorder=3)
    ax.text(7.55, 7.04, "Escalated Ambiguous Lures (3.4%)  •  Multi-Agent Deliberation  •  Adversarial Public Defender Veto",
            fontsize=7.6, color=DARK_GRAY, ha='left', va='center', zorder=3)

    # =========================================================================
    # 2. DEVICE: TOP ROW - INGESTION, SCREENING, ROUTING
    # =========================================================================
    # Card 1: Incoming SMS Input
    draw_mono_card(0.60, 4.30, 1.45, 2.45, "1. Incoming SMS", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.38)
    ax.text(1.32, 5.95, "SMS Message $x$", fontsize=8.2, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(1.32, 5.25, "Raw message stream:\n• Vietnamese text\n• Slang & teencode\n• URLs / Shortlinks\n• Banking OTP lures",
            fontsize=7.0, color=DARK_GRAY, ha='center', va='center', zorder=4)
    ax.text(1.32, 4.52, "[ Mobile Client ]", fontsize=6.5, fontstyle='italic', color=MID_GRAY, ha='center', va='center', zorder=4)

    # Arrow 1 -> 2
    draw_mono_arrow(2.05, 5.52, 2.40, 5.52, color=BLACK, lw=1.8)

    # Card 2: Tier 1 ViSoBERT Edge Screener
    draw_mono_card(2.40, 4.10, 2.25, 2.65, "2. Tier 1 Edge Screener", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.38)
    # Notice: Header is [6.37, 6.75]. Highest body text is at 6.00 (0.37 margin below header!)
    ax.text(3.52, 6.02, "ViSoBERT INT8", fontsize=8.5, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(3.52, 5.75, "Cost-Sensitive Loss ($\\alpha = 5.0$)", fontsize=7.4, fontweight='bold', color=DARK_GRAY, ha='center', va='center', zorder=4)
    ax.text(3.52, 5.12, "• 110M Parameters (98.4 MB)\n• CPU Latency: 70.7 ms (ONNX)\n• 5x loss weight on missed scams\n• Frozen Test Scam Recall: 95.62%",
            fontsize=6.8, color=BLACK, ha='center', va='center', zorder=4)
    ax.text(3.52, 4.38, "Output: Score $P_{\\mathrm{T1}} \\in [0, 1]$\nConfidence: $C_{\\mathrm{T1}} = \\max(P, 1-P)$",
            fontsize=7.0, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)

    # Arrow 2 -> 3
    draw_mono_arrow(4.65, 5.52, 5.00, 5.52, color=BLACK, lw=1.8)

    # Card 3: Confidence Router
    draw_mono_card(5.00, 4.30, 1.85, 2.45, "3. Confidence Router", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.38)
    ax.text(5.92, 5.95, "Operating Point $\\tau = 0.90$", fontsize=7.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(5.92, 5.25, "Routing Rule:\nIs $C_{\\mathrm{T1}}(x) \\geq \\tau$?\n\nHigh Confidence\nvs. Ambiguous Lure",
            fontsize=7.0, color=BLACK, ha='center', va='center', zorder=4)
    ax.text(5.92, 4.52, "[ Exploratory Setpoint ]", fontsize=6.5, fontstyle='italic', color=MID_GRAY, ha='center', va='center', zorder=4)

    # =========================================================================
    # 3. DEVICE: BOTTOM ROW - FAST PATH & CLIENT PII SANITIZER
    # =========================================================================
    # Fast Path Branch (YES, 96.6%): Arrow from Router down-left to Fast Path Card
    draw_mono_arrow(5.45, 4.30, 5.45, 3.90, color=BLACK, lw=1.6)
    draw_mono_arrow(5.45, 3.90, 3.95, 3.90, color=BLACK, lw=1.6)
    draw_mono_arrow(3.95, 3.90, 3.95, 3.65, color=BLACK, lw=1.6)
    ax.text(4.70, 4.05, "Yes: Confident (96.6%)", fontsize=7.0, fontweight='bold', color=BLACK, ha='center', va='bottom', zorder=6)

    # Card 4: Fast-Path Local Decision
    draw_mono_card(0.60, 0.55, 3.45, 3.10, "Fast-Path Edge Resolution (96.6% Local)", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.38, bg=VERY_LIGHT_GRAY)
    ax.text(2.32, 2.95, "Confident Edge Decision ($C_{\\mathrm{T1}} \\geq 0.90$)", fontsize=7.6, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(2.32, 2.65, "Sub-100 ms Total Latency  •  Zero Cloud API Cost", fontsize=7.0, color=DARK_GRAY, ha='center', va='center', zorder=4)
    
    # Sub-card: High-Risk Scam
    draw_mono_card(0.75, 1.60, 3.15, 0.85, "High-Risk Scam ($P_{\\mathrm{T1}} \\geq 0.90$)", header_bg=LIGHT_GRAY, header_fg=BLACK, header_h=0.28, bg=WHITE)
    ax.text(2.32, 1.90, "Immediate Local Quarantine & Threat Alert", fontsize=6.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)

    # Sub-card: Benign Alert
    draw_mono_card(0.75, 0.68, 3.15, 0.85, "Benign Alert ($P_{\\mathrm{T1}} \\leq 0.10$)", header_bg=LIGHT_GRAY, header_fg=BLACK, header_h=0.28, bg=WHITE)
    ax.text(2.32, 0.98, "Normal Delivery to Subscriber Inbox", fontsize=6.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)

    # Escalation Branch (NO, 3.4%): Arrow from Router down to PII Sanitizer
    draw_mono_arrow(6.40, 4.30, 6.40, 3.65, color=BLACK, lw=1.6)
    ax.text(6.45, 3.98, "No: Ambiguous (3.4%)\nEscalate to Council", fontsize=7.0, fontweight='bold', color=BLACK, ha='left', va='center', zorder=6)

    # Card 5: Client-Side Privacy Sanitizer
    draw_mono_card(4.25, 0.55, 2.60, 3.10, "4. Privacy Sanitizer", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.38, bg=WHITE)
    ax.text(5.55, 2.95, "MessagePIISanitizer", fontsize=7.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(5.55, 2.62, "Local Pre-Transmission Redaction:\n(0.03 ms Regex Latency)", fontsize=6.8, color=DARK_GRAY, ha='center', va='center', zorder=4)
    ax.text(5.55, 1.85, "• Phone $\\rightarrow$ [PHONE_REDACTED]\n• Bank Acct $\\rightarrow$ [ACCT_REDACTED]\n• Citizen ID $\\rightarrow$ [ID_REDACTED]\n• OTP Code $\\rightarrow$ [OTP_REDACTED]",
            fontsize=6.7, color=BLACK, ha='center', va='center', zorder=4)
    ax.text(5.55, 0.95, "Zero plaintext credentials\nleave the mobile client\n(Article 25 Motivation)", fontsize=6.5, fontstyle='italic', color=DARK_GRAY, ha='center', va='center', zorder=4)

    # Sanitized Lure crosses Boundary into Cloud
    draw_mono_arrow(6.85, 2.10, 7.50, 2.10, color=BLACK, lw=2.0)
    ax.text(7.17, 2.32, "Sanitized Lure\n(3.4% Traffic)", fontsize=7.0, fontweight='bold', color=BLACK, ha='center', va='bottom', zorder=6)

    # =========================================================================
    # 4. CLOUD: 3 COLUMNS (SPECIALISTS -> CONSENSUS -> 3-LABEL VERDICTS)
    # =========================================================================
    
    # ------------------ COLUMN 1: 3 SPECIALIST SEATS -------------------------
    # Ingress distribution bus: from (7.50, 2.10) distribute vertically to 3 seats
    draw_mono_arrow(7.50, 2.10, 7.50, 5.95, color=BLACK, lw=1.6)
    draw_mono_arrow(7.50, 5.95, 7.65, 5.95, color=BLACK, lw=1.5) # to Seat A
    draw_mono_arrow(7.50, 3.70, 7.65, 3.70, color=BLACK, lw=1.5) # to Seat B
    draw_mono_arrow(7.50, 1.45, 7.65, 1.45, color=BLACK, lw=1.5) # to Seat C

    # Seat A: Cyber-Financial Analyst
    draw_mono_card(7.65, 4.95, 2.70, 1.95, "Seat A: Cyber-Financial ($w_A = 0.35$)", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.35)
    # Header is [6.55, 6.90]. Body text begins at 6.15 (0.40 margin!)
    ax.text(9.00, 6.10, "• Brand spoofing & domain typos\n• Malicious link structure & APKs\n• Fake OTT / VNeID app lures\n• SBV 2345/QD-NHNN compliance",
            fontsize=6.6, color=BLACK, ha='center', va='center', zorder=4)
    ax.text(9.00, 5.25, "Output: Score $P_A \\in [0, 1]$\n+ Technical Forensics", fontsize=6.6, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)

    # Seat B: Psycholinguistic Specialist
    draw_mono_card(7.65, 2.70, 2.70, 1.95, "Seat B: Psycholinguistic ($w_B = 0.35$)", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.35)
    ax.text(9.00, 3.85, "• Urgency & fear extortion cues\n• Police / court summon pretext\n• Vietnamese teencode & slang\n• Emotional manipulation trace",
            fontsize=6.6, color=BLACK, ha='center', va='center', zorder=4)
    ax.text(9.00, 3.00, "Output: Score $P_B \\in [0, 1]$\n+ Behavioral Traces", fontsize=6.6, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)

    # Seat C: Public Defender Advocate
    draw_mono_card(7.65, 0.45, 2.70, 1.95, "Seat C: Public Defender ($w_C = 0.30$)", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.35)
    ax.text(9.00, 1.60, "• Anti-Alarm Fatigue shield\n• Authentic OTP syntax match\n• Carrier notification templates\n• Adversarial counter-evidence",
            fontsize=6.6, color=BLACK, ha='center', va='center', zorder=4)
    ax.text(9.00, 0.75, "Output: Score $P_C \\in [0, 1]$\n+ Defender Veto Flag", fontsize=6.6, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)

    # ------------------ COLUMN 2: CONSENSUS ENGINE & DEFENDER VETO -----------
    # Arrows from 3 seats into Consensus Engine
    draw_mono_arrow(10.35, 5.95, 10.70, 5.95, color=BLACK, lw=1.5)
    draw_mono_arrow(10.35, 3.70, 10.70, 3.70, color=BLACK, lw=1.5)
    draw_mono_arrow(10.35, 1.45, 10.70, 1.45, color=BLACK, lw=1.5)

    # Consensus Engine Card (Spans vertical height of all 3 seats!)
    draw_mono_card(10.70, 0.45, 2.35, 6.45, "Consensus & Veto Engine", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.40)
    # Header is [6.50, 6.90].
    # CRITICAL: Section 1 (Weighted Fusion) starts at 6.10 (0.40 below header!)
    ax.text(11.87, 6.10, "Weighted Fusion", fontsize=7.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(11.87, 5.50, r"$P_{\mathrm{raw}} = \sum_{j} w_j P_j$" + "\n\n$w_A = 0.35$\n$w_B = 0.35$\n$w_C = 0.30$",
            fontsize=7.2, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    
    # Separator line inside engine
    ax.plot([10.90, 12.85], [4.65, 4.65], color=DARK_GRAY, lw=1.0, linestyle=":", zorder=4)
    
    ax.text(11.87, 4.25, "Public Defender Veto", fontsize=7.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(11.87, 3.40, "If Seat C certifies\nauthentic alert:\n\n" + r"$\delta_{\mathrm{defender}} = 0.25$" + "\n\nOffset applied to\nsuppress false alarms\n(0.00% FPR on OTPs)",
            fontsize=6.8, color=BLACK, ha='center', va='center', zorder=4)
    
    # Separator line
    ax.plot([10.90, 12.85], [2.25, 2.25], color=DARK_GRAY, lw=1.0, linestyle=":", zorder=4)
    
    ax.text(11.87, 1.95, "Final Council Score", fontsize=7.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(11.87, 1.30, r"$P_{\mathrm{council}} =$" + "\n" + r"$P_{\mathrm{raw}} - \delta_{\mathrm{def}}$",
            fontsize=7.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)

    # ------------------ COLUMN 3: STANDARDIZED 3-LABEL VERDICTS --------------
    # Arrows from Consensus Engine to 3 Verdict Cards
    draw_mono_arrow(13.05, 5.95, 13.40, 5.95, color=BLACK, lw=1.6)
    draw_mono_arrow(13.05, 3.70, 13.40, 3.70, color=BLACK, lw=1.6)
    draw_mono_arrow(13.05, 1.45, 13.40, 1.45, color=BLACK, lw=1.6)

    # Verdict 1: SCAM-RISK
    draw_mono_card(13.40, 4.95, 2.05, 1.95, "SCAM-RISK", header_bg=CHARCOAL, header_fg=WHITE, header_h=0.35, bg=WHITE)
    ax.text(14.42, 6.15, r"$P_{\mathrm{council}} \geq 0.60$", fontsize=8.2, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(14.42, 5.45, "Critical Threat Level\n\nImmediate Threat Alert\nand Quarantine\nof SMS Message",
            fontsize=6.8, color=BLACK, ha='center', va='center', zorder=4)

    # Verdict 2: UNKNOWN
    draw_mono_card(13.40, 2.70, 2.05, 1.95, "UNKNOWN", header_bg=LIGHT_GRAY, header_fg=BLACK, header_h=0.35, bg=WHITE)
    ax.text(14.42, 3.90, r"$0.40 \leq P_{\mathrm{c}} < 0.60$", fontsize=7.8, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(14.42, 3.20, "Ambiguous Boundary\n\nCautious Abstention\nAsync Security Triage\n& Human Inspection",
            fontsize=6.8, color=BLACK, ha='center', va='center', zorder=4)

    # Verdict 3: LOW-RISK
    draw_mono_card(13.40, 0.45, 2.05, 1.95, "LOW-RISK", header_bg=LIGHT_GRAY, header_fg=BLACK, header_h=0.35, bg=WHITE)
    ax.text(14.42, 1.65, r"$P_{\mathrm{council}} < 0.40$", fontsize=8.2, fontweight='bold', color=BLACK, ha='center', va='center', zorder=4)
    ax.text(14.42, 0.95, "Authentic Notification\n\nVerified Bank / OTP\nDelivered Safely to\nSubscriber Inbox",
            fontsize=6.8, color=BLACK, ha='center', va='center', zorder=4)

    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    plt.savefig(output_png, dpi=dpi, bbox_inches='tight', pad_inches=0.04)
    plt.close()
    print(f"Monochrome publication-grade architecture diagram saved cleanly to {output_png}!")

if __name__ == "__main__":
    create_monochrome_publication_figure()
