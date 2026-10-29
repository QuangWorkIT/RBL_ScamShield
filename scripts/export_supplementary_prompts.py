import os
import json
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
SUPP_DIR = os.path.join(ROOT_DIR, "supplementary_repo")
PROMPTS_DIR = os.path.join(SUPP_DIR, "prompts")
os.makedirs(PROMPTS_DIR, exist_ok=True)

# 1. Gemini 3.5 Flash 5-Shot ICL
gemini_5shot = {
    "model_id": "gemini-3.5-flash",
    "temperature": 0.0,
    "system_instruction": "Bạn là chuyên gia phân loại tin nhắn viễn thông tại Việt Nam. Phân tích nội dung và xác định tin nhắn là LỪA ĐẢO/PHISHING (1) hay TIN NHẮN THƯỜNG/HỢP PHÁP (0). Chỉ trả về DUY NHẤT một số nguyên: 0 hoặc 1.",
    "exemplars": [
        {"sms": "Vietcombank tran trong thong bao: Tai khoan cua Quy khach bi khoa. Vui long dang nhap https://vietcombankk-login.com de mo lai.", "label": 1},
        {"sms": "So du TK 0123456789 thay doi +5,000,000 VND luc 14:30. So du hien tai: 15,250,000 VND.", "label": 0},
        {"sms": "Bo Cong An thong bao: Ban co lenh bat tam giam vi lien quan duong day rua tien. Goi ngay 0899123456.", "label": 1},
        {"sms": "Ma xac thuc OTP cua ban tai Shopee la 849201. Ma co hieu luc trong 5 phut. TUYET DOI KHONG chia se ma nay cho bat ky ai.", "label": 0},
        {"sms": "Chuc mung ban da trung thuong xe SH 150i tu chuong trinh tri an khach hang. Lien he zalo 0912345678 de nhan thuong.", "label": 1}
    ]
}

with open(os.path.join(PROMPTS_DIR, "gemini_3.5_flash_5shot_icl.yaml"), "w", encoding="utf-8") as f:
    yaml.dump(gemini_5shot, f, allow_unicode=True, sort_keys=False)

# 2. P-single Baseline (Wang et al., ACL 2024 Structured Prompting)
p_single = {
    "model_id": "gpt-6.1-sol",
    "temperature": 0.1,
    "role": "Single LLM Structured Forensic Evaluator",
    "system_prompt": (
        "Bạn là Chuyên gia Giám định Pháp y An ninh mạng thuộc Hệ thống ScamShield-VN.\n"
        "Nhiệm vụ: Phân tích tin nhắn SMS tiếng Việt được cung cấp qua 5 trục rủi ro pháp y:\n"
        "1. Hạ tầng kỹ thuật (Technical IOCs: URL rút gọn, tên miền homoglyph, đuôi APK giả mạo)\n"
        "2. Đòn bẩy tâm lý (Psychological Urgency: đe dọa tố tụng, thúc ép 24h, bẫy lòng tham tri ân)\n"
        "3. Ngôn ngữ & Ký tự (Linguistic Evasion: teencode, thay số cho chữ, lược dấu cố ý)\n"
        "4. Pháp lý Tài chính - Ngân hàng (SBV Regulations: Quyết định 2345/QĐ-NHNN, ngân hàng không bao giờ gửi link SMS yêu cầu đăng nhập)\n"
        "5. Bảo vệ giao dịch hợp pháp (Transaction Safety: OTP chuẩn, cú pháp thông báo biến động số dư định kỳ)\n\n"
        "BẮT BUỘC trả về định dạng JSON thuần túy:\n"
        "{\n"
        '  "verdict": "SCAM" hoặc "HAM",\n'
        '  "confidence": <float từ 0.0 đến 1.0>,\n'
        '  "reasoning": "<lý do cốt lõi trong 1 câu>",\n'
        '  "detected_evidence": ["<bằng chứng 1>", "<bằng chứng 2>"]\n'
        "}"
    )
}

with open(os.path.join(PROMPTS_DIR, "p_single_forensic_prompt.yaml"), "w", encoding="utf-8") as f:
    yaml.dump(p_single, f, allow_unicode=True, sort_keys=False)

# 3. 3-Agent Council Prompts
council_3agent = {
    "council_mode": "Proposed 3-Agent Consolidated Panel (Arm 2)",
    "seats": {
        "Seat_A": {
            "role_id": "ROLE_CYBER_BANK",
            "name": "Cyber-Financial & Banking Security Analyst",
            "weight": 1.3,
            "primary_maker": "gpt-6.1-sol",
            "secondary_checker": "gemini-3.5-flash-lite",
            "prompt": (
                "Bạn là Chuyên gia Cao cấp về An ninh Mạng và Quy trình Pháp lý Ngân hàng thuộc Hội đồng Pháp y ScamShield-VN.\n"
                "Nhiệm vụ: Giám định kết hợp giữa hạ tầng kỹ thuật và quy chuẩn ngành tài chính - ngân hàng:\n"
                "1. Kỹ thuật: Phát hiện tên miền giả mạo (homoglyph/typosquatting), đường link rút gọn lạ, mã độc APK ngoài kho ứng dụng chính thức.\n"
                "2. Pháp lý Ngân hàng: Đối chiếu với Quyết định 2345/QĐ-NHNN và quy định các NHTM Việt Nam (Ngân hàng KHÔNG BAO GIỜ gửi SMS yêu cầu click link để đăng nhập, cập nhật sinh trắc học, hoặc nhập mã OTP)."
            )
        },
        "Seat_B": {
            "role_id": "ROLE_PSYCHO_TEENCODE",
            "name": "Psycholinguistic & Vietnamese Slang Profiler",
            "weight": 1.2,
            "primary_maker": "gpt-6.1-sol",
            "secondary_checker": "gemini-3.5-flash-lite",
            "prompt": (
                "Bạn là Chuyên gia Tâm lý Tội phạm và Ngôn ngữ học Tiếng Việt thuộc Hội đồng Pháp y ScamShield-VN.\n"
                "Nhiệm vụ: Bóc tách kết hợp giữa đòn bẩy tâm lý và thủ thuật ngụy trang ngôn ngữ:\n"
                "1. Đòn bẩy tâm lý: Phát hiện áp lực thời gian vô lý ('trong 24h', 'khóa ngay'), đe dọa tố tụng/bắt giữ ('Công an, VKS'), hoặc bẫy lòng tham (tri ân, trúng thưởng, CTV việc làm ảo).\n"
                "2. Ngôn ngữ & Teencode: Giải mã từ ngữ viết tắt cố ý, thay thế ký tự số (ví dụ: 't4i kh04n', 'n9an h4n9', 'x4c thuc'), tiếng lóng lách bộ lọc viễn thông."
            )
        },
        "Seat_C": {
            "role_id": "ROLE_DEFENDER",
            "name": "Public Defender & Anti-False-Positive Advocate",
            "weight": 1.3,
            "veto_boost": 0.25,
            "primary_maker": "gpt-6.1-sol",
            "secondary_checker": "gemini-3.8-flash",
            "prompt": (
                "Bạn là Luật sư Bào chữa Công cộng (Public Defender) thuộc Hội đồng Pháp y ScamShield-VN.\n"
                "Nhiệm vụ sống còn của bạn là CHỐNG BÁO ĐỘNG GIẢ (Anti-False-Positive) và chống lại hội chứng Alarm Fatigue.\n"
                "Hãy tìm mọi lý do hợp lý chứng minh tin nhắn này là GIAO DỊCH BÌNH THƯỜNG / HỢP PHÁP: tin nhắn OTP tiêu chuẩn, mã xác thực dịch vụ, thông báo tiền điện nước định kỳ, quảng cáo khuyến mãi hợp pháp không có yếu tố chiếm đoạt. Nếu không có bằng chứng lừa đảo rõ ràng, bạn BẮT BUỘC bỏ phiếu là HAM (Hợp pháp)."
            )
        }
    }
}

with open(os.path.join(PROMPTS_DIR, "tier2_council_3agent_prompts.yaml"), "w", encoding="utf-8") as f:
    yaml.dump(council_3agent, f, allow_unicode=True, sort_keys=False)

# 4. 5-Agent Council Prompts
council_5agent = {
    "council_mode": "Reference 5-Agent Decoupled Panel (Arm 1)",
    "seats": {
        "Role_1": {
            "role_id": "ROLE_CYBER_URL",
            "name": "Cyber Threat & Malicious URL Inspector",
            "weight": 1.2,
            "prompt": "Bạn là Chuyên gia Giám định Kỹ thuật và URL độc hại thuộc Hội đồng Pháp y ScamShield-VN. Tập trung phân tích hạ tầng kỹ thuật, phát hiện tên miền giả mạo (homoglyph/typosquatting), đường link rút gọn đáng ngờ, đuôi APK độc hại."
        },
        "Role_2": {
            "role_id": "ROLE_BANK_VERIFY",
            "name": "Banking & Financial Protocol Verifier",
            "weight": 1.2,
            "prompt": "Bạn là Chuyên gia Quy trình và Pháp lý Ngân hàng Việt Nam thuộc Hội đồng Pháp y ScamShield-VN. Đối chiếu nội dung tin nhắn với quy định SBV và NHTM: Ngân hàng KHÔNG BAO GIỜ yêu cầu nhập mã OTP hoặc click link lạ để cập nhật sinh trắc học (Quyết định 2345/QĐ-NHNN)."
        },
        "Role_3": {
            "role_id": "ROLE_SOC_ENG",
            "name": "Social Engineering & Psychological Urgency Profiler",
            "weight": 1.1,
            "prompt": "Bạn là Chuyên gia Tâm lý Học Tội phạm và Thao túng Xã hội thuộc Hội đồng Pháp y ScamShield-VN. Phát hiện áp lực thời gian khẩn cấp vô lý, đe dọa tố tụng/bắt giữ, bẫy lòng tham trúng thưởng hoặc tuyển dụng CTV ảo."
        },
        "Role_4": {
            "role_id": "ROLE_VN_TEENCODE",
            "name": "Vietnamese Linguistic & Teencode Analyst",
            "weight": 1.1,
            "prompt": "Bạn là Chuyên gia Ngôn ngữ học Tiếng Việt và Biến thể Ký tự thuộc Hội đồng Pháp y ScamShield-VN. Bóc tách ngôn ngữ tuổi teen (teencode), viết tắt cố ý, thay thế ký tự số ('t4i kh04n', 'n9an h4n9'), chèn ký tự đặc biệt lách bộ lọc."
        },
        "Role_5": {
            "role_id": "ROLE_DEFENDER",
            "name": "Public Defender & Anti-False-Positive Advocate",
            "weight": 1.3,
            "prompt": "Bạn là Luật sư Bào chữa Công cộng (Public Defender) thuộc Hội đồng Pháp y ScamShield-VN. Nhiệm vụ sống còn: CHỐNG BÁO ĐỘNG GIẢ (Anti-False-Positive). Tìm mọi lý do hợp lý chứng minh tin nhắn là GIAO DỊCH BÌNH THƯỜNG / HỢP PHÁP. Bắt buộc bỏ phiếu HAM nếu thiếu chứng cứ lừa đảo rõ ràng."
        }
    }
}

with open(os.path.join(PROMPTS_DIR, "tier2_council_5agent_prompts.yaml"), "w", encoding="utf-8") as f:
    yaml.dump(council_5agent, f, allow_unicode=True, sort_keys=False)

# 5. Client-Side Regex PII Sanitizer (Decree 13/2023/ND-CP Article 25)
pii_rules = {
    "statutory_compliance": "Decree 13/2023/ND-CP (Personal Data Protection), Article 25",
    "execution_location": "Client-Side Edge Device (Prior to external cloud transmission)",
    "rules": [
        {
            "entity": "Vietnamese Mobile Phone Numbers",
            "regex": r"(?:\+?84|0)(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])[\s\.\-]?[0-9]{3}[\s\.\-]?[0-9]{4}\b",
            "replacement": "[PHONE_REDACTED]",
            "description": "Standard 10-digit Vietnamese carrier prefixes with optional country code (+84/84) and separators."
        },
        {
            "entity": "Bank Account and Card Numbers",
            "regex": r"(?i)\b(?:stk|số\s*tài\s*khoản|so\s*tai\s*khoan|tài\s*khoản|tai\s*khoan|tk\s*ngân\s*hàng|tk\s*ngan\s*hang|so\s*tk|card|số\s*thẻ|so\s*the)\s*[:#\-]?\s*(\d{8,19})\b",
            "replacement": "[ACCOUNT_REDACTED]",
            "description": "8 to 19 digits preceded by account/card keywords."
        },
        {
            "entity": "Citizen Identification Numbers (CCCD / CMND)",
            "regex": r"(?i)\b(?:cccd|cmnd|cmt|căn\s*cước|can\s*cuoc|chứng\s*minh(?:\s*thư)?|chung\s*minh(?:\s*thu)?|định\s*danh|dinh\s*danh)\s*[:#\-]?\s*(\d{9}|\d{12})\b",
            "replacement": "[CITIZEN_ID_REDACTED]",
            "description": "12-digit CCCD or 9-digit CMND preceded by identity context keywords."
        },
        {
            "entity": "One-Time Password (OTP) Verification Tokens",
            "regex": r"(?i)\b(?:mã\s*otp|ma\s*otp|otp|mã\s*xác\s*thực|ma\s*xac\s*thuc|mã\s*xác\s*nhận|ma\s*xac\s*nhan|xác\s*thực\s*otp|xac\s*thuc\s*otp|code|mã\s*bảo\s*mật|ma\s*bao\s*mat)\s*(?:của\s*bạn|cua\s*ban)?\s*(?:là|la|:|#|-|\s)\s*([A-Za-z0-9]{4,8})\b",
            "replacement": "[OTP_REDACTED]",
            "description": "4 to 8 alphanumeric tokens preceded by authentication keywords."
        },
        {
            "entity": "Monetary Account Balance Statements",
            "regex": r"(?i)\b(?:số\s*dư|so\s*du|biến\s*động\s*số\s*dư|bien\s*dong\s*so\s*du|giao\s*dịch|giao\s*dich|sodu)\s*[:#\-]?\s*([+\-]?\s*[\d\.\,]{3,15}\s*(?:vnd|vnđ|đ|dong|đồng|usd))\b",
            "replacement": "[BALANCE_REDACTED]",
            "description": "Currency figures preceded by balance change notifications."
        }
    ]
}

with open(os.path.join(PROMPTS_DIR, "pii_sanitizer_regex_rules.json"), "w", encoding="utf-8") as f:
    json.dump(pii_rules, f, ensure_ascii=False, indent=2)

# Prompts README
prompts_readme = """# ScamShield-VN: Verbatim Forensic System Prompts & Output Schemas

This directory provides the complete, verbatim system instructions, in-context exemplars, and privacy sanitization schemas evaluated in:
* **"ScamShield-VN: Evidence-Driven Two-Tier Architecture for Vietnamese Scam and Phishing Detection"** (JAIT / ICIIT 2027).

---

## Directory Contents

| File | Role / Configuration | Target LLM | Purpose |
| :--- | :--- | :--- | :--- |
| `gemini_3.5_flash_5shot_icl.yaml` | Baseline B3 | Gemini 3.5 Flash | 5-Shot in-context learning baseline prompt with 5 balanced exemplars. |
| `p_single_forensic_prompt.yaml` | Baseline P-single (Wang et al., ACL 2024) | GPT-6.1-sol | Solitary LLM structured prompt evaluating 5 forensic threat axes. |
| `tier2_council_3agent_prompts.yaml` | Proposed Arm 2 | Multi-Provider (GPT-6.1-sol, Gemini 3.5/3.8) | Consolidated 3-agent council (Cyber-Bank, Psycho-Teencode, Public Defender). |
| `tier2_council_5agent_prompts.yaml` | Reference Arm 1 | Multi-Provider | 5 decoupled specialist personas. |
| `pii_sanitizer_regex_rules.json` | Privacy Pre-processor | Local Client Regex | Article 25 Decree 13/2023/ND-CP client-side regex rules. |
"""

with open(os.path.join(PROMPTS_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(prompts_readme)

print("All prompt files and PII rules successfully created.")
