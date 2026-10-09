import unittest

from campusflow.tickets import (
    create_ticket,
    generate_next_id,
    validate_affected_users,
)


class TestCreateTicket(unittest.TestCase):

    def test_valid_ticket_has_all_fields(self):
        tickets = []
        ticket = create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)
        expected_keys = {
            "id", "title", "category", "urgency",
            "affected_users", "priority", "status", "assigned_to",
        }
        self.assertEqual(set(ticket.keys()), expected_keys)
        self.assertEqual(len(tickets), 1)

    def test_new_ticket_defaults(self):
        ticket = create_ticket([], "Wi-Fi down", "Network", "high", 15)
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_title_is_stripped(self):
        ticket = create_ticket([], "  Wi-Fi down  ", "Network", "high", 15)
        self.assertEqual(ticket["title"], "Wi-Fi down")

    def test_category_is_normalized(self):
        for raw in ("network", " NETWORK ", "Network"):
            with self.subTest(raw=raw):
                ticket = create_ticket([], "x", raw, "low", 1)
                self.assertEqual(ticket["category"], "Network")

    def test_urgency_is_normalized(self):
        for raw in ("HIGH", " high ", "High"):
            with self.subTest(raw=raw):
                ticket = create_ticket([], "x", "Network", raw, 1)
                self.assertEqual(ticket["urgency"], "high")

    def test_numeric_string_affected_users_accepted(self):
        ticket = create_ticket([], "x", "Network", "low", "15")
        self.assertEqual(ticket["affected_users"], 15)
        self.assertIsInstance(ticket["affected_users"], int)


class TestInvalidInput(unittest.TestCase):

    def test_blank_title_rejected(self):
        for bad in ("", "   ", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    create_ticket([], bad, "Network", "high", 5)

    def test_invalid_category_rejected(self):
        for bad in ("Plumbing", "", "   ", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    create_ticket([], "x", bad, "high", 5)

    def test_invalid_urgency_rejected(self):
        for bad in ("urgent", "", "   ", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    create_ticket([], "x", "Network", bad, 5)

    def test_bad_affected_users_rejected(self):
        for bad in (0, -3, 2.5, "abc", "", "2.5", "-3", True, False, None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_affected_users(bad)

    def test_failed_creation_leaves_list_unchanged(self):
        tickets = []
        create_ticket(tickets, "First", "Network", "low", 1)
        snapshot = [dict(t) for t in tickets]

        with self.assertRaises(ValueError):
            create_ticket(tickets, "Second", "Network", "high", 0)
        with self.assertRaises(ValueError):
            create_ticket(tickets, "Third", "BadCategory", "high", 5)

        self.assertEqual(tickets, snapshot)


class TestIds(unittest.TestCase):

    def test_first_id_is_t001(self):
        self.assertEqual(generate_next_id([]), "T001")

    def test_next_id_after_t009_is_t010(self):
        self.assertEqual(generate_next_id([{"id": "T009"}]), "T010")

    def test_next_id_uses_highest_not_length(self):
        # Two tickets, but the highest number is 5, so the next must be T006.
        tickets = [{"id": "T002"}, {"id": "T005"}]
        self.assertEqual(generate_next_id(tickets), "T006")

    def test_created_tickets_get_sequential_ids(self):
        tickets = []
        first = create_ticket(tickets, "a", "Network", "low", 1)
        second = create_ticket(tickets, "b", "Network", "low", 1)
        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")


if __name__ == "__main__":
    unittest.main()