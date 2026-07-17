# review/service.py

from django.db import transaction
from django.db.models import Avg, Count

from .models import ReviewModel
from product.models import ProductModel
from dc.constant  import *


class ReviewService:

    @staticmethod
    @transaction.atomic
    def create_or_update_review(user, data):

        productId = data["productId"] 
        print('productId  ', productId)

        product = ProductModel.objects.get(
            id =  productId ,
            is_active = True,
        ) 

        if not product:
            raise Exception("Product not found.")

        review, created = ReviewModel.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                "rating": data["rating"],
                "review": data.get("review", ""),
            },
        )

        stats = ReviewModel.objects.filter(
            product=product
        ).aggregate(
            avg_rating=Avg("rating"),
            total_reviews=Count("id"),
        )

        product.rating = round(stats["avg_rating"] or 0, 2)
        product.totalReviews = stats["total_reviews"]
        product.save(update_fields=["rating", "totalReviews"])

        return {
            "created": created,
            "review": review,
            "averageRating": product.rating,
            "totalReviews": product.totalReviews,
        }
    