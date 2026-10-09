# Design Decisions — CampusFlow

This document records the shared agreements made by both fellows before implementation.

## 1. Data structure

Tickets are stored in a single `list[dict]` named `tickets`. Each ticket dict has exactly these keys:

| Key | Type | Notes |
|-----|------|-------|
| `id` | str | Auto-generated as `T001`, `T002`, ... |
| `title` | str | Non-empty after strip |
| `category` | str | One of: Network, Hardware, Software, Other |
| `urgency` | str | One of: low, medium, high |
| `affected_users` | int | Positive integer (> 0) |
| `priority` | str | Computed by `calculate_priority` — never set by hand |
| `status` | str | One of: open, in_progress, resolved |
| `assigned_to` | str or None | Staff name, or None if unassigned |

No separate "loan" structure exists — a single list is enough because tickets are the only entity.

## 2. Error handling

- Library functions raise `ValueError` on invalid input.
- Only `main.py` catches `ValueError` and prints a friendly message.
- Only `main.py` calls `input()` and `print()`.
- This keeps library functions pure and testable with `unittest`'s `assertRaises`.

## 3. JSON ownership

`campusflow/storage.py` owns all persistence:

- `load_tickets(path=DEFAULT_PATH)` — reads the JSON file, returns a list. If the file is missing, returns `[]` (fresh start). If the file is malformed, raises `ValueError`.
- `save_tickets(tickets, path=DEFAULT_PATH)` — writes the list to the file as pretty-printed JSON.

`DEFAULT_PATH = "data/tickets.json"`. The `data/` folder is git-ignored.

## 4. ID rule

Ticket IDs are formatted `T001`, `T002`, `T003`, ... `generate_next_id(tickets)` reads the highest existing numeric ID and increments. This guarantees uniqueness even after reload.

## 5. Allowed status transitions

| From | To | Allowed? |
|------|----|----------|
| open | in_progress | Only if `assigned_to` is not None |
| in_progress | resolved | Yes |
| resolved | open | Yes (explicit reopen) |
| any other pair | — | No, raises `ValueError` |

Enforced by `transition_status` in `workflow.py`.

## 6. Queue decision

`work_queue(tickets)` returns only tickets with status `open` or `in_progress` (resolved tickets excluded). Sorted by priority (`critical > high > medium > low`), tie-broken by numeric ticket ID ascending — this matches the spec's requirement that ties break by "earlier numeric ticket ID."

## 7. Normalization

- `urgency` and `category` inputs are normalized to lowercase before validation.
- `title` and `staff_name` are `.strip()`-ed before use.
- Category display names preserve case in output (e.g. "Network") but comparison is case-insensitive.

## Ownership summary

| Area | Owner |
|------|-------|
| Ticket creation, validation, priority engine | Engineer A |
| Assignment, workflow, queue, reports | Engineer B |
| Storage integration, `main.py` | Both |