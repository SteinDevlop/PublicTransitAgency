import unittest
from backend.app.models.ticket import Ticket

class TestTicket(unittest.TestCase):
    def setUp(self):
        self.ticket = Ticket(ticket_id=1, status_code=2)

    def test_initialization(self):
        self.assertEqual(self.ticket.ticket_id, 1)
        self.assertEqual(self.ticket.status_code, 2)

    def test_to_dict(self):
        ticket_dict = self.ticket.to_dict()
        self.assertEqual(ticket_dict["ticket_id"], 1)
        self.assertEqual(ticket_dict["status_code"], 2)

    def test_get_fields(self):
        fields = Ticket.get_fields()
        self.assertIn("ticket_id", fields)
        self.assertIn("status_code", fields)

if __name__ == "__main__":
    unittest.main()