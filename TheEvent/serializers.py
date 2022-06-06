from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from TheEvent.models import Ticket


class DynamicExcludeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)
        super(DynamicExcludeSerializer, self).__init__(*args, **kwargs)
        if exclude is not None:
            not_allowed = set(exclude)
            for field_name in not_allowed:
                self.fields.pop(field_name)


class TicketSerializer(DynamicExcludeSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class UserSerializer(DynamicExcludeSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomJWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(
            username=attrs.get("username")).first()

        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)
