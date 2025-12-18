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
