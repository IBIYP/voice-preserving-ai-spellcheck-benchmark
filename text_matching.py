import re


def contains_phrase(text, phrase):
    """Match a case-insensitive phrase without matching inside another word."""
    pattern = r"(?<!\w)" + re.escape(phrase.casefold()) + r"(?!\w)"
    return re.search(pattern, text.casefold()) is not None
