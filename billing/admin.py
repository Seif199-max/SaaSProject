from django.contrib import admin
from .models import Subscription, Plan

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "is_active", "start_date", "end_date")
    list_filter = ("is_active", "plan")
    search_fields = ("user__email",)
    ordering = ("-start_date",)

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active",'price_per_month')
    search_fields = ("name",)
    ordering = ("-price_per_month",)
