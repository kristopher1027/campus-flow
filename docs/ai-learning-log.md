# AI Learning Log — CampusFlow

Each fellow records at least three AI interactions. At least one interaction per fellow documents how an AI suggestion was verified, corrected, improved, or rejected.

> **Accuracy note:** These entries are first-person reflections supplied for this log. Each fellow should review and edit their section so it accurately represents their own experience before assessment submission.

---

## Fellow A — Christopher Okoh

### Interaction 1 — JSON round-trip with `json.dump` and `json.load`

- **Problem:** I needed to save the ticket list to a file and load it back on startup, without losing data or crashing when the file was missing.
- **My initial understanding:** I thought I had to manually check for the file first and use `try/except` around `open`.
- **Prompt to AI:** “Explain `json.dump()` and `json.load()` with a five-line example unrelated to my project. Then quiz me on the difference between `dump` and `dumps`. I want to write the storage module myself.”
- **Useful AI guidance:** `json.dump(obj, f)` writes to an open file handle and `json.load(f)` reads from one. `dumps` and `loads` are the string versions. A missing file needs to be handled explicitly.
- **My independent experiment/test:** I wrote a small script in `/tmp` that saved `{"a": 1}` to a file and read it back, then added a round-trip test in `tests/test_storage.py`.
- **Verification source or result:** Ran `python3 -m unittest discover -s tests -v`; the storage tests passed.
- **Decision:** Accepted the round-trip pattern and handled a missing data file as an empty ticket list.
- **Related project evidence:** [`campusflow/storage.py`](../campusflow/storage.py), [`tests/test_storage.py`](../tests/test_storage.py).
- **What I can now explain without AI:** `json.dump` writes an object to a stream while `json.dumps` returns a JSON string. `json.load` reads JSON from a stream; malformed JSON raises `JSONDecodeError`, which the application must handle deliberately.

### Interaction 2 — Validating input without relying only on `str.isdigit()`

- **Problem:** I wanted to reject invalid `affected_users` input—including zero, negative numbers, decimals, and text—with a clear error.
- **My initial understanding:** I planned to use `int(input())` inside a `try/except` block. It worked, but I wanted to understand the alternatives and their trade-offs.
- **Prompt to AI:** “Show me the difference between `str.isdigit()` and `try/except int()` for validating positive integers, with a small example. Give me the trade-offs, not the code for my project.”
- **Useful AI guidance:** `.isdigit()` returns true for strings such as `"0"` and for some Unicode digits. Parsing with `int()` still requires a separate range check.
- **My independent experiment/test:** I compared both approaches with `"12"`, `"0"`, `"-3"`, `"2.5"`, `"abc"`, and `"١٢٣"`.
- **Verification source or result:** The experiment confirmed that `.isdigit()` alone does not validate a positive integer. I chose integer parsing with an explicit greater-than-zero check.
- **Decision:** **Improved** the approach by combining `try/except int()` with a range check, rather than relying on `.isdigit()`.
- **Related project evidence:** [`campusflow/tickets.py`](../campusflow/tickets.py), [`tests/test_tickets.py`](../tests/test_tickets.py).
- **What I can now explain without AI:** A string digit check is not the same as validating the domain rule. Parsing and then checking the allowed range makes the intended constraint explicit.

### Interaction 3 — Critical evaluation: AI suggested a global counter for ticket IDs

- **Problem:** I needed to generate unique ticket IDs such as `T001`, `T002`, and so on.
- **My initial understanding:** I asked AI for a simple counter.
- **Prompt to AI:** “How do I generate sequential ticket IDs in Python?”
- **Useful AI guidance:** AI suggested a counter that increments and formats the value, for example `f"T{counter:03d}"`. That is simple while the counter remains alive.
- **My independent experiment/test:** I traced a restart scenario: create three tickets, exit, reload from JSON, and create a fourth ticket. An in-memory counter would reset and could generate an ID already in use.
- **Verification source or result:** The restart scenario showed that a process-local counter is insufficient for persisted data. The design decision is documented in [`docs/design-decisions.md`](design-decisions.md), and ID behavior is covered in [`tests/test_tickets.py`](../tests/test_tickets.py).
- **Decision:** **Rejected** the global-counter suggestion for this persisted workflow. The next ID must be derived from the stored tickets.
- **Related project evidence:** [`campusflow/tickets.py`](../campusflow/tickets.py), [`docs/design-decisions.md`](design-decisions.md), [`tests/test_tickets.py`](../tests/test_tickets.py).
- **What I can now explain without AI:** Persistent systems cannot rely on an in-memory counter that resets between runs. ID generation must account for IDs already present in saved data.

---

## Fellow B — Moses Attah

### Interaction 1 — Custom sort key with tuple ordering

- **Problem:** I needed to sort tickets by priority first, then by numeric ticket ID. I did not understand how `sorted()` could handle two levels of ordering.
- **My initial understanding:** I thought I would need to sort twice—once by ID and once by priority.
- **Prompt to AI:** “Explain how Python's `sorted()` with a tuple key handles two-level ordering, with a small unrelated example. Don't write my project's code.”
- **Useful AI guidance:** A tuple key such as `(priority_rank, numeric_id)` sorts by the first element and uses the second to break ties.
- **My independent experiment/test:** I compared a tuple-key sort with a two-pass approach and checked that both produced the expected order.
- **Verification source or result:** The behavior is covered by [`tests/test_reports.py`](../tests/test_reports.py), including tests for priority ordering and numeric-ID tie-breaking.
- **Decision:** Accepted the tuple-key approach because it expresses both sort criteria in one key.
- **Related project evidence:** [`campusflow/reports.py`](../campusflow/reports.py), [`tests/test_reports.py`](../tests/test_reports.py), commit `06df50b`.
- **What I can now explain without AI:** Python compares tuples lexicographically: it compares the first element and consults later elements when earlier elements tie.

### Interaction 2 — Guard clauses versus nested conditionals

- **Problem:** In `transition_status`, I needed to reject invalid status transitions without deeply nested conditionals.
- **My initial understanding:** I used nested `if` blocks, but the logic became difficult to read and I missed a branch.
- **Prompt to AI:** “Show me the guard-clause pattern for validating a multi-branch state machine, with a tiny unrelated example. I want to write the project code myself.”
- **Useful AI guidance:** Guard clauses handle invalid cases early with a return or exception, keeping the valid path less nested.
- **My independent experiment/test:** I refactored the transition logic to check valid transitions and raise `ValueError` for invalid ones. I then ran the targeted invalid-transition tests.
- **Verification source or result:** The targeted workflow tests passed, including invalid transitions and transitions that must not skip required states.
- **Decision:** Accepted the guard-clause pattern because it made the allowed transitions easier to inspect.
- **Related project evidence:** [`campusflow/workflow.py`](../campusflow/workflow.py), [`tests/test_workflow.py`](../tests/test_workflow.py), commit `dcc5570`.
- **What I can now explain without AI:** Guard clauses make validation paths explicit and reduce nesting, but the allowed transitions still need to be defined and tested correctly.

### Interaction 3 — Critical evaluation: AI suggested alphabetical priority sorting

- **Problem:** I asked AI how to sort a list of dictionaries by a string `priority` field.
- **My initial understanding:** I initially expected a straightforward sort by the field to match the required priority order.
- **Prompt to AI:** “How do I sort a list of dicts by a string `priority` field?”
- **Useful AI guidance:** AI suggested `sorted(tickets, key=lambda t: t["priority"])`, which sorts the values alphabetically.
- **My independent experiment/test:** I compared alphabetical ordering with the required semantic order: `critical`, `high`, `medium`, `low`. Alphabetical ordering puts `low` before `medium`, which violates the specification.
- **Verification source or result:** The required order is defined by the project specification and tested in [`tests/test_reports.py`](../tests/test_reports.py).
- **Decision:** **Rejected** alphabetical sorting and used an explicit priority-rank mapping in the report implementation.
- **Related project evidence:** [`campusflow/reports.py`](../campusflow/reports.py), [`tests/test_reports.py`](../tests/test_reports.py), commit `06df50b`.
- **What I can now explain without AI:** Alphabetical order is not a substitute for a domain-specific ranking. When a specification defines semantic order, encode that order explicitly and test it.

---

