import random

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from TheEvent.models import Ticket
from TheEvent.views import manage_tickets


# Test the "manage_tickets" function
class TestUtility(TestCase):
    def setUp(self) -> None:
        # create a fake user
        self.user = User.objects.create_user(username='testUser', email='testUser@email.com', password='password')

    def test_buy_available_ticket(self):
        ticket = Ticket.objects.create(type='testType1', price=random.randint(20, 200), available_tickets=100)
        result = manage_tickets(ticket, self.user)
        self.assertEqual(result.available_tickets, 99)

    def test_buy_unavailable_ticket(self):
        ticket = Ticket.objects.create(type='testType1', price=random.randint(20, 200), available_tickets=0)
        result = manage_tickets(ticket, self.user)
        self.assertEqual(result, None)

