# CampusFlow

A command-line ticket management system for Learn2Earn campus technical support.

## Problem

Campus staff receive technical requests — Wi-Fi outages, faulty laptops, broken development environments, inaccessible platforms — through informal channels. Reports get lost, priorities are unclear, and no one knows who is working on what.

CampusFlow records every ticket, calculates priority using a fixed rule set, assigns responsibility, tracks progress through a workflow, and generates reports. It runs entirely in the terminal using only the Python standard library.

## Fellows and contributions

- **Kristopher (Engineer A)** — ticket creation, input validation, priority engine, JSON storage, and the README.
- **Moshel9ice (Engineer B)** — assignment, status workflow, work queue, reports, and CLI menu handlers.

Both fellows wrote automated tests for their own features and reviewed each other's pull requests before merging.

## Python version

Python 3.10 or later. No third-party packages required — standard library only (`json`, `os`, `unittest`).

## Project structure
campus-flow/
├── README.md
├── .gitignore
├── main.py
├── campusflow/
│ ├── init.py
│ ├── tickets.py
│ ├── workflow.py
│ ├── reports.py
│ └── storage.py
├── tests/
│ ├── test_tickets.py
│ ├── test_workflow.py
│ ├── test_reports.py
│ └── test_storage.py
└── docs/
├── design-decisions.md
└── ai-learning-log.md

text

## How to run

1. Clone the repository:

   ```bash
   git clone https://github.com/kristopher1027/campus-flow.git
   cd campus-flow
Run the program:

bash
python3 main.py
Choose a menu option by typing its number and pressing Enter.

Menu options
text
--- CampusFlow ---
1. Create ticket
2. List tickets
3. View ticket
4. Assign ticket
5. Change status
6. Work queue
7. Report
8. Exit
How to test
From the project root:

bash
python3 -m unittest discover -s tests -v
All tests should pass. The suite covers priority boundaries, validation, workflow transitions, queue ordering, reports, and storage round-trips.

Priority rules
Priority is calculated by calculate_priority() in campusflow/tickets.py. Rules are applied in order and the first match wins:

Rule	Condition	Result
1	high urgency AND affected_users >= 10	critical
2	high urgency OR affected_users >= 10	high
3	medium urgency OR affected_users >= 3	medium
4	all other valid tickets	low
Status rules
A ticket's status follows a fixed workflow enforced by transition_status() in campusflow/workflow.py:

From	To	Allowed?
open	in_progress	Only if assigned_to is not None
in_progress	resolved	Yes
resolved	open	Yes (reopen)
any other	—	Rejected with ValueError
An unassigned ticket cannot move to in_progress. A resolved ticket cannot be modified until it is explicitly reopened to open.

Where data is saved
Tickets are saved to data/tickets.json (git-ignored).

The file is created automatically on first save.

To start fresh, delete the file:

bash
rm data/tickets.json
A missing file is treated as a fresh start (no error).

A malformed file raises a clear error instead of silently wiping data.

Known limitations
Ctrl+C during input is handled (saves before exit), but hard-killing the terminal may lose the last unsaved change.

No user authentication — anyone with terminal access can create, assign, or transition tickets.

Single-user CLI with no concurrent access control. Running two instances at once can overwrite each other's changes.

Priority rules are fixed in code; there is no admin UI to change them.

No historical log of status changes — only the current state is stored.

Pull requests
Engineer A: PR_LINK_A

Engineer B: PR_LINK_B

CLI menu (Issue #9): PR_LINK_9

Documentation (Issue #11): PR_LINK_11
