from typing import List, Dict

from .intent_dfa import Intent


def build_prompt(intent: Intent, history: List[Dict[str, str]], user_text: str) -> str:
    """CFG-like structured prompt builder."""

    system_block = (
        "You are a helpful, safe assistant running entirely on a local machine. "
        "You must respect privacy, avoid disallowed content, and clearly say when you don't know something."
    )

    if intent == Intent.MATH:
        task_block = "Solve the following math expression step by step. Show short reasoning and final answer."
    elif intent == Intent.UNSAFE:
        task_block = (
            "The user request may contain unsafe or sensitive content. "
            "Respond by refusing politely and suggesting they seek appropriate, safe support."
        )
    else:
        task_block = "Answer the user's question clearly, concisely, and accurately."

    turns = []
    for msg in history[-6:]:
        role = msg["role"].title()
        turns.append(f"{role}: {msg['content']}")
    history_block = "\n".join(turns)

    prompt_parts = [
        system_block,
        "",
        task_block,
        "",
    ]
    if history_block:
        prompt_parts.append(history_block)
        prompt_parts.append("")

    prompt_parts.append(f"User: {user_text}")
    prompt_parts.append("Assistant:")

    return "\n".join(prompt_parts)
