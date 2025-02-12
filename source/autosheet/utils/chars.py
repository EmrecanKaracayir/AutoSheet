def get_safe_name(char: str) -> str:
    """
    Get a safe name and code for a given character.
    """
    code = ord(char)
    safe_char = char if char.isalnum() else f"u{code:04x}"
    return f"{safe_char}_{code}"
