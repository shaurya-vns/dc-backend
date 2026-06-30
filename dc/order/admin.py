from django.contrib import admin
from .models import OrderModel
 
@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in OrderModel._meta.fields]

    search_fields = (
        "id",
        "user__phone",
        "user__name",
        "subscription__id",
        "subOwner__phone",
        "subOwner__name",
    )

    list_filter = (
        "status",
        "meal_type",
        "delivery_date",
        "created_at",
        "subOwner",
    )

    list_select_related = (
        "user",
        "subOwner",
        "subscription",
    )

    date_hierarchy = "delivery_date"

    ordering = ("-created_at",)