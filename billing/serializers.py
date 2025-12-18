from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Plan, Subscription
from django.utils import timezone
from .services import can_user_subscribe


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price_per_month",
            "price_per_year",
            "currency",
            "max_projects",
            "features",
            "is_active",
            "created_at",
        ]

    def validate_price_per_month(self, value):
        if value < 0:
            raise ValidationError("Monthly price must be >= 0")
        return value

    def validate_price_per_year(self, value):
        if value is not None and value < 0:
            raise ValidationError("Yearly price must be >= 0")
        return value

    def validate(self, attrs):
        # yearly price >= monthly price
        price_per_month = attrs.get("price_per_month", getattr(self.instance, "price_per_month", 0))
        price_per_year = attrs.get("price_per_year", getattr(self.instance, "price_per_year", 0))

        if price_per_year is not None and price_per_year < price_per_month:
            raise ValidationError("Yearly price cannot be less than monthly price")
        return attrs




class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "plan",
            "start_date",
            "end_date",
            "is_active",
            "auto_renew",
            "payment_status",
        ]
        read_only_fields = ["user", "is_active", "payment_status"]

    def validate(self, attrs):

        user = self.context["request"].user

        plan = attrs.get("plan", getattr(self.instance, "plan", None))

        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))

        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))


        if start_date and end_date and end_date <= start_date:
            raise ValidationError("End date must be after start date")


        if plan and not plan.is_active:
            raise ValidationError("Cannot subscribe to an inactive plan")

        if not self.instance and not can_user_subscribe(user, plan):
            raise ValidationError("User already has an active subscription")

        return attrs
