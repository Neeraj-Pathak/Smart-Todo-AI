from datetime import datetime, timedelta
import random
import re
from collections import Counter

def choose_relevant_snippet(title: str, context_list: list[str]) -> str | None:
    """Pick the context line with most word overlap to title (stop‑word‑aware)."""
    if not context_list:
        return None

    # very small stop‑word set
    stop = {"the", "for", "and", "to", "by", "a", "an", "of", "in", "on", "with"}
    title_words = {w for w in re.findall(r"[a-zA-Z]+", title.lower()) if w not in stop}

    best_line = None
    best_score = 0
    for line in context_list:
        words = {w for w in re.findall(r"[a-zA-Z]+", line.lower()) if w not in stop}
        overlap = len(title_words & words)
        if overlap > best_score:
            best_score = overlap
            best_line = line

    # Require at least one shared keyword, OR line contains 'urgent/today/by <date>'
    if best_score > 0 or re.search(r"\b(urgent|today|asap|by\s+\w+)\b", best_line or "", re.I):
        return best_line
    return None


def generate_task_suggestions(title: str,
                              description: str = "",
                              context_list: list[str] | None = None):
    """
    Rule‑based demo AI that looks at title + description + daily context
    and returns priority, deadline, category, and an enhanced description.
    """

    # ── 1. Merge all text for simple keyword checks ──────────────────────────────
    context_text = " ".join(context_list or [])
    text = f"{title} {description} {context_text}".lower()

    # ── 2. Priority & deadline heuristics ───────────────────────────────────────
    if re.search(r"\b(urgent|today|asap)\b", text):
        priority = round(random.uniform(8.5, 10), 2)
        deadline = datetime.now().date()
    elif re.search(r"\b(interview|presentation|report|resume|sales deck)\b", text):
        priority = round(random.uniform(6, 8.5), 2)
        deadline = datetime.now().date() + timedelta(days=2)
    else:
        priority = round(random.uniform(4, 6), 2)
        deadline = datetime.now().date() + timedelta(days=3)

    # ── 3. Category guess ───────────────────────────────────────────────────────
    if "interview" in text or "resume" in text or "career" in text:
        category = "Career"
    elif "project" in text or "report" in text or "presentation" in text:
        category = "Work"
    elif "meditation" in text or "workout" in text or "doctor" in text:
        category = "Health"
    elif "buy" in text or "shopping" in text:
        category = "Personal"
    elif "email" in text or "call" in text:
        category = "Communication"
    else:
        category = "General"

    CATEGORY_KEYWORDS = {
    "Career": ["resume", "interview", "placement", "linkedin", "job"],
    "Work": ["report", "deck", "meeting", "deadline", "project"],
    "Health": ["meditation", "doctor", "exercise", "yoga", "diet"],
    "Communication": ["email", "message", "chat", "call", "client"],
    "Personal": ["shopping", "family", "birthday", "travel", "movie"],
    "General": ["note", "misc", "task"]
}

def auto_category(title: str, description: str) -> str:
    combined = f"{title} {description}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in combined for word in keywords):
            return category
    return "General"

        # --- 4. choose snippet ---
    chosen_snippet = choose_relevant_snippet(title, context_list or [])
    if chosen_snippet:
        enhanced_description = f"{title.strip().capitalize()} — {chosen_snippet}"
    else:
        enhanced_description = (
            f"{title.strip().capitalize()} — remember to stay focused and well‑prepared."
        )

    # ── 5. Return the suggestion dict ───────────────────────────────────────────
    return {
        "priority_score": priority,
        "suggested_deadline": str(deadline),
        "suggested_category": category,
        "enhanced_description": enhanced_description,
    }
