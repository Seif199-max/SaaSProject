from django.core.management.base import BaseCommand
from django.utils import timezone
from billing.models import Subscription

class Command(BaseCommand):
    help = "Deactivate expired subscriptions"

    def handle(self, *args, **options):
        now = timezone.now()

        expired = Subscription.objects.filter(
            is_active=True,
            end_date__lt=now
        )

        count = expired.count()

        expired.update(
            is_active=False,
            payment_status="expired"
        )

        self.stdout.write(
            self.style.SUCCESS(f"{count} subscriptions expired successfully")
        )
