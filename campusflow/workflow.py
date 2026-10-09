def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a staff member.

    Raises ValueError if ticket_id is unknown or staff_name is empty.
    Returns the updated ticket dict on success.
    """
    # 1. Find the ticket by ID
    ticket = None
    for t in tickets:
        if t["id"] == ticket_id:
            ticket = t
            break

    # 2. Reject unknown ID
    if ticket is None:
        raise ValueError(f"Unknown ticket ID: {ticket_id}")

    # 3. Reject empty staff name
    if not staff_name or not staff_name.strip():
        raise ValueError("Staff name cannot be empty")

    # 4. Mutate after validation
    ticket["assigned_to"] = staff_name.strip()
    return ticket


def transition_status(tickets, ticket_id, new_status):
    """Move a ticket through the workflow.

    Allowed transitions:
        open        -> in_progress  (only if assigned_to is not None)
        in_progress -> resolved
        resolved    -> open          (reopen)

    Raises ValueError on unknown ID or invalid transition.
    Returns the updated ticket dict on success.
    """
    ticket = None
    for t in tickets:
        if t["id"] == ticket_id:
            ticket = t
            break

    if ticket is None:
        raise ValueError(f"Unknown ticket ID: {ticket_id}")

    current = ticket["status"]

    if current == "open" and new_status == "in_progress":
        if ticket["assigned_to"] is None:
            raise ValueError(
                "Cannot start an unassigned ticket. Assign it first."
            )
    elif current == "in_progress" and new_status == "resolved":
        pass
    elif current == "resolved" and new_status == "open":
        pass
    else:
        raise ValueError(
            f"Invalid transition: {current} -> {new_status}"
        )

    ticket["status"] = new_status
    return ticket
