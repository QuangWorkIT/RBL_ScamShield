# -*- coding: utf-8 -*-
"""
==============================================================================
ScamShield-VN: Client-Side PII Sanitization Module
==============================================================================
Location: pipeline/pii_sanitizer.py
Description:
    Implements deterministic rule-based redaction of Personally Identifiable
    Information (PII) before telemetry logging or external Cloud LLM transmission.
    Adheres to safety-first principles aligned with Decree 13/2023/ND-CP Article 25.
    
    Protected Entities:
      1. Phone numbers (VN standard 10-digit prefixes, +84, dots/dashes)
      2. Bank account and card numbers (8-19 consecutive digits)
      3. Citizen Identification Numbers (CCCD 12 digits, CMND 9 digits)
      4. One-Time Password (OTP) verification tokens (4-8 digits)
      5. Monetary balance statements (VND / USD / đ)
==============================================================================
"""

import re
from typing import Dict, Tuple, List, Optional

class MessagePIISanitizer:
    """
    Sanitizes personal identifiable information from Vietnamese SMS text
    prior to sending payloads to external cloud LLM APIs.
    """

    # 1. Citizen Identity: 12-digit CCCD or 9-digit CMND preceded by context keywords
    CCCD_PATTERN = re.compile(
        r"(?i)\b(?:cccd|cmnd|cmt|căn\s*cước|can\s*cuoc|chứng\s*minh(?:\s*thư)?|chung\s*minh(?:\s*thu)?|định\s*danh|dinh\s*danh)\s*[:#\-]?\s*(\d{9}|\d{12})\b"
    )

    # Standalone 12-digit numeric sequences starting with 0 likely to be CCCD
    STANDALONE_CCCD_PATTERN = re.compile(
        r"\b(0\d{11})\b"
    )

    # 2. Bank Account / Debit / Credit Card: preceded by context keywords
    ACCOUNT_KEYWORD_PATTERN = re.compile(
        r"(?i)\b(?:stk|số\s*tài\s*khoản|so\s*tai\s*khoan|tài\s*khoản|tai\s*khoan|tk\s*ngân\s*hàng|tk\s*ngan\s*hang|so\s*tk|card|số\s*thẻ|so\s*the)\s*[:#\-]?\s*(\d{8,19})\b"
    )

    # 3. OTP verification code: 4-8 digits preceded by OTP keywords (accented and unaccented)
    OTP_PATTERN = re.compile(
        r"(?i)\b(?:mã\s*otp|ma\s*otp|otp|mã\s*xác\s*thực|ma\s*xac\s*thuc|mã\s*xác\s*nhận|ma\s*xac\s*nhan|xác\s*thực\s*otp|xac\s*thuc\s*otp|code|mã\s*bảo\s*mật|ma\s*bao\s*mat)\s*(?:của\s*bạn|cua\s*ban)?\s*(?:là|la|:|#|-|\s)\s*([A-Za-z0-9]{4,8})\b"
    )

    # 4. Vietnamese Phone Numbers: (03x, 05x, 07x, 08x, 09x, or +84/84) with 9-10 digits, allowing space/dot/dash
    PHONE_PATTERN = re.compile(
        r"(?:\+?84|0)(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])[\s\.\-]?[0-9]{3}[\s\.\-]?[0-9]{4}\b"
    )

    # 5. Account Balances: e.g., "Số dư: 12.500.000 VND" or "GD: -500,000 d"
    BALANCE_PATTERN = re.compile(
        r"(?i)\b(?:số\s*dư|so\s*du|biến\s*động\s*số\s*dư|bien\s*dong\s*so\s*du|giao\s*dịch|giao\s*dich|sodu)\s*[:#\-]?\s*([+\-]?\s*[\d\.\,]{3,15}\s*(?:vnd|vnđ|đ|dong|đồng|usd))\b"
    )

    def __init__(self, redact_otp: bool = True, redact_phone: bool = True, redact_account: bool = True):
        self.redact_otp = redact_otp
        self.redact_phone = redact_phone
        self.redact_account = redact_account

    def sanitize(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """
        Redacts sensitive tokens in text.
        
        Returns:
            Tuple of (sanitized_text, redaction_manifest)
        """
        if not text:
            return "", {}

        sanitized = text
        manifest: Dict[str, List[str]] = {
            "cccd": [],
            "account": [],
            "otp": [],
            "phone": [],
            "balance": []
        }

        # Step 1: Sanitize Account Balances
        def _rep_balance(m):
            matched = m.group(0)
            val = m.group(1)
            manifest["balance"].append(val)
            return matched.replace(val, "[BALANCE_REDACTED]")
        sanitized = self.BALANCE_PATTERN.sub(_rep_balance, sanitized)

        # Step 2: Sanitize CCCD / CMND
        def _rep_cccd(m):
            full_match = m.group(0)
            id_val = m.group(1)
            manifest["cccd"].append(id_val)
            return full_match.replace(id_val, "[CITIZEN_ID_REDACTED]")
        sanitized = self.CCCD_PATTERN.sub(_rep_cccd, sanitized)

        def _rep_standalone_cccd(m):
            id_val = m.group(1)
            manifest["cccd"].append(id_val)
            return "[CITIZEN_ID_REDACTED]"
        sanitized = self.STANDALONE_CCCD_PATTERN.sub(_rep_standalone_cccd, sanitized)

        # Step 3: Sanitize Bank Accounts
        if self.redact_account:
            def _rep_account(m):
                full_match = m.group(0)
                acc_val = m.group(1)
                manifest["account"].append(acc_val)
                return full_match.replace(acc_val, "[ACCOUNT_REDACTED]")
            sanitized = self.ACCOUNT_KEYWORD_PATTERN.sub(_rep_account, sanitized)

        # Step 4: Sanitize OTP codes
        if self.redact_otp:
            def _rep_otp(m):
                full_match = m.group(0)
                otp_val = m.group(1)
                manifest["otp"].append(otp_val)
                return full_match.replace(otp_val, "[OTP_REDACTED]")
            sanitized = self.OTP_PATTERN.sub(_rep_otp, sanitized)

        # Step 5: Sanitize Phone Numbers
        if self.redact_phone:
            def _rep_phone(m):
                phone_val = m.group(0)
                manifest["phone"].append(phone_val)
                return "[PHONE_REDACTED]"
            sanitized = self.PHONE_PATTERN.sub(_rep_phone, sanitized)

        return sanitized, manifest
