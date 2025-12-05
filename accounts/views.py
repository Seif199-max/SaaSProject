from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


