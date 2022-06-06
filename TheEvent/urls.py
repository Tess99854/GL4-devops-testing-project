from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('login', views.TokenObtainCustom.as_view(), name='token_obtain'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.register, name="register"),
    path('tickets', views.get_tickets, name="tickets"),
    path('users', views.get_users, name="users"),
    path('add_ticket', views.add_ticket, name="add_ticket"),
]
