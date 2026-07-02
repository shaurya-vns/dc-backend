from django.contrib import admin
from onetimeorder.models import OneTimeOrderModel
 
@admin.register(OneTimeOrderModel)
class OneTimeOrderAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in OneTimeOrderModel._meta.fields]