# AI Learning Log — CampusFlow

This log records learning points connected to the implementation and verification work in this repository. References point to actual project files and merged pull requests. The entries are reflections, not a verbatim transcript of prompts; each fellow should adjust the wording to match their own experience before assessment submission.

## Kristopher Okoh — Engineer A

### Entry 1: Validate before mutating shared state

- **Concept:** Input validation and keeping a failed operation from partially changing the ticket list.
- **Project evidence:** `campusflow/tickets.py`; [PR #13 — ticket creation and validation](https://github.com/kristopher1027/campus-flow/pull/13).
- **My verification:** `tests/test_tickets.py` includes `test_failed_creation_leaves_list_unchanged`, which snapshots the list and checks that invalid creation does not append a ticket.
- **Critical evaluation:** It is not enough for an error message to appear; the state must also remain unchanged. A review suggestion is only useful if the test checks that invariant, not merely that an exception was raised.
- **Changed/rejected advice:** No specific AI advice change is recorded in the repository evidence; add a concrete example here if one occurred.

### Entry 2: Make priority rules explicit and test boundaries

- **Concept:** Ordered business rules can overlap, so rule order and boundary tests matter.
- **Project evidence:** `calculate_priority()` in `campusflow/tickets.py`; [PR #15 — priority engine](https://github.com/kristopher1027/campus-flow/pull/15).
- **My verification:** `tests/test_tickets.py` covers the required priority examples and boundary cases such as 9 versus 10 affected users.
- **What I learned:** The high-urgency-and-large-impact condition must be checked before the broader high-urgency-or-large-impact condition, otherwise a critical ticket would be classified as high.
- **Changed/rejected advice:** No specific change to AI advice is recorded; document one only if it reflects what actually happened.

### Entry 3: Persistence failures must not look like an empty database

- **Concept:** Missing data and corrupted data are different situations and should not have the same recovery behavior.
- **Project evidence:** `campusflow/storage.py`; `tests/test_storage.py`; [PR #18 — JSON storage](https://github.com/kristopher1027/campus-flow/pull/18).
- **My verification:** Storage tests check that a missing file returns an empty list, malformed JSON raises `StorageError`, and a corrupt file is not overwritten.
- **Critical evaluation:** Automatically resetting to an empty list after a parse error would make the CLI seem to work but could destroy users' existing tickets on the next save. A safer design stops and requires the damaged file to be handled explicitly.
- **Changed/rejected advice:** No specific AI advice change is recorded; add a real example if applicable.

## Moshel9ice — Engineer B

### Entry 1: Encode workflow rules as explicit transitions

- **Concept:** A workflow should define allowed state changes instead of accepting any status supplied by a user.
- **Project evidence:** `transition_status()` in `campusflow/workflow.py`; `tests/test_workflow.py`; [PR #12 — assignment, workflow, queue and reports](https://github.com/kristopher1027/campus-flow/pull/12).
- **My verification:** Tests check that an unassigned ticket cannot start, an assigned ticket can move to `in_progress`, and an in-progress ticket can be resolved.
- **Critical evaluation:** A happy-path test alone would not prove the workflow is enforced. Invalid transitions and the assignment prerequisite need their own assertions.
- **Changed/rejected advice:** No specific AI advice change is recorded; document a real example if one occurred.

### Entry 2: Prioritize the active queue deterministically

- **Concept:** A work queue should show actionable tickets first and have a stable tie-breaker for tickets with equal priority.
- **Project evidence:** `work_queue()` in `campusflow/reports.py`; `tests/test_reports.py`; [PR #12](https://github.com/kristopher1027/campus-flow/pull/12).
- **My verification:** The tests cover exclusion of resolved tickets, priority ordering, and numeric ID ordering for equal-priority tickets.
- **What I learned:** Sorting IDs as strings can put `T010` before or after IDs unexpectedly in more general ID formats; parsing the numeric suffix makes the intended ordering explicit.
- **Changed/rejected advice:** No specific AI advice change is recorded; add one only if it reflects the actual development process.

### Entry 3: Keep reports separate from terminal interaction

- **Concept:** Reporting logic is easier to test when counting and sorting are separated from printing menu output.
- **Project evidence:** `generate_report()`, `report_summary()`, and `format_report()` in `campusflow/reports.py`; `tests/test_reports.py`; [PR #17 — ticket summary reports](https://github.com/kristopher1027/campus-flow/pull/17).
- **My verification:** Tests check empty reports, totals, counts by status and priority, and consistent formatting. The CLI calls report functions from `main.py`.
- **Critical evaluation:** A report can display plausible output while still omitting zero-count statuses or priorities. Tests should check the complete result shape, not just one visible count.
- **Changed/rejected advice:** No specific AI advice change is recorded; add a concrete example if one occurred.

## Before submitting

The code and PR references above are verifiable, but personal reflection must remain truthful. Each fellow should replace any generic wording with the actual concept discussed with AI, what they independently ran or inspected, and any advice they changed or rejected. Do not claim an AI suggestion was accepted, rejected, or tested unless that really happened.
