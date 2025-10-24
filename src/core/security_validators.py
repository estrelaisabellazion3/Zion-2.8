#!/usr/bin/env python3
"""
ZION Security Validators
Input validation and sanitization utilities
"""

import re
import html
from typing import Tuple, Optional

def validate_address(address: str) -> Tuple[bool, Optional[str]]:
    """
    Validate blockchain address format

    Args:
        address: Address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not address or not isinstance(address, str):
        return False, "Address is required"

    # ZION address format: starts with Z3 followed by 60 hex characters
    if address.startswith('Z3') and len(address) == 62:
        if re.match(r'^Z3[a-fA-F0-9]{60}$', address):
            return True, None
        else:
            return False, "Invalid ZION address format"

    # Basic validation for other formats
    if len(address) < 10:
        return False, "Address too short"

    if len(address) > 100:
        return False, "Address too long"

    return True, None

def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:
        return False, "Password too long"

    return True, None

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent injection attacks

    Args:
        input_str: Input string to sanitize

    Returns:
        Sanitized string
    """
    if not input_str:
        return ""

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>]', '', input_str)

    # Limit length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]

    return sanitized.strip()

def sanitize_html(input_str: str) -> str:
    """
    Sanitize HTML content

    Args:
        input_str: HTML string to sanitize

    Returns:
        Sanitized HTML
    """
    if not input_str:
        return ""

    # Basic HTML escaping
    return html.escape(input_str)