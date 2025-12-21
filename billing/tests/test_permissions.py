from datetime import timedelta
from django.test import TestCase
from accounts.models import User
from billing.models import Plan, Subscription
from billing.permissions import IsOwnerOrAdmin
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.utils import timezone

class IsOwnerOrAdminPermissionTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = IsOwnerOrAdmin()

        self.owner = User.objects.create_user(email="owner@owner.com",password='123')
        self.other_user = User.objects.create_user(email="other@other.com",password='123')
        self.admin = User.objects.create_superuser(email="a@a.com",password= "123")

        self.plan = Plan.objects.create(
            name="Pro",
            slug='Pro',
            price_per_month='100',
            max_projects='10',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        self.subscription = Subscription.objects.create(
            user=self.owner,
            plan=self.plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_owner_can_access(self):
        request = self.factory.get("/")
        request.user = self.owner
        view = None

        self.assertTrue(
            self.permission.has_object_permission(
                request, view, self.subscription
            )
        )

    def test_admin_can_access(self):
        request = self.factory.get("/")
        request.user = self.admin
        view = None

        self.assertTrue(
            self.permission.has_object_permission(
                request, view, self.subscription
            )
        )

    def test_other_user_cannot_access(self):
        request = self.factory.get("/")
        request.user = self.other_user
        view = None

        self.assertFalse(
            self.permission.has_object_permission(
                request, view, self.subscription
            )
        )
