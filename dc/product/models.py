from django.db import models
from dc.base_model import BaseModel
from django.contrib.postgres.fields import ArrayField
from users.models import UserModel

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

    CATEGORY = (
        ("daily_ghar_ka_khana", "Daily Ghar Ka Khana Plans"),
        ("pocket_friendly_meals", "Pocket Friendly Meals Plans"),
        ("desi_rice_bowl_combos", "Desi Rice Bowl Combos Plans"),
        ("fitness_meals", "Fitness Meal Plans"),
    )

    DAY_CHOICES = (
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    )

    subOwner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"userType": UserModel.SUB_OWNER},
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY,
        default="daily_ghar_ka_khana"
    )
    
    plan_type = models.CharField(
        max_length=100,
        choices=PLAN_TYPES,
        default="breakfast"
    )

    day = models.CharField(
        max_length=3,
            choices=DAY_CHOICES,
            default='mon'
        )

    name = models.CharField( max_length=500, default='')
    title = models.CharField( max_length=500, default='')

    description = models.TextField(default='')

    is_active = models.BooleanField(
        default=True
    )

    images = ArrayField(
        models.CharField(max_length=500),
        blank=True,
        default=list
    )

    offer = models.ForeignKey(
        "offer.OfferModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
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
    
 