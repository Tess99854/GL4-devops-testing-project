# Generated by Django 3.1 on 2022-06-07 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TheEvent', '0002_ticket_sold_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='available_tickets',
            field=models.IntegerField(default=100),
        ),
    ]
