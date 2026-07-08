from django.contrib import admin
from ondemand.models import OnDemandModel
 
@admin.register(OnDemandModel)
class OnDemandAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in OnDemandModel._meta.fields]
