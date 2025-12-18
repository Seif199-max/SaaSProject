from django.urls import path
from .views import PlansView,PlanView,SubscriptionsView,SubscriptionView


urlpatterns = [
    path("plans", PlansView.as_view()),

    path("plans/<int:pk>", PlanView.as_view()),

    path("subscriptions", SubscriptionsView.as_view()),

   path("subscriptions/<int:pk>", SubscriptionView.as_view()),


]
