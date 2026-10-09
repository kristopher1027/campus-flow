"""Ticket creation, validation and priority logic for CampusFlow."""

ALLOWED_CATEGORIES = ("Network", "Hardware", "Software", "Other")
ALLOWED_URGENCIES = ("low", "medium", "high")


def calculate_priority(urgency, affected_users):
    """Placeholder. The real rules are built in Issue #2."""
    return "low"


def validate_title(title):
    """Return the stripped title. Raise ValueError if blank or not a string."""
    if not isinstance(title, str):
        raise ValueError("Title must be text.")
    cleaned = title.strip()
    if cleaned == "":
        raise ValueError("Title cannot be blank.")
    return cleaned


def validate_category(category):
    """Return the properly capitalised category (e.g. ' network ' -> 'Network')."""
    if not isinstance(category, str):
        raise ValueError("Category must be text.")
    cleaned = category.strip().lower()
    for allowed in ALLOWED_CATEGORIES:
        if allowed.lower() == cleaned:
            return allowed
    raise ValueError(
        "Category must be one of: " + ", ".join(ALLOWED_CATEGORIES) + "."
    )


def validate_urgency(urgency):
    """Return the lowercase urgency (e.g. ' HIGH ' -> 'high')."""
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")
    cleaned = urgency.strip().lower()
    if cleaned not in ALLOWED_URGENCIES:
        raise ValueError(
            "Urgency must be one of: " + ", ".join(ALLOWED_URGENCIES) + "."
        )
    return cleaned


def validate_affected_users(value):
    """Return a positive whole number as an int, or raise ValueError."""
    if isinstance(value, bool):
        raise ValueError("Affected users must be a whole number, not True/False.")

    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned.isdigit():
            raise ValueError("Affected users must be a positive whole number.")
        number = int(cleaned)
    elif isinstance(value, int):
        number = value
    else:
        raise ValueError("Affected users must be a positive whole number.")

    if number <= 0:
        raise ValueError("Affected users must be greater than zero.")
    return number


def generate_next_id(tickets):
    """Return the next ID: highest existing number + 1, formatted like 'T001'."""
    highest = max((int(t["id"][1:]) for t in tickets), default=0)
    return f"T{highest + 1:03d}"

def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate everything, then build and append a ticket. Return the ticket."""
    # Validate first, into local variables. If any call raises, the list is untouched.
    title = validate_title(title)
    category = validate_category(category)
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    priority = calculate_priority(urgency, affected_users)
    new_id = generate_next_id(tickets)

    ticket = {
        "id": new_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)   # the very last step that touches the list
    return ticket

