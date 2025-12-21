from django.test import TestCase
from accounts.models import User
from billing.models import Plan, Subscription
from django.utils import timezone
from datetime import timedelta
from billing.services import can_user_subscribe


class SubscriptionServiceTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(email="test@example.com", password='123')
        self.plan = Plan.objects.create(
            name="Special Plan",
            slug='special',
            price_per_month=100,
            max_projects=10,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_user_can_subscribe_first_time(self):

        self.assertTrue(can_user_subscribe(self.user, self.plan))

    def test_user_cannot_subscribe_twice(self):


        Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )


        can_subscribe = can_user_subscribe(self.user, self.plan)

        self.assertFalse(can_subscribe, "User Can not subscribe twice")