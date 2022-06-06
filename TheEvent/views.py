from django.contrib.auth.models import User
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
@permission_classes([AllowAny])
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
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request) -> Response:
    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response("User have been created successfully")
    else:
        return Response(serializer.errors)
