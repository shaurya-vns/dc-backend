from django.contrib import admin
from .models import ProductModel, ProductPricingModel, MealTypeModel

class ProductPricingInline(admin.TabularInline):
    model = ProductPricingModel
    extra = 1


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        "category",
        "name",
        'plan_type',
        'day'
    ] + [
        field.name for field in ProductModel._meta.fields
        if field.name not in ("category", "name", "description", 'id', 'plan_type' , 'title', 'day')
    ]

    ordering = ["name"]

    
    inlines = [ProductPricingInline]


 

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