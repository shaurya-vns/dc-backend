from django.contrib import admin
from users.models import UserModel, UserAddress
 
@admin.register(UserModel)
class OwnerAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in UserModel._meta.fields]



@admin.register(UserAddress)
class OwnerAddressAdmin(admin.ModelAdmin):
    # Show all fields in the list view
    list_display = [field.name for field in UserAddress._meta.fields]