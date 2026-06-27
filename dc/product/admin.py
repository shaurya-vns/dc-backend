from django.contrib import admin
from .models import ProductModel, ProductPricingModel, MealTypeModel

class ProductPricingInline(admin.TabularInline):
    model = ProductPricingModel
    extra = 1


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "plan_type",
        "is_active",
        "created_at",
        'subOwner'
    )

    list_filter = (
        "plan_type",
        "is_active",
    )

    search_fields = (
        "name",
        "plan_name",
        "short_description",
    )

    inlines = [ProductPricingInline]

    ordering = ("-created_at",)
 

@admin.register(ProductPricingModel)
class ProductPricingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "days",
        "price",
        "is_best_offer",
    )

    list_filter = (
        "days",
        "is_best_offer",
    )

    search_fields = (
        "product__name",
    )

@admin.register(MealTypeModel)
class MealTypeAdmin(admin.ModelAdmin):

    list_display = ("id", "name")