from django.contrib import admin
from contact_us.models import ContactUsModel



@admin.register(ContactUsModel)
class ContactUsAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in ContactUsModel._meta.fields]
