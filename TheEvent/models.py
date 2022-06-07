from django.contrib.auth.models import User
from django.db import models

User._meta.get_field('email')._unique = True


class Ticket(models.Model):
    type = models.CharField(max_length=200, unique=True)
    price = models.FloatField(default=0)
    available_tickets = models.IntegerField(default=100)
    sold_tickets = models.ManyToManyField(User)
