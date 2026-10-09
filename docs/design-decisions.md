# Design Decisions

## Data structures
- Tickets stored in a single `list[dict]` named `tickets`.
- Each ticket has keys: id, title, category, urgency, affected_users, priority, status, assigned_to.
- Ticket IDs auto-generated as T001, T002, ... from the highest existing ID.

## Error handling
- Invalid input raises ValueError.
- Only main.py catches ValueError and prints a friendly message.
- Only main.py calls input() and print().

## Function contracts
- calculate_priority(urgency, affected_users) -> str
- assign_ticket(tickets, ticket_id, staff_name) -> dict
- transition_status(tickets, ticket_id, new_status) -> dict
- work_queue(tickets) -> list[dict]
- report_summary(tickets) -> dict

## Ownership
- Engineer A: ticket creation, validation, priority engine.
- Engineer B: assignment, workflow, queue, reports.
- Both: storage.py, main.py, integration.
