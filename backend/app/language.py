import re
from typing import Optional

# In-process store per session_id — swap for Redis in multi-worker deploys
_session_lang: dict[str, str] = {}

# Patterns that explicitly request Filipino responses
_TO_FILIPINO = [
    r"\b(sagutin|sumagot|mag-?reply|i-?reply).*(tagalog|filipino|pilipino)\b",
    r"\b(gamitin|gumamit).*(tagalog|filipino|pilipino)\b",
    r"\btagalog\s+(lang|na|po|muna)\b",
    r"\bfil(ipino)?\s+(lang|na|po|muna)\b",
    r"\bsagot.*(?:tagalog|filipino)\b",
    r"\bswitch\s+to\s+(tagalog|filipino)\b",
    r"\breply\s+in\s+(tagalog|filipino)\b",
    r"\banswer\s+in\s+(tagalog|filipino)\b",
    r"\bspeak\s+(tagalog|filipino)\b",
]

# Patterns that explicitly request English responses (from Filipino speakers)
_TO_ENGLISH = [
    r"\b(sagutin|sumagot|mag-?reply|i-?reply).*(ingles|english)\b",
    r"\bswitch\s+to\s+english\b",
    r"\breply\s+in\s+english\b",
    r"\banswer\s+in\s+english\b",
    r"\bspeak\s+english\b",
    r"\benglis[hs]\s+(na|lang|po|muna)\b",
]

def detect_language_switch(text: str) -> Optional[str]:
    lower = text.lower()
    for pat in _TO_FILIPINO:
        if re.search(pat, lower):
            return "filipino"
    for pat in _TO_ENGLISH:
        if re.search(pat, lower):
            return "english"
    return None

def get_response_language(session_id: str, user_message: str) -> str:
    """
    Returns the language the bot should respond in.
    Default is always English. Only changes on explicit user request.
    The preference is remembered for the rest of the session.
    """
    switch = detect_language_switch(user_message)
    if switch:
        _session_lang[session_id] = switch
    # Default to English if no preference has ever been set
    return _session_lang.get(session_id, "english")

def build_language_instruction(lang: str) -> str:
    if lang == "filipino":
        return (
            "Sumagot sa Filipino/Tagalog. "
            "Maaari kang gumamit ng mga teknikal na termino sa Ingles kung kinakailangan, "
            "ngunit ang pangunahing wika ng iyong sagot ay Filipino. "
            "Maging malinaw at propesyonal."
        )
    return (
        "Always respond in English. "
        "You understand both English and Filipino input fluently — "
        "the user may write in either language or mix them (Taglish), "
        "and you will understand perfectly. "
        "However, you must always reply in English "
        "unless the user explicitly asks you to switch to Filipino."
    )