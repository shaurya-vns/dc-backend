from django.contrib import admin
from support.models import SupportRequestModel
 
@admin.register(SupportRequestModel)
class SupportAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in SupportRequestModel._meta.fields]

