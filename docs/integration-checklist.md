# Integration Checklist (Issue #10)

Automated integration results recorded from `main` at commit
[`0fb9b8b14ec92af82197ce94941e15b9d0282244`](https://github.com/kristopher1027/campus-flow/commit/0fb9b8b14ec92af82197ce94941e15b9d0282244).

## Automated tests

- **Command:** `python3 -m unittest discover -s tests -v`
- **Result:** 59 tests ran; all passed (`OK`).
- **Full output:** [`docs/test-output.txt`](test-output.txt)

## Required scenarios (guide 6.1)

- [x] 1. High urgency + 12 users → critical: `TestPriority.test_required_acceptance_scenarios`
- [x] 2. High urgency + 2 users → high: `TestPriority.test_required_acceptance_scenarios`
- [x] 3. Low urgency + 4 users → medium: `TestPriority.test_required_acceptance_scenarios`
- [x] 4. Low urgency + 1 user → low: `TestPriority.test_required_acceptance_scenarios`
- [x] 5. Zero affected users rejected: `TestInvalidInput.test_bad_affected_users_rejected`
- [x] 6. Unassigned ticket cannot move to `in_progress`: `TestTransitionStatus.test_unassigned_cannot_start_progress`
- [x] 7. Assigned ticket moves from `open` → `in_progress` → `resolved`: `TestTransitionStatus.test_assigned_can_progress_to_in_progress` and `TestTransitionStatus.test_in_progress_to_resolved`
- [x] 8. Queue sorted by priority then numeric ID: `TestWorkQueue.test_orders_by_priority` and `TestWorkQueue.test_tie_broken_by_numeric_id`
- [x] 9. Saving and reloading preserves tickets: `TestStorage.test_round_trip_preserves_tickets`
- [x] 10. Creating after reload does not duplicate IDs: `TestStorage.test_ids_stay_unique_after_reload`

## Manual checks

The committed test output records automated tests only. These manual checks are **not documented as completed** and should be performed before marking them done.

- [ ] Restart persistence: manual result not recorded.
- [ ] Unique IDs after reload: manual result not recorded.
- [ ] Invalid transition rejected: manual result not recorded.
- [ ] Corrupted file produces a clear error and is not overwritten: manual result not recorded. Automated coverage exists in `TestStorage.test_corrupt_json_raises_storage_error` and `TestStorage.test_corrupt_file_is_not_overwritten`.

## Defects found

No defects are reported in the recorded automated test run. This does not establish that manual checks or untested scenarios are defect-free.
