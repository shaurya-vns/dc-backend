from django.db import models
from dc.base_model import BaseModel
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class ProductModel(BaseModel):

    PLAN_TYPES = (
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("breakfast_lunch", "Breakfast + Lunch"),
        ("breakfast_dinner", "Breakfast + Dinner"),
        ("lunch_dinner", "Lunch + Dinner"),
        ("breakfast_lunch_dinner", "Breakfast + Lunch + Dinner")
    )

    name = models.CharField( max_length=500,)
    plan_name = models.CharField( max_length=500,)

    
    plan_type = models.CharField(
        max_length=100,
        choices=PLAN_TYPES
    )

    short_description = models.TextField(
 
    )

    include = models.TextField( )

    description = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    images = ArrayField(
        models.CharField(max_length=500),
        blank=True,
        default=list
    )

    def __str__(self):
        return self.name
    

class ProductPricingModel(BaseModel):
    product = models.ForeignKey(
        ProductModel,
        related_name="pricing_options",
        on_delete=models.CASCADE
    )

    days = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_best_offer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.days} Days"
    

class MealTypeModel(BaseModel):
    name = models.CharField(
        max_length=20,
        choices=(
            ("breakfast", "Breakfast"),
            ("lunch", "Lunch"),
            ("dinner", "Dinner"),
        ),
        unique=True
    )

    def __str__(self):
        return self.name