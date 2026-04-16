from typing import Tuple

BANNED_PATTERNS = [
    "credit card",
    "password",
    "bank account",
    "kill yourself",
    "self-harm",
]


def check_output_safe(text: str) -> Tuple[bool, str | None]:
    """Very simple DFA-like scanner."""
    lower = text.lower()
    for pattern in BANNED_PATTERNS:
        if pattern in lower:
            return False, f"Contains disallowed phrase: '{pattern}'"
    return True, None
