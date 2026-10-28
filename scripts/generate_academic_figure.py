import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

def create_publication_figure(output_png="paper/figures/pipeline_architecture.png", dpi=300):
    # Set academic font styling
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'mathtext.fontset': 'dejavusans',
        'text.color': '#0F172A',
        'axes.edgecolor': '#94A3B8',
    })

    # High aspect ratio suitable for 2-column IEEE/JAIT template (\textwidth)
    # 15 inches width x 6.8 inches height
    fig, ax = plt.subplots(figsize=(15.0, 6.8), dpi=dpi)
    ax.set_xlim(0, 15.0)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    # Color Palette: Refined, elegant, academic palette
    COLOR_CARD_BORDER = "#CBD5E1"     # Slate 300
    
    PRIMARY_BLUE = "#1E40AF"        # Blue 800
    ACCENT_BLUE = "#2563EB"         # Blue 600
    LIGHT_BLUE = "#EFF6FF"          # Blue 50
    BORDER_BLUE = "#93C5FD"         # Blue 300
    
    GREEN_FILL = "#F0FDF4"          # Emerald 50
    GREEN_BORDER = "#10B981"        # Emerald 500
    GREEN_TEXT = "#065F46"          # Emerald 800
    
    RED_FILL = "#FEF2F2"            # Red 50
    RED_BORDER = "#EF4444"          # Red 500
    RED_TEXT = "#991B1B"            # Red 800
    
    AMBER_FILL = "#FFFBEB"          # Amber 50
    AMBER_BORDER = "#F59E0B"        # Amber 500
    AMBER_TEXT = "#92400E"          # Amber 800
    
    PURPLE_FILL = "#FAF5FF"         # Purple 50
    PURPLE_BORDER = "#A855F7"       # Purple 500
    PURPLE_TEXT = "#6B21A8"         # Purple 800

    def draw_card(x, y, w, h, bg="#FFFFFF", border=COLOR_CARD_BORDER, radius=0.12, lw=1.2, zorder=2):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad=0,rounding_size={radius}",
                             facecolor=bg, edgecolor=border, linewidth=lw, zorder=zorder)
        ax.add_patch(box)
        return box

    def draw_arrow(x1, y1, x2, y2, color="#475569", lw=1.5, rad=0.0, zorder=5):
        if rad == 0.0:
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                    arrowstyle="-|>",
                                    mutation_scale=13,
                                    color=color, linewidth=lw, zorder=zorder)
        else:
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                    connectionstyle=f"arc3,rad={rad}",
                                    arrowstyle="-|>",
                                    mutation_scale=13,
                                    color=color, linewidth=lw, zorder=zorder)
        ax.add_patch(arrow)

    # =========================================================================
    # 1. TIER BOUNDARY CONTAINERS (DEVICE vs CLOUD)
    # =========================================================================
    # Mobile Device Boundary
    dev_box = FancyBboxPatch((0.2, 0.35), 6.8, 6.25,
                             boxstyle="round,pad=0,rounding_size=0.25",
                             facecolor="#F8FAFC", edgecolor="#64748B", linewidth=1.5, linestyle="--", zorder=1)
    ax.add_patch(dev_box)
    
    # Device Header Title
    ax.text(0.45, 6.30, "ON-DEVICE SECURITY BOUNDARY (TIER 1 SCREENING)", 
            fontsize=10.5, fontweight='bold', color="#0F172A", ha='left', va='center', zorder=3)
    ax.text(0.45, 6.05, "Local Mobile Execution  •  Sub-100 ms CPU Latency  •  Zero Cloud Exposure for 96.6% of Traffic", 
            fontsize=8.0, color="#64748B", ha='left', va='center', zorder=3)

    # Cloud Boundary
    cloud_box = FancyBboxPatch((7.3, 0.35), 7.5, 6.25,
                               boxstyle="round,pad=0,rounding_size=0.25",
                               facecolor="#F8FAFC", edgecolor="#2563EB", linewidth=1.5, linestyle="--", zorder=1)
    ax.add_patch(cloud_box)
    
    # Cloud Header Title
    ax.text(7.55, 6.30, "SECURE CLOUD BOUNDARY (TIER 2 FORENSIC COUNCIL)", 
            fontsize=10.5, fontweight='bold', color="#1E40AF", ha='left', va='center', zorder=3)
    ax.text(7.55, 6.05, "Sanitized Escalation  •  Occam 3-Agent Forensic Deliberation  •  Adversarial Public Defender Veto", 
            fontsize=8.0, color="#64748B", ha='left', va='center', zorder=3)

    # =========================================================================
    # 2. INPUT MESSAGE
    # =========================================================================
    draw_card(0.4, 3.8, 1.35, 1.8, bg="#FFFFFF", border="#2563EB", lw=1.5)
    ax.text(1.07, 5.25, "Incoming SMS", fontsize=9.2, fontweight='bold', color="#1E40AF", ha='center', va='center', zorder=4)
    ax.text(1.07, 4.65, "Raw Message $x$\n• Vietnamese text\n• Slang & teencode\n• URLs / shortlinks\n• Brand OTP alerts", 
            fontsize=7.5, color="#334155", ha='center', va='center', zorder=4)
    ax.text(1.07, 4.05, "[ Mobile Client ]", fontsize=7.0, fontweight='bold', color="#94A3B8", ha='center', va='center', zorder=4)

    # Arrow from Input to Tier 1 Screener
    draw_arrow(1.75, 4.70, 2.15, 4.70, color="#1E40AF", lw=1.8)

    # =========================================================================
    # 3. TIER 1: ViSoBERT EDGE SCREENER
    # =========================================================================
    draw_card(2.15, 3.5, 2.25, 2.3, bg=LIGHT_BLUE, border=BORDER_BLUE, lw=1.5)
    ax.text(3.27, 5.50, "Tier 1: Edge Screener", fontsize=9.2, fontweight='bold', color="#1E3A8A", ha='center', va='center', zorder=4)
    ax.text(3.27, 5.15, "ViSoBERT + Cost-Sensitive WBCE\nONNX Runtime INT8 ($98.4$ MB)", 
            fontsize=7.8, fontweight='bold', color="#2563EB", ha='center', va='center', zorder=4)
    ax.text(3.27, 4.60, "• Penalty weight: $\\alpha = 5.0$ on missed scam\n• Latency: $70.7$ ms (CPU INT8)\n• Frozen Test Scam Recall: $95.62\%$", 
            fontsize=7.3, color="#334155", ha='center', va='center', zorder=4)
    ax.text(3.27, 3.90, "Risk Score $P_{\\mathrm{T1}} \\in [0, 1]$\nConfidence $C_{\\mathrm{T1}} = \\max(P_{\\mathrm{T1}}, 1 - P_{\\mathrm{T1}})$", 
            fontsize=7.4, fontweight='bold', color="#0F172A", ha='center', va='center', zorder=4)

    # Arrow to Router
    draw_arrow(4.40, 4.70, 4.75, 4.70, color="#1E40AF", lw=1.8)

    # =========================================================================
    # 4. CONFIDENCE ROUTER
    # =========================================================================
    draw_card(4.75, 3.7, 2.05, 1.9, bg="#FFFFFF", border="#64748B", lw=1.5)
    ax.text(5.77, 5.30, "Confidence Router", fontsize=9.0, fontweight='bold', color="#0F172A", ha='center', va='center', zorder=4)
    ax.text(5.77, 4.95, "Operating Point $\\tau = 0.90$", fontsize=8.0, fontweight='bold', color="#2563EB", ha='center', va='center', zorder=4)
    ax.text(5.77, 4.45, "Is $C_{\\mathrm{T1}}(x) \\geq \\tau$?\n(Unambiguous Prediction)", fontsize=7.5, color="#334155", ha='center', va='center', zorder=4)
    ax.text(5.77, 3.95, "[ Exploratory Setpoint ]", fontsize=7.0, fontstyle='italic', color="#94A3B8", ha='center', va='center', zorder=4)

    # Fast-Path Branch -> DOWN to Fast-Path Box
    draw_arrow(5.3, 3.7, 5.3, 3.1, color="#10B981", lw=1.8)
    ax.text(5.35, 3.40, " Yes (96.6%)\n Confident", fontsize=7.2, fontweight='bold', color="#059669", ha='left', va='center', zorder=6)

    # =========================================================================
    # 5. FAST-PATH LOCAL VERDICT BOX
    # =========================================================================
    draw_card(2.15, 1.85, 4.65, 1.25, bg=GREEN_FILL, border=GREEN_BORDER, lw=1.5)
    ax.text(4.47, 2.80, "FAST-PATH LOCAL EDGE RESOLUTION (96.6% OF TRAFFIC)", 
            fontsize=8.5, fontweight='bold', color=GREEN_TEXT, ha='center', va='center', zorder=4)
    ax.text(4.47, 2.45, "Confident Local Verdict ($C_{\\mathrm{T1}} \\geq 0.90$)  •  Latency: Sub-100 ms  •  Cost: $0.00\n"
                        "Verdict: High-Risk Scam ($P_{\\mathrm{T1}} \\geq 0.90$) or Benign Alert ($P_{\\mathrm{T1}} \\leq 0.10$)", 
            fontsize=7.4, color="#047857", ha='center', va='center', zorder=4)
    ax.text(4.47, 2.05, "Immediate Local User Block or Inbox Delivery  •  Zero Cloud Overhead", 
            fontsize=7.0, fontweight='bold', color="#059669", ha='center', va='center', zorder=4)

    # Escalation Branch -> DOWN to PII Sanitizer
    draw_arrow(6.3, 3.7, 6.3, 1.45, color="#D97706", lw=1.8)
    draw_arrow(6.3, 1.45, 5.85, 1.45, color="#D97706", lw=1.8)
    ax.text(6.35, 2.50, " No (3.4%)\n Ambiguous\n ($C_{\\mathrm{T1}} < \\tau$)", 
            fontsize=7.2, fontweight='bold', color="#D97706", ha='left', va='center', zorder=6)

    # =========================================================================
    # 6. CLIENT-SIDE PII SANITIZER (Inside Device Boundary)
    # =========================================================================
    draw_card(0.4, 0.55, 5.4, 1.05, bg=LIGHT_BLUE, border=BORDER_BLUE, lw=1.4)
    ax.text(3.1, 1.35, "Client-Side Privacy Sanitizer (MessagePIISanitizer)", 
            fontsize=8.5, fontweight='bold', color="#1E40AF", ha='center', va='center', zorder=4)
    ax.text(3.1, 1.00, "Pre-transmission regex masking (0.03 ms):\n"
                       "Phone $\\rightarrow$ [PHONE_REDACTED], Bank Account $\\rightarrow$ [ACCT_REDACTED], CCCD $\\rightarrow$ [ID_REDACTED], OTP $\\rightarrow$ [OTP_REDACTED]", 
            fontsize=7.0, color="#334155", ha='center', va='center', zorder=4)
    ax.text(3.1, 0.70, "Guarantees zero plaintext financial or identity identifiers leave the user device", 
            fontsize=6.8, fontweight='bold', color="#2563EB", ha='center', va='center', zorder=4)

    # Cross-Boundary Arrow from Sanitizer to Cloud Council
    draw_arrow(5.8, 1.07, 7.5, 1.07, color="#1E40AF", lw=2.0)
    ax.text(6.65, 1.25, "Sanitized Lure\n(3.4% Traffic)", fontsize=7.2, fontweight='bold', color="#1E40AF", ha='center', va='bottom', zorder=6)

    # =========================================================================
    # 7. TIER 2: OCCAM 3-AGENT SPECIALIST COUNCIL (Cloud Boundary)
    # =========================================================================
    panel_box = FancyBboxPatch((7.5, 2.75), 7.1, 3.0,
                               boxstyle="round,pad=0,rounding_size=0.18",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2, zorder=2)
    ax.add_patch(panel_box)
    ax.text(11.05, 5.50, "Tier 2: Occam-Optimized 3-Agent Forensic Specialist Council", 
            fontsize=9.2, fontweight='bold', color="#0F172A", ha='center', va='center', zorder=4)

    # Seat A: Cyber-Financial Specialist
    draw_card(7.65, 2.95, 2.2, 2.3, bg=LIGHT_BLUE, border="#3B82F6", lw=1.2)
    ax.text(8.75, 4.98, "SEAT A ($w_A = 0.35$)\nCyber-Financial", fontsize=8.0, fontweight='bold', color="#1E40AF", ha='center', va='center', zorder=4)
    ax.text(8.75, 4.35, "• Brand spoofing & homoglyphs\n• Malicious link/URL structure\n• Fake OTT / VNeID app lures\n• SBV 2345/QD-NHNN compliance", 
            fontsize=6.8, color="#334155", ha='center', va='center', zorder=4)
    ax.text(8.75, 3.25, "Output: Risk score $P_A \\in [0, 1]$\n+ Forensic Technical Rationale", 
            fontsize=6.7, fontweight='bold', color="#1E40AF", ha='center', va='center', zorder=4)

    # Seat B: Psycholinguistic Specialist
    draw_card(9.95, 2.95, 2.2, 2.3, bg=PURPLE_FILL, border=PURPLE_BORDER, lw=1.2)
    ax.text(11.05, 4.98, "SEAT B ($w_B = 0.35$)\nPsycholinguistic", fontsize=8.0, fontweight='bold', color=PURPLE_TEXT, ha='center', va='center', zorder=4)
    ax.text(11.05, 4.35, "• Urgency & fear extortion cues\n• Police / court summon pretext\n• Vietnamese teencode & slang\n• Lottery & prize pretexts", 
            fontsize=6.8, color="#334155", ha='center', va='center', zorder=4)
    ax.text(11.05, 3.25, "Output: Risk score $P_B \\in [0, 1]$\n+ Behavioral Manipulation Trace", 
            fontsize=6.7, fontweight='bold', color=PURPLE_TEXT, ha='center', va='center', zorder=4)

    # Seat C: Public Defender Advocate
    draw_card(12.25, 2.95, 2.2, 2.3, bg=RED_FILL, border=RED_BORDER, lw=1.2)
    ax.text(13.35, 4.98, "SEAT C ($w_C = 0.30$)\nPublic Defender", fontsize=8.0, fontweight='bold', color=RED_TEXT, ha='center', va='center', zorder=4)
    ax.text(13.35, 4.35, "• Anti-Alarm Fatigue shield\n• Authentic OTP syntax check\n• Telecom carrier template match\n• Adversarial counter-evidence", 
            fontsize=6.8, color="#334155", ha='center', va='center', zorder=4)
    ax.text(13.35, 3.25, "Output: Risk score $P_C \\in [0, 1]$\n+ Defender Veto Flag", 
            fontsize=6.7, fontweight='bold', color=RED_TEXT, ha='center', va='center', zorder=4)

    # Route sanitized lure to 3 seats
    draw_arrow(7.5, 1.07, 7.5, 2.1, color="#1E40AF", lw=1.5)
    draw_arrow(7.5, 2.1, 8.75, 2.90, color="#1E40AF", lw=1.2, rad=-0.08)
    draw_arrow(7.5, 2.1, 11.05, 2.90, color=PURPLE_TEXT, lw=1.2)
    draw_arrow(7.5, 2.1, 13.35, 2.90, color=RED_TEXT, lw=1.2, rad=0.08)

    # =========================================================================
    # 8. WEIGHTED CONSENSUS & DEFENDER VETO
    # =========================================================================
    draw_card(7.5, 1.75, 7.1, 0.85, bg="#FFFFFF", border="#475569", lw=1.3)
    ax.text(11.05, 2.38, "Weighted Consensus Aggregation with Public Defender Veto", 
            fontsize=8.5, fontweight='bold', color="#0F172A", ha='center', va='center', zorder=4)
    ax.text(11.05, 2.02, 
            r"$P_{\mathrm{council}} = \left( \sum_{j \in \{A, B, C\}} w_j P_j \right) - \delta_{\mathrm{defender}}$"
            r"    where $\delta_{\mathrm{defender}} = 0.25$ if Seat C certifies authentic bank/carrier notification",
            fontsize=7.3, fontweight='bold', color="#1E293B", ha='center', va='center', zorder=4)

    # Arrows from 3 seats down to consensus box
    draw_arrow(8.75, 2.95, 8.75, 2.62, color="#1E40AF", lw=1.2)
    draw_arrow(11.05, 2.95, 11.05, 2.62, color=PURPLE_TEXT, lw=1.2)
    draw_arrow(13.35, 2.95, 13.35, 2.62, color=RED_TEXT, lw=1.2)

    # Arrow from consensus to 3-Label Output
    draw_arrow(11.05, 1.75, 11.05, 1.50, color="#475569", lw=1.5)

    # =========================================================================
    # 9. STANDARDIZED 3-LABEL VERDICT PROTOCOL
    # =========================================================================
    # Label 1: SCAM-RISK
    draw_card(7.5, 0.55, 2.2, 0.88, bg=RED_FILL, border=RED_BORDER, lw=1.4)
    ax.text(8.6, 1.20, "SCAM-RISK", fontsize=8.2, fontweight='bold', color=RED_TEXT, ha='center', va='center', zorder=4)
    ax.text(8.6, 0.95, r"$P_{\mathrm{council}} \geq 0.60$", fontsize=7.5, fontweight='bold', color=RED_TEXT, ha='center', va='center', zorder=4)
    ax.text(8.6, 0.72, "User Warning + Quarantined", fontsize=6.8, color="#7F1D1D", ha='center', va='center', zorder=4)

    # Label 2: LOW-RISK
    draw_card(9.95, 0.55, 2.2, 0.88, bg=GREEN_FILL, border=GREEN_BORDER, lw=1.4)
    ax.text(11.05, 1.20, "LOW-RISK", fontsize=8.2, fontweight='bold', color=GREEN_TEXT, ha='center', va='center', zorder=4)
    ax.text(11.05, 0.95, r"$P_{\mathrm{council}} < 0.40$", fontsize=7.5, fontweight='bold', color=GREEN_TEXT, ha='center', va='center', zorder=4)
    ax.text(11.05, 0.72, "Delivered to Subscriber", fontsize=6.8, color="#064E3B", ha='center', va='center', zorder=4)

    # Label 3: UNKNOWN
    draw_card(12.4, 0.55, 2.2, 0.88, bg=AMBER_FILL, border=AMBER_BORDER, lw=1.4)
    ax.text(13.5, 1.20, "UNKNOWN", fontsize=8.2, fontweight='bold', color=AMBER_TEXT, ha='center', va='center', zorder=4)
    ax.text(13.5, 0.95, r"$0.40 \leq P_{\mathrm{council}} < 0.60$", fontsize=7.2, fontweight='bold', color=AMBER_TEXT, ha='center', va='center', zorder=4)
    ax.text(13.5, 0.72, "Cautious Abstention / SecOps", fontsize=6.8, color="#78350F", ha='center', va='center', zorder=4)

    # Connecting arrows to verdict labels
    draw_arrow(11.05, 1.50, 8.6, 1.50, color="#475569", lw=1.2)
    draw_arrow(8.6, 1.50, 8.6, 1.45, color=RED_BORDER, lw=1.2)
    
    draw_arrow(11.05, 1.50, 11.05, 1.45, color=GREEN_BORDER, lw=1.2)
    
    draw_arrow(11.05, 1.50, 13.5, 1.50, color="#475569", lw=1.2)
    draw_arrow(13.5, 1.50, 13.5, 1.45, color=AMBER_BORDER, lw=1.2)

    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    plt.savefig(output_png, dpi=dpi, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"Publication-grade architecture diagram saved cleanly to {output_png}!")

if __name__ == "__main__":
    create_publication_figure()
