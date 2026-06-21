from django.contrib import admin
from .models import OrderModel
 
@admin.register(OrderModel)
class SubscriptionAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in OrderModel._meta.fields]