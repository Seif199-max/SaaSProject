from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from accounts.models import User
from billing.models import Plan


class SubscriptionAPITest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="1234"
        )

        self.plan = Plan.objects.create(
            name="Special Plan",
            slug='special',
            price_per_month=100,
            max_projects=10,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        self.client.force_authenticate(user=self.user)

    def test_user_can_subscribe(self):
        url = "/billing/subscriptions/"

        data = {
            'user' : self.user,
            'plan': self.plan.id,
            'start_date' : timezone.now(),
            'end_date' : timezone.now() + timedelta(days=30),
            'created_at' : timezone.now(),
            'updated_at' : timezone.now()
        }

        response = self.client.post(url, data)

        if response.status_code != status.HTTP_201_CREATED:
            print("\n--- Error Details ---")
            print(response.data)
            print("----------------------\n")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)