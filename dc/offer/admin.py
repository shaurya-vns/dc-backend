from django.contrib import admin
from .models import OfferModel
 
@admin.register(OfferModel)
class OfferAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in OfferModel._meta.fields]