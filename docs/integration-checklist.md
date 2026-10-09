# Integration Checklist (Issue #10)

Run on `main` at commit: <PASTE git log --oneline -1>

## Automated tests
- Command: `python3 -m unittest discover -s tests -v`
- Result: Ran <XX> tests, <OK / FAILED>
- Full output: `docs/test-output.txt`

## Required scenarios (guide 6.1)
- [ ] 1. High + 12 users → critical: <test name>
- [ ] 2. High + 2 users → high: <test name>
- [ ] 3. Low + 4 users → medium: <test name>
- [ ] 4. Low + 1 user → low: <test name>
- [ ] 5. Zero affected users rejected: <test name>
- [ ] 6. Unassigned cannot move to in_progress: <test name>
- [ ] 7. Assigned ticket open → in_progress → resolved: <test name>
- [ ] 8. Queue sorted by priority then numeric ID: <test name>
- [ ] 9. Save and reload preserves tickets: <test name>
- [ ] 10. Create after reload, no duplicate IDs: <test name>

## Manual checks
- [ ] Restart persistence: <what I did and saw>
- [ ] Unique IDs after reload: <what I did and saw>
- [ ] Invalid transition rejected: <what I did and saw>
- [ ] Corrupted file: clear error, file not overwritten: <what I did and saw>

## Defects found
- <none, or list issue numbers and fix PRs>
