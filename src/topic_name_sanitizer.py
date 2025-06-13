import re

def sanitize_topic_name(topic: str, max_length: int = 50) -> str:
    """Make a filesystem-safe, truncated version of the topic string."""
    topic = topic.strip()
    topic = topic.replace("IRB Section:", "").strip()  # Optional: remove prefix
    topic = re.sub(r"[^\w\d\- ]", "", topic)           # Remove symbols
    topic = topic.replace(" ", "_")                    # Convert spaces
    return topic[:max_length]                          # Truncate to safe length