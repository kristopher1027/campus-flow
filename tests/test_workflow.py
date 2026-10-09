import unittest
from campusflow.workflow import assign_ticket, transition_status


def make_ticket(tid="T001", status="open", assigned_to=None):
    return {
        "id": tid,
        "title": "Test ticket",
        "category": "Network",
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": status,
        "assigned_to": assigned_to,
    }


class TestAssignTicket(unittest.TestCase):

    def test_assign_unknown_ticket_raises(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T999", "Alice")

    def test_assign_empty_name_raises(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "   ")

    def test_assign_success_sets_field(self):
        tickets = [make_ticket("T001")]
        result = assign_ticket(tickets, "T001", "Alice")
        self.assertEqual(result["assigned_to"], "Alice")
        self.assertEqual(tickets[0]["assigned_to"], "Alice")


class TestTransitionStatus(unittest.TestCase):

    def test_unassigned_cannot_start_progress(self):
        tickets = [make_ticket("T001", status="open", assigned_to=None)]
        with self.assertRaises(ValueError):
            transition_status(tickets, "T001", "in_progress")

    def test_assigned_can_progress_to_in_progress(self):
        tickets = [make_ticket("T001", status="open", assigned_to="Alice")]
        result = transition_status(tickets, "T001", "in_progress")
        self.assertEqual(result["status"], "in_progress")

    def test_in_progress_to_resolved(self):
        tickets = [make_ticket("T001", status="in_progress", assigned_to="Alice")]
        result = transition_status(tickets, "T001", "resolved")
        self.assertEqual(result["status"], "resolved")

    def test_resolved_must_reopen_to_open(self):
        tickets = [make_ticket("T001", status="resolved", assigned_to="Alice")]
        result = transition_status(tickets, "T001", "open")
        self.assertEqual(result["status"], "open")

    def test_resolved_cannot_skip_reopen(self):
        tickets = [make_ticket("T001", status="resolved", assigned_to="Alice")]
        with self.assertRaises(ValueError):
            transition_status(tickets, "T001", "in_progress")

    def test_unknown_ticket_raises(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            transition_status(tickets, "T999", "in_progress")

    def test_invalid_transition_raises(self):
        tickets = [make_ticket("T001", status="open", assigned_to="Alice")]
        with self.assertRaises(ValueError):
            transition_status(tickets, "T001", "resolved")


if __name__ == "__main__":
    unittest.main()
