from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Plan(models.Model):

    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('EGP', 'EGP'),
    )

    name = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=100, unique=True,db_index=True)

    description = models.TextField(blank=True)

    price_per_month = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    price_per_year = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD'
    )

    max_projects = models.PositiveIntegerField()

    features = models.JSONField(default=dict, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price_per_month']
        constraints = [              #DB _ Constrains
            models.CheckConstraint(
                check=models.Q(price_per_month__gte=0),
                name="price_per_month_non_negative"
            ),
            models.CheckConstraint(
                check=models.Q(max_projects__gte=0),
                name="max_projects_non_negative"
            ),
        ]

    def clean(self):    #Bussniess Logic
        # yearly price must be >= monthly price
        if self.price_per_year is not None:
            if self.price_per_year < self.price_per_month:
                raise ValidationError(
                    "Yearly price cannot be less than monthly price"
                )


        if self.price_per_month == 0 and self.price_per_year not in (None, 0):
            raise ValidationError(
                "Free plan cannot have yearly price"
            )

    def __str__(self):
        return self.name




class Subscription(models.Model):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('canceled', 'Canceled'),
        ('pending', 'Pending'),
    )

    user = models.ForeignKey(
       User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        db_index=True
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )

    start_date = models.DateTimeField(default=timezone.now)

    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True,db_index=True)

    auto_renew = models.BooleanField(default=False)

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_active"]),
        ]
        ordering = ['-start_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='end_date_after_start_date'
            ),
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_active=True),
                name='unique_active_subscription_per_user'
            ),
        ]

    def clean(self):
        # End date must be in the future
        if self.end_date <= timezone.now():
            raise ValidationError(
                "End date must be in the future"
            )

        # Expired subscription auto-deactivate
        if self.end_date <= timezone.now():
            self.is_active = False

    def __str__(self):
        return f"{self.user} → {self.plan}"




















