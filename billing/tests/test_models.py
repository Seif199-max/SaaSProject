from datetime import timedelta
from django.test import TestCase
from accounts.models import User
from billing.models import Plan, Subscription
from django.utils import timezone

class SubscriptionModelTest(TestCase):

    def test_create_subscription(self):
        user = User.objects.create_user(email="owner@owner.com",password='123')
        plan =  Plan.objects.create(
            name="Pro",
            slug='Pro',
            price_per_month='100',
            max_projects='10',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        sub = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        self.assertTrue(sub.is_active)
        self.assertEqual(sub.payment_status, 'pending')
