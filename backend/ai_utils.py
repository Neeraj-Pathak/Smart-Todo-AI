from datetime import datetime, timedelta
import random
import re

def generate_task_suggestions(title, description, context_list=None):
    context_list = context_list or []
    combined_text = (title + " " + description + " " + " ".join(context_list)).lower()

    # Priority logic
    if any(word in combined_text for word in ["urgent", "today", "asap", "now"]):
        priority = round(random.uniform(8.5, 10), 2)
        deadline = datetime.now().date()
    elif "project" in combined_text:
        priority = round(random.uniform(6, 8), 2)
        deadline = datetime.now().date() + timedelta(days=2)
    else:
        priority = round(random.uniform(4, 6), 2)
        deadline = datetime.now().date() + timedelta(days=3)

    # Category logic
    if "email" in combined_text or "call" in combined_text:
        category = "Communication"
    elif "project" in combined_text or "report" in combined_text:
        category = "Work"
    elif "buy" in combined_text or "shopping" in combined_text:
        category = "Shopping"
    elif "meditate" in combined_text or "health" in combined_text:
        category = "Health"
    else:
        category = "General"

    # Enhanced description (context-aware)
    snippet = next((line for line in context_list if any(kw in line.lower() for kw in title.lower().split())), None)
    if snippet:
        enhanced = f"{title.strip().capitalize()} — {snippet}"
    else:
        enhanced = f"{title.strip().capitalize()} — stay focused and follow through."

    return {
        "priority_score": priority,
        "suggested_deadline": str(deadline),
        "suggested_category": category,
        "enhanced_description": enhanced
    }
