from django.contrib import admin
from .models import CustomerModel

@admin.register(CustomerModel)
class UserAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in CustomerModel._meta.fields]

