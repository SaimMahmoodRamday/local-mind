from .intent_dfa import Intent


def canned_response_for_intent(intent: Intent) -> str:
    if intent == Intent.GREETING:
        return "Hello! 👋 How can I help you today?"
    if intent == Intent.GOODBYE:
        return "Goodbye! 👋 If you have more questions later, just open this chat again."
    if intent == Intent.THANKS:
        return "You're welcome! 😊 Let me know if there's anything else you need."
    return "How can I assist you?"
