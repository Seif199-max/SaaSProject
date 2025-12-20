from datetime import timedelta, timezone

from .models import Plan,Subscription


def get_active_plans():

    return Plan.objects.filter(is_active=True).order_by('price_per_month')


def get_default_plan():
    default_plan = Plan.objects.filter(price_per_month=0, is_active=True).first()
    if not default_plan:
        raise Exception('No default plan found')
    return default_plan


def can_user_subscribe(user, plan):
    if Subscription.objects.filter(user=user, is_active=True).exists():
        return False
    if not plan.is_active:
        return False
    return True

def calculate_end_date(start_date, plan):

    if hasattr(plan, 'duration_months'):
        return start_date + timedelta(days=30*plan.duration_months)
    return start_date + timedelta(days=30)

def renew_subscription(subscription):

    if subscription.end_date is None or subscription.end_date < timezone.now():
        subscription.start_date = timezone.now()
        subscription.end_date = calculate_end_date(subscription.start_date, subscription.plan)
        subscription.is_active = True
        subscription.status = 'active'
        subscription.save()

def create_subscription(user, plan, auto_renew):
    subscription = Subscription.objects.create(
        user=user,
        plan=plan,
        start_date=timezone.now(),
        auto_renew=auto_renew,
        is_active=True,
        status="active"
    )

    if auto_renew:
        subscription.end_date = calculate_end_date(subscription.start_date, plan)
        subscription.save()

    return subscription