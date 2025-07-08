from datetime import datetime, timedelta
import random
import re
import json
import requests

today = datetime.now().strftime("%Y-%m-%d") 

CATEGORY_KEYWORDS = {
    "Career": ["resume", "interview", "placement", "linkedin", "job"],
    "Work": ["report", "deck", "meeting", "deadline", "project"],
    "Health": ["meditation", "doctor", "exercise", "yoga", "diet"],
    "Communication": ["email", "message", "chat", "call", "client"],
    "Personal": ["shopping", "family", "birthday", "travel", "movie"],
    "General": ["note", "misc", "task"]
}

def choose_relevant_snippet(title: str, context_list: list[str]) -> str | None:
    """Pick the context line with most word overlap to title (stop‑word‑aware)."""
    if not context_list:
        return None

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

    if best_score > 0 or re.search(r"\b(urgent|today|asap|by\s+\w+)\b", best_line or "", re.I):
        return best_line
    return None

def auto_category(title: str, description: str) -> str:
    combined = f"{title} {description}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in combined for word in keywords):
            return category
    return "General"

def generate_task_suggestions(title: str,
                              description: str = "",
                              context_list: list[str] = None):
    """
    Uses Ollama to generate task suggestions.
    Falls back to rule-based logic if LLM call fails.
    """

    prompt = f"""
You are a productivity assistant.

Today's date is {today}.

Given:
Task title: "{title}"
Task description: "{description}"
Context: {context_list or []}

Respond ONLY in this valid JSON format:

{{
  "priority_score": 8.5,
  "suggested_deadline": "2025-07-10",
  "suggested_category": "Health",
  "enhanced_description": "Practice daily mindfulness meditation at 7:00 am every morning."
}}

Make sure:
- To respond in valid JSON. If no specific deadline is inferred from the task or context, default to today ({today}) as the suggested_deadline. Otherwise, suggest a realistic future date.
- The priority_score is a float between 1 and 10.
- All values are properly quoted.
- Do NOT include any explanation — only the JSON object.
"""



    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # or "llama2" or your preferred Ollama model
                "prompt": prompt,
                "stream": False
            }
        )
        result = response.json()
        return json.loads(result["response"])

    except Exception as e:
        print("Ollama AI error:", e)

        # fallback logic
        priority = round(random.uniform(4, 6), 2)
        deadline = str(datetime.now().date() + timedelta(days=3))
        category = auto_category(title, description)

        snippet = choose_relevant_snippet(title, context_list or [])
        if snippet:
            enhanced_description = f"{title.strip().capitalize()} — {snippet}"
        else:
            enhanced_description = f"{title.strip().capitalize()} — remember to stay focused and well‑prepared."

        return {
            "priority_score": priority,
            "suggested_deadline": deadline,
            "suggested_category": category,
            "enhanced_description": enhanced_description
        }
