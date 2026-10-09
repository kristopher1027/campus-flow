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


## JSON persistence (Issue #8)
- `storage.py` owns `save_tickets(tickets, path)` and `load_tickets(path)`; other modules call these and never touch the file directly.
- Missing file: `load_tickets` returns `[]` (fresh start).
- Malformed JSON or wrong structure (not a list of dicts): raises `StorageError`; the file is never modified by a failed load.
- `StorageError` is separate from `ValueError`, so a storage failure stops the program instead of being treated as bad user input.
- `main.py` stops on `StorageError` at startup, because continuing with an empty list and saving would overwrite the real data.
- Saving writes to a `.tmp` file and then uses `os.replace`, so an interrupted save cannot leave a half-written file.
- IDs stay unique after reload because `generate_next_id` uses the highest existing ID + 1.
- Tests use `tempfile`, never the real `data/tickets.json`.