from enum import Enum
import re


# class Intent(str, Enum):
#     GREETING = "greeting"
#     GOODBYE = "goodbye"
#     THANKS = "thanks"
#     MATH = "math"
#     GENERAL = "general"
#     UNSAFE = "unsafe"


# GREETING_RE = re.compile(r"\b(hi|hello|hey|salam|assalam|good morning|good evening)\b", re.I)
# GOODBYE_RE = re.compile(r"\b(bye|goodbye|see you|take care)\b", re.I)
# THANKS_RE = re.compile(r"\b(thanks|thank you|shukria|shukriya)\b", re.I)
# MATH_RE = re.compile(r"^[0-9\.\+\-\*/\^\(\)\s=]+$", re.I)

# UNSAFE_KEYWORDS = [
#     "password",
#     "credit card",
#     "kill",
#     "suicide",
#     "self-harm",
#     "hack"
# ]


class Intent(str, Enum):
    GREETING = "greeting"
    GOODBYE = "goodbye"
    THANKS = "thanks"
    MATH = "math"
    GENERAL = "general"
    UNSAFE = "unsafe"


GREETING_RE = re.compile(
    r"\b(hi|hello|hey|salam|assalam|good morning|good evening|"
    r"greetings|howdy|what's up|hi there|hello there|hey there|"
    r"good afternoon|good day|yo|welcome)\b",
    re.I
)

GOODBYE_RE = re.compile(
    r"\b(bye|goodbye|see you|take care|see you later|farewell|"
    r"catch you later|talk to you later|good night|see ya|later|"
    r"have a good day|i'm leaving|ciao)\b",
    re.I
)

THANKS_RE = re.compile(
    r"\b(thanks|thank you|shukria|shukriya|thanks a lot|thank you so much|"
    r"much appreciated|thanks buddy|thanks man|thanks dear|thanks for the help|"
    r"i appreciate it|grateful)\b",
    re.I
)

MATH_RE = re.compile(
    r"^[0-9\.\+\-\*/\^\(\)\s=]+$",   # math-only patterns (kept same)
    re.I
)

UNSAFE_KEYWORDS = [
    "password", "credit card", "kill", "suicide", "self-harm", "hack",
    "murder", "harm", "danger", "attack", "bomb", "illegal access",
    "exploit", "malware", "virus", "ddos", "steal data",
    "unauthorized login", "shoot", "knife", "violent act",
    "terror", "terrorist", "extremism", "injure", "abuse",
    "phishing", "breach", "fraud", "identity theft",
    "poison", "assault", "destroy", "gun", "weapon",
    "rape", "drugs", "illegal hacking", "unauthorized entry",
    "blackmail", "threat", "violence", "crime", "kidnap",
    "harm yourself", "end your life", "take your life",
    "commit suicide", "bomb making", "grenade", "shooting"
]


def classify_intent(text: str) -> Intent:
    t = text.strip().lower()

    for kw in UNSAFE_KEYWORDS:
        if kw in t:
            return Intent.UNSAFE

    if GREETING_RE.search(t):
        return Intent.GREETING
    if GOODBYE_RE.search(t):
        return Intent.GOODBYE
    if THANKS_RE.search(t):
        return Intent.THANKS

    if MATH_RE.match(t.replace(" ", "")):
        return Intent.MATH

    return Intent.GENERAL
