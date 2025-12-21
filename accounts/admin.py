from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active','is_staff')
    list_filter = ("is_active", "date_joined")
    search_fields = ("email",)
    ordering = ("date_joined",)