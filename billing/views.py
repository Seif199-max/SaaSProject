from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer
from .permissions import IsManagerOrReadOnly, IsOwnerOrAdmin
from.services import create_subscription
class PlanViewSet(viewsets.ModelViewSet):

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsManagerOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class SubscriptionViewSet(viewsets.ModelViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = [ IsOwnerOrAdmin]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    #authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Subscription.objects.all()
        return Subscription.objects.filter(user=user)

    def perform_create(self, serializer):
        plan = serializer.validated_data['plan']
        auto_renew = serializer.validated_data.get('auto_renew', False)

        create_subscription(self.request.user, plan, auto_renew)

