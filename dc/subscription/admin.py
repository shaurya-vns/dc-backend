from django.contrib import admin
from .models import SubscriptionModel
 
@admin.register(SubscriptionModel)
class SubscriptionAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in SubscriptionModel._meta.fields]