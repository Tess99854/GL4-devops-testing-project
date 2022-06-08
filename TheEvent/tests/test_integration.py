import random

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from django.contrib.auth.models import User

from TheEvent.models import Ticket


# Test the "buy_ticket" view
class TestBuyTicketView(TestCase):
    def setUp(self) -> None:
        # create a fake ticket
        self.ticket = Ticket.objects.create(type='testType', price=random.randint(20, 200), available_tickets=100)
        # register a user
        user = {
            "username": "sarah",
            "email": "sarah@email.com",
            "password": "bestPasswordEver"
        }
        self.client.post(reverse('register'), data=user)

        # authenticate the user we registered
        self.user = User.objects.get(email="sarah@email.com")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_request_without_ticket_type(self):
        response = self.client.get(reverse('buy_ticket'))
        self.assertEqual(response.status_code, 400)

    def test_request_with_wrong_ticket_type(self):
        ticket_type = "Wrong Type"
        response = self.client.get(f"{reverse('buy_ticket')}?ticket_type={ticket_type}")
        self.assertEqual(response.status_code, 404)

    def test_request_with_right_ticket_type(self):
        ticket_type = "testType"
        response = self.client.get(f"{reverse('buy_ticket')}?ticket_type={ticket_type}")
        self.assertEqual(response.status_code, 200)
