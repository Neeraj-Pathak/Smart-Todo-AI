from datetime import datetime, timedelta
import random

def generate_task_suggestions(title, description, context_list=None):
    # Simple keyword-based logic
    keywords = (title + " " + description).lower()

    # Priority score logic
    priority = 10 if "urgent" in keywords or "today" in keywords else random.uniform(4, 8)

    # Deadline logic
    deadline = datetime.now().date() + timedelta(days=2)
    if "today" in keywords or "urgent" in keywords:
        deadline = datetime.now().date()

    # Category suggestion
    if "email" in keywords:
        category = "Communication"
    elif "project" in keywords:
        category = "Work"
    elif "buy" in keywords:
        category = "Shopping"
    else:
        category = "General"

    # Enhanced description
    enhanced = description + " (Auto-enhanced based on task urgency and context.)"

    return {
        "priority_score": round(priority, 2),
        "suggested_deadline": str(deadline),
        "suggested_category": category,
        "enhanced_description": enhanced
    }
