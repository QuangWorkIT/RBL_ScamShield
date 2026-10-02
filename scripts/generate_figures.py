"""
SVG Vector Figure Generator for ScamShield-VN Paper (RBL-4)
Generates high-resolution vector figures (infinite DPI >= 300 DPI) for IEEE/ACM paper.
Zero external dependencies (pure Python SVG generator).
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def create_bar_chart():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="100%" height="100%">
    <style>
        .title { font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #1e293b; text-anchor: middle; }
        .axis { stroke: #94a3b8; stroke-width: 1.5; }
        .tick { font-family: Arial, sans-serif; font-size: 12px; fill: #475569; }
        .label { font-family: Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #334155; }
        .bar-visobert { fill: #2563eb; }
        .bar-baseline { fill: #64748b; }
        .bar-llm { fill: #d97706; }
        .val { font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; fill: #0f172a; text-anchor: middle; }
        .grid { stroke: #e2e8f0; stroke-dasharray: 4,4; stroke-width: 1; }
    </style>
    
    <!-- Background -->
    <rect width="800" height="450" fill="#ffffff"/>
    
    <!-- Title -->
    <text x="400" y="35" class="title">Figure 1: Scam Recall and Macro-F1 Comparison Across 5 Models (Mean ± Std)</text>
    
    <!-- Grid lines -->
    <line x1="80" y1="80" x2="750" y2="80" class="grid"/>
    <line x1="80" y1="150" x2="750" y2="150" class="grid"/>
    <line x1="80" y1="220" x2="750" y2="220" class="grid"/>
    <line x1="80" y1="290" x2="750" y2="290" class="grid"/>
    <line x1="80" y1="360" x2="750" y2="360" class="axis"/>
    <line x1="80" y1="60" x2="80" y2="360" class="axis"/>
    
    <!-- Y-axis Ticks -->
    <text x="70" y="365" class="tick" text-anchor="end">70%</text>
    <text x="70" y="295" class="tick" text-anchor="end">80%</text>
    <text x="70" y="225" class="tick" text-anchor="end">90%</text>
    <text x="70" y="85" class="tick" text-anchor="end">100%</text>
    
    <!-- Bars (x-base, Scam Recall / F1) -->
    <!-- ViSoBERT (95.62%, 92.51%) -->
    <rect x="110" y="110.6" width="45" height="249.4" class="bar-visobert" rx="3"/>
    <text x="132.5" y="103" class="val">95.6%</text>
    <rect x="160" y="132.4" width="45" height="227.6" fill="#3b82f6" rx="3"/>
    <text x="182.5" y="125" class="val">92.5%</text>
    <text x="157.5" y="385" class="tick" text-anchor="middle" font-weight="bold">ViSoBERT*</text>
    <text x="157.5" y="402" class="tick" text-anchor="middle" fill="#2563eb">(Proposed)</text>

    <!-- PhoBERT-large (92.33%, 92.70%) -->
    <rect x="240" y="133.7" width="45" height="226.3" class="bar-baseline" rx="3"/>
    <text x="262.5" y="126" class="val">92.3%</text>
    <rect x="290" y="131.1" width="45" height="228.9" fill="#94a3b8" rx="3"/>
    <text x="312.5" y="123" class="val">92.7%</text>
    <text x="287.5" y="385" class="tick" text-anchor="middle">PhoBERT-lg</text>
    <text x="287.5" y="402" class="tick" text-anchor="middle">(370M)</text>

    <!-- FPT ViBERT (92.60%, 91.25%) -->
    <rect x="370" y="131.8" width="45" height="228.2" class="bar-baseline" rx="3"/>
    <text x="392.5" y="124" class="val">92.6%</text>
    <rect x="420" y="141.2" width="45" height="218.8" fill="#94a3b8" rx="3"/>
    <text x="442.5" y="133" class="val">91.3%</text>
    <text x="417.5" y="385" class="tick" text-anchor="middle">FPT ViBERT</text>
    <text x="417.5" y="402" class="tick" text-anchor="middle">(124M)</text>

    <!-- PhoBERT-base-v2 (91.23%, 91.23%) -->
    <rect x="500" y="141.4" width="45" height="218.6" class="bar-baseline" rx="3"/>
    <text x="522.5" y="134" class="val">91.2%</text>
    <rect x="550" y="141.4" width="45" height="218.6" fill="#94a3b8" rx="3"/>
    <text x="572.5" y="134" class="val">91.2%</text>
    <text x="547.5" y="385" class="tick" text-anchor="middle">PhoBERT-v2</text>
    <text x="547.5" y="402" class="tick" text-anchor="middle">(135M)</text>

    <!-- Gemini 3.5 Flash (100.0%, 78.38%) -->
    <rect x="630" y="80.0" width="45" height="280.0" class="bar-llm" rx="3"/>
    <text x="652.5" y="72" class="val">100.0%</text>
    <rect x="680" y="231.3" width="45" height="128.7" fill="#f59e0b" rx="3"/>
    <text x="702.5" y="223" class="val">78.4%</text>
    <text x="677.5" y="385" class="tick" text-anchor="middle">Gemini 3.5</text>
    <text x="677.5" y="402" class="tick" text-anchor="middle" fill="#d97706">(Alarm Fatigue)</text>

    <!-- Legend -->
    <rect x="280" y="425" width="15" height="12" fill="#2563eb" rx="2"/>
    <text x="300" y="435" class="tick">Scam Recall (Core Target)</text>
    <rect x="470" y="425" width="15" height="12" fill="#94a3b8" rx="2"/>
    <text x="490" y="435" class="tick">F1-Score</text>
    </svg>'''
    return svg

def create_tradeoff_chart():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 500" width="100%" height="100%">
    <style>
        .title { font-family: Arial, sans-serif; font-size: 17px; font-weight: bold; fill: #0f172a; text-anchor: middle; }
        .subtitle { font-family: Arial, sans-serif; font-size: 11px; fill: #64748b; text-anchor: middle; }
        .axis { stroke: #64748b; stroke-width: 1.5; }
        .tick { font-family: Arial, sans-serif; font-size: 11px; fill: #475569; }
        .axis-label { font-family: Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #1e293b; }
        .grid { stroke: #f1f5f9; stroke-width: 1; }
        .pareto-line { stroke: #2563eb; stroke-width: 2; stroke-dasharray: 6,4; }
        .point-visobert { fill: #2563eb; stroke: #1d4ed8; stroke-width: 3; }
        .point-baseline { fill: #64748b; stroke: #475569; stroke-width: 2; }
        .point-llm { fill: #d97706; stroke: #b45309; stroke-width: 2; }
        .node-label { font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #0f172a; }
        .node-sub { font-family: Arial, sans-serif; font-size: 10px; fill: #64748b; }
        .zone-edge { fill: #eff6ff; opacity: 0.6; }
        .zone-cloud { fill: #fffbeb; opacity: 0.6; }
        .break-mark { stroke: #94a3b8; stroke-width: 2; }
    </style>

    <!-- Background -->
    <rect width="850" height="500" fill="#ffffff" rx="8"/>

    <!-- Deployment Zones -->
    <!-- Edge Zone: x=90 to 520 -->
    <rect x="90" y="70" width="430" height="340" class="zone-edge" rx="6"/>
    <text x="305" y="88" font-family="Arial, sans-serif" font-size="11px" font-weight="bold" fill="#1e40af" text-anchor="middle">TIER 1: REAL-TIME EDGE ZONE (&lt; 60ms, $0 Cost, On-Device)</text>

    <!-- Cloud Zone: x=560 to 800 -->
    <rect x="560" y="70" width="250" height="340" class="zone-cloud" rx="6"/>
    <text x="685" y="88" font-family="Arial, sans-serif" font-size="11px" font-weight="bold" fill="#92400e" text-anchor="middle">TIER 2: ASYNC CLOUD ZONE (&gt; 1s, API Quota)</text>

    <!-- Titles -->
    <text x="425" y="32" class="title">Figure 2: Multi-Objective Trade-Off — Scam Recall vs Latency &amp; Deployment Scope</text>
    <text x="425" y="50" class="subtitle">ViSoBERT defines the Pareto Frontier for Edge Scam Prevention; Gemini 3.5 Flash handles Deep Verification</text>

    <!-- Grid lines (Y: Recall 88% to 101%) -->
    <!-- Y bounds: 88% = y410, 92% = y295, 96% = y175, 100% = y115 -->
    <line x1="90" y1="115" x2="810" y2="115" class="grid"/>
    <line x1="90" y1="175" x2="810" y2="175" class="grid"/>
    <line x1="90" y1="295" x2="810" y2="295" class="grid"/>
    <line x1="90" y1="410" x2="810" y2="410" class="axis"/>

    <!-- Y-axis Ticks -->
    <text x="82" y="119" class="tick" text-anchor="end">100%</text>
    <text x="82" y="179" class="tick" text-anchor="end">96%</text>
    <text x="82" y="299" class="tick" text-anchor="end">92%</text>
    <text x="82" y="414" class="tick" text-anchor="end">88%</text>
    <line x1="90" y1="70" x2="90" y2="410" class="axis"/>

    <!-- Axis Labels -->
    <text x="35" y="250" class="axis-label" transform="rotate(-90 35,250)" text-anchor="middle">Scam Recall Rate (%)</text>
    <text x="440" y="460" class="axis-label" text-anchor="middle">Inference Latency per Message (ms) &amp; Execution Paradigm</text>

    <!-- X-axis Ticks (Edge zone: 10ms - 60ms) -->
    <!-- 10ms = x140, 20ms = x230, 30ms = x320, 40ms = x410, 60ms = x500 -->
    <line x1="140" y1="410" x2="140" y2="415" class="axis"/>
    <text x="140" y="430" class="tick" text-anchor="middle">10ms</text>
    <line x1="230" y1="410" x2="230" y2="415" class="axis"/>
    <text x="230" y="430" class="tick" text-anchor="middle">20ms</text>
    <line x1="320" y1="410" x2="320" y2="415" class="axis"/>
    <text x="320" y="430" class="tick" text-anchor="middle">30ms</text>
    <line x1="500" y1="410" x2="500" y2="415" class="axis"/>
    <text x="500" y="430" class="tick" text-anchor="middle">60ms</text>

    <!-- Axis Break Indicator between Edge & Cloud (x=530 to 550) -->
    <line x1="535" y1="400" x2="525" y2="420" class="break-mark"/>
    <line x1="545" y1="400" x2="535" y2="420" class="break-mark"/>

    <!-- X-axis Cloud Tick -->
    <line x1="685" y1="410" x2="685" y2="415" class="axis"/>
    <text x="685" y="430" class="tick" text-anchor="middle">~4,900ms (Cloud)</text>

    <!-- Pareto Frontier Line -->
    <!-- Connects ViSoBERT (x=217, y=181) to Gemini 3.5 (x=685, y=115) -->
    <path d="M 217 181 Q 380 140 685 115" class="pareto-line"/>
    <text x="400" y="145" font-family="Arial, sans-serif" font-size="10px" font-weight="bold" fill="#2563eb" transform="rotate(-7 400,145)">Pareto Efficiency Frontier</text>

    <!-- Data Points -->
    <!-- 1. ViSoBERT: x=217 (18.6ms), y=181 (95.62%), r=10 -->
    <circle cx="217" cy="181" r="14" fill="#3b82f6" opacity="0.3"/>
    <circle cx="217" cy="181" r="9" class="point-visobert"/>
    <text x="217" y="158" class="node-label" fill="#1d4ed8" text-anchor="middle">ViSoBERT + WBCE* (Hiếu)</text>
    <text x="217" y="172" class="node-sub" font-weight="bold" fill="#2563eb" text-anchor="middle">95.6% Recall | 18.6ms (390MB)</text>

    <!-- 2. PhoBERT-base-v2: x=262 (23.5ms), y=318 (91.23%), r=8 -->
    <circle cx="262" cy="318" r="8" class="point-baseline"/>
    <text x="275" y="315" class="node-label">PhoBERT-base-v2 (Trân)</text>
    <text x="275" y="328" class="node-sub">91.2% Recall | 23.5ms (540MB)</text>

    <!-- 3. FPT ViBERT: x=242 (21.3ms), y=277 (92.60%), r=8 -->
    <circle cx="242" cy="277" r="8" class="point-baseline"/>
    <text x="175" y="275" class="node-label" text-anchor="end">FPT ViBERT (Phúc)</text>
    <text x="175" y="288" class="node-sub" text-anchor="end">92.6% Recall | 21.3ms (480MB)</text>

    <!-- 4. PhoBERT-large: x=486 (58.4ms), y=285 (92.33%), r=14 -->
    <circle cx="486" cy="285" r="14" class="point-baseline"/>
    <text x="505" y="282" class="node-label">PhoBERT-large (Huy)</text>
    <text x="505" y="295" class="node-sub">92.3% Recall | 58.4ms (1.48GB - 370M)</text>

    <!-- 5. Gemini 3.5 Flash: x=685, y=115 (100.0%), r=11 -->
    <circle cx="685" cy="115" r="11" class="point-llm"/>
    <text x="685" y="142" class="node-label" fill="#b45309" text-anchor="middle">Gemini 3.5 Flash (Quang)</text>
    <text x="685" y="155" class="node-sub" fill="#d97706" text-anchor="middle">100% Recall | ~4.9s | Prec 64.5% (Alarm Fatigue)</text>

    <!-- Architectural Tier Summary Box -->
    <rect x="105" y="335" width="220" height="60" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2" rx="4"/>
    <text x="115" y="352" font-family="Arial, sans-serif" font-size="10.5px" font-weight="bold" fill="#1e3a8a">ScamShield 2-Tier Architecture:</text>
    <text x="115" y="368" font-family="Arial, sans-serif" font-size="9.5px" fill="#334155">• Tier 1 (ViSoBERT): 80% msgs, 15ms latency</text>
    <text x="115" y="383" font-family="Arial, sans-serif" font-size="9.5px" fill="#334155">• Tier 2 (Gemini Flash): 20% ambiguous, XAI</text>
    </svg>'''
    return svg

def main():
    fig_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    path1 = os.path.join(fig_dir, "fig1_model_performance_comparison.svg")
    with open(path1, "w", encoding="utf-8") as f:
        f.write(create_bar_chart())
    print(f"✅ Đã tạo figure vector chất lượng cao (>= 300 DPI): {path1}")

    path2 = os.path.join(fig_dir, "fig2_tradeoff_latency_vs_recall.svg")
    with open(path2, "w", encoding="utf-8") as f:
        f.write(create_tradeoff_chart())
    print(f"✅ Đã tạo figure Pareto vector chất lượng cao (>= 300 DPI): {path2}")

if __name__ == "__main__":
    main()

