from django.contrib import admin
from support.models import SupportTicketModel
  
@admin.register(SupportTicketModel)
class SupportAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in SupportTicketModel._meta.fields]

