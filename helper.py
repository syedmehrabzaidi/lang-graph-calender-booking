from datetime import datetime, timedelta
import re

def parse_prompt(prompt):
    """
    Parse the user prompt to extract recipient email, meeting time, and duration.
    Example: "book my meeting with xyz@gmail.com at 2 PM for 1 hour"
    """
    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', prompt)
    if not email_match:
        raise ValueError("No email found in the prompt.")
    recipient_email = email_match.group()

    # Extract time (default to 1 hour from now if not specified)
    now = datetime.utcnow()
    default_start_time = now + timedelta(hours=1)
    default_end_time = default_start_time + timedelta(hours=1)

    # Simple parsing for time and duration (can be enhanced with NLP)
    if "at" in prompt:
        time_str = re.search(r'at\s+(\d{1,2}\s?(?:AM|PM|am|pm))', prompt)
        if time_str:
            start_time = datetime.strptime(time_str.group(1), '%I %p').replace(year=now.year, month=now.month, day=now.day)
            end_time = start_time + timedelta(hours=1)
        else:
            start_time, end_time = default_start_time, default_end_time
    else:
        start_time, end_time = default_start_time, default_end_time

    return recipient_email, start_time, end_time