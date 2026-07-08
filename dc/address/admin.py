from django.contrib import admin
from address.models import AddressModel



@admin.register(AddressModel)
class AddressAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in AddressModel._meta.fields]
