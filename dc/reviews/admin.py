from django.contrib import admin
from .models import ReviewModel
 
@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in ReviewModel._meta.fields]