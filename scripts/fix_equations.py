# -*- coding: utf-8 -*-
"""
Fix equation widths across Section III to eliminate two-column margin overflow.
"""

def update_equations():
    # 1. Update 03_method.tex
    with open('paper/sections/03_method.tex', 'r', encoding='utf-8') as f:
        text = f.read()

    # Compact Eq 2 (gradient): remove verbose text comments inside math cases
    old_eq2 = r'''\begin{equation}
\label{eq:wbce_gradient}
\frac{\partial \mathcal{L}_{\text{WBCE}}}{\partial z_i} = \frac{1}{N} \begin{cases} \alpha (\hat{y}_i - 1), & \text{if } y_i = 1 \text{ (False Negative)} \\ \hat{y}_i, & \text{if } y_i = 0 \text{ (False Positive)} \end{cases}
\end{equation}'''

    new_eq2 = r'''\begin{equation}
\label{eq:wbce_gradient}
\frac{\partial \mathcal{L}_{\text{WBCE}}}{\partial z_i} = \frac{1}{N} \begin{cases} 
\alpha (\hat{y}_i - 1), & \text{if } y_i = 1 \\ 
\hat{y}_i, & \text{if } y_i = 0 
\end{cases}
\end{equation}'''

    text = text.replace(old_eq2, new_eq2)

    # Compact Eq 3 (routing): use confidence metric C_T1 to prevent horizontal overflow
    old_eq3 = r'''\begin{equation}
\label{eq:routing}
\text{Route}(x) = \begin{cases} \text{Tier 1 Edge Fast-Path}, & \text{if } \max(P_{\text{T1}}, 1 - P_{\text{T1}}) \ge \tau \\ \text{Tier 2 Council Escalation}, & \text{if } \max(P_{\text{T1}}, 1 - P_{\text{T1}}) < \tau \end{cases}
\end{equation}
where $P_{\text{T1}} = \sigma(z_{\text{T1}})$ denotes the calibrated scam probability output by Tier 1, and $\tau = 0.90$ is the operational routing threshold. Messages with confident predictions ($\ge 0.90$ or $\le 0.10$) terminate at Tier 1 with sub-100 ms latency and zero API cost. Borderline messages within the uncertainty band ($P_{\text{T1}} \in (0.10, 0.90)$) are escalated to Tier 2.'''

    new_eq3 = r'''\begin{equation}
\label{eq:routing}
\text{Route}(x) = \begin{cases} 
\text{Tier 1 (Edge)}, & \text{if } C_{\text{T1}}(x) \ge \tau \\ 
\text{Tier 2 (Council)}, & \text{if } C_{\text{T1}}(x) < \tau 
\end{cases}
\end{equation}
where $C_{\text{T1}}(x) = \max(P_{\text{T1}}, 1 - P_{\text{T1}})$ denotes the edge screener confidence, $P_{\text{T1}} = \sigma(z_{\text{T1}})$ represents the calibrated scam probability output by ViSoBERT, and $\tau = 0.90$ is the operational routing threshold. Messages with confident predictions ($C_{\text{T1}} \ge 0.90$) terminate at Tier 1 with sub-100 ms latency and zero API cost. Borderline messages within the uncertainty band ($C_{\text{T1}} < 0.90$, i.e., $P_{\text{T1}} \in (0.10, 0.90)$) are escalated to Tier 2.'''

    text = text.replace(old_eq3, new_eq3)

    # Compact Eq 5 (verdict): use 'otherwise' for third condition
    old_eq5 = r'''\begin{equation}
\label{eq:labels}
\text{Verdict} = \begin{cases} 
\textbf{SCAM-RISK}, & \text{if } P_{\text{council}} \ge 0.60 \\
\textbf{LOW-RISK}, & \text{if } P_{\text{council}} < 0.40 \\
\textbf{UNKNOWN}, & \text{if } 0.40 \le P_{\text{council}} < 0.60 
\end{cases}
\end{equation}'''

    new_eq5 = r'''\begin{equation}
\label{eq:labels}
\text{Verdict} = \begin{cases} 
\text{SCAM-RISK}, & \text{if } P_{\text{council}} \ge 0.60 \\
\text{LOW-RISK}, & \text{if } P_{\text{council}} < 0.40 \\
\text{UNKNOWN}, & \text{otherwise}
\end{cases}
\end{equation}'''

    text = text.replace(old_eq5, new_eq5)

    with open('paper/sections/03_method.tex', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated paper/sections/03_method.tex with compact equations!')

if __name__ == '__main__':
    update_equations()
