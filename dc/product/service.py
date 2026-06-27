from users.models import UserModel
from .models import ProductModel


class ProductService:

    @staticmethod
    def create_product(validated_data):

        sub_owner_id = validated_data.pop("subOwnerId")

        sub_owner = UserModel.objects.filter(
            id=sub_owner_id,
            userType=UserModel.SUB_OWNER,
            is_active=True,
        ).first()

        if sub_owner is None:
            raise ValueError("SubOwner not found.")

        return ProductModel.objects.create(
            subOwner=sub_owner,
            **validated_data,
        )