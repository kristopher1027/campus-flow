PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def get_ticket(tickets, ticket_id):
    """Return the ticket with the given ID, or raise ValueError."""
    for t in tickets:
        if t["id"] == ticket_id:
            return t
    raise ValueError(f"Unknown ticket ID: {ticket_id}")


def list_tickets(tickets):
    """Return the full ticket list."""
    return tickets


def work_queue(tickets):
    """Return open + in_progress tickets sorted by priority, then numeric ID."""
    queue = [t for t in tickets if t["status"] in ("open", "in_progress")]

    def sort_key(ticket):
        priority_rank = PRIORITY_ORDER.get(ticket["priority"], 99)
        try:
            numeric_id = int(ticket["id"][1:])
        except (ValueError, IndexError):
            numeric_id = 9999
        return (priority_rank, numeric_id)

    return sorted(queue, key=sort_key)


def report_summary(tickets):
    """Return totals by status and by priority. Handles zero tickets."""
    by_status = {"open": 0, "in_progress": 0, "resolved": 0}
    by_priority = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for t in tickets:
        if t["status"] in by_status:
            by_status[t["status"]] += 1
        if t["priority"] in by_priority:
            by_priority[t["priority"]] += 1

    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }
