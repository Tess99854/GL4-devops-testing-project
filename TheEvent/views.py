from typing import Optional

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers

from TheEvent.models import Ticket


class TokenObtainCustom(TokenObtainPairView):
    serializer_class = serializers.CustomJWTSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tickets(request) -> Response:
    tickets = Ticket.objects.all()
    serializer = serializers.TicketSerializer(tickets, many=True)
    return Response({"tickets": serializer.data})


@api_view(['GET'])
def get_users(request) -> Response:
    users = User.objects.all()
    serializer = serializers.UserSerializer(users, many=True, exclude=('password',))
    return Response({"users": serializer.data})


@api_view(['POST'])
def add_ticket(request) -> Response:
    serializer = serializers.TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request) -> Response:
    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response("User have been created successfully")
    else:
        return Response(serializer.errors)


def manage_tickets(ticket, user) -> Optional[Ticket]:
    if ticket.available_tickets != 0:
        ticket.sold_tickets.add(user)
        ticket.available_tickets -= 1
        ticket.save()
        return ticket
    else:
        return None


@api_view(['GET'])
def buy_ticket(request) -> Response:
    user = request.user
    ticket_type = request.GET.get('ticket_type')

    if not ticket_type:
        return Response("please add a ticket type", status=status.HTTP_400_BAD_REQUEST)

    try:
        ticket = Ticket.objects.get(type=ticket_type)
    except Ticket.DoesNotExist:
        return Response("This ticket type does not exist", status=status.HTTP_404_NOT_FOUND)

    if not manage_tickets(ticket, user):
        return Response("No more tickets available for this event", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Congratulation on your new ticket!", status=status.HTTP_200_OK)
