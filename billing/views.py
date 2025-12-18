from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Plan, Subscription
from .serializers import PlanSerializer,SubscriptionSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class PlansView(generics.ListCreateAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class PlanView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class SubscriptionsView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

class SubscriptionView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()