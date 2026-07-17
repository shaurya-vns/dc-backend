from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from users.utils import generate_salt, check_password, encode_token, store_token
from dc.utils import response_fun
from dc.constant import RESPONSE_INVALID, RESPONSE_SUCCESS, RESPONSE_ERROR
from dc.errors import ERROR_CODE_UNAUTHORIZED, ERROR_CODE_NOT_FOUND
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers        import make_password
from dc.parameters import TOKEN
from dc.utils import authenticate_and_get_user
from dc.errors import *
from dc.parameters import *
from address.serializers import AddAddressSerializer
from address.models import AddressModel
from onetimeorder.models import OneTimeOrderModel
from ondemand.models import OnDemandModel
 

class AddressViewSet(viewsets.ViewSet):
             

            @swagger_auto_schema(
                tags=["Address"],
                request_body=AddAddressSerializer,
                manual_parameters=[TOKEN]
            )
            @action(detail=False, methods=["post"])
            def address_add(self, request):

                try:

                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error

                    serializer = AddAddressSerializer(
                        data=request.data,
                        context={"user": user}
                    )

                    if serializer.is_valid():
                        serializer.save()

                        return response_fun(
                            RESPONSE_SUCCESS,
                            {
                                "message": "Address added successfully.",
                                "data": serializer.data
                            }
                        )

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "errors": serializer.errors,
                            "code": ERROR_CODE_BAD_REQUEST
                        }
                    )
            
                except Exception as e:
                        print('error ', e)
                        return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 


            @swagger_auto_schema(
                tags=["Address"],
                manual_parameters=[TOKEN, USER_ID]
            )
            @action(detail=False, methods=["get"])
            def address_default(self, request):

                try:

                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                    
                    if user.userType != UserModel.SUB_OWNER:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Only User can access this API.",
                                "code": ERROR_CODE_BAD_REQUEST,
                            },
                        )


                    addresses = AddressModel.objects.filter(
                        user=user,
                        isDefault = True
                    ).first()

                    serializer = GetAddressSerializer(addresses)

                    return response_fun(
                        RESPONSE_SUCCESS,
                        {
                            "data": serializer.data
                        }
                    )
                
                except Exception as e:
                        print('eeeeee', e)
                        return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 


            @swagger_auto_schema(
                tags=["Address"],
                manual_parameters=[TOKEN, USER_ID]
            )
            @action(detail=False, methods=["get"])
            def address_list(self, request):

                try:
                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                    
                    user_id = request.query_params.get("userId")
                    if not user_id:
                        return response_fun(
                            RESPONSE_INVALID,
                            {"message": "user_id is required"},
                        )

                    addresses = AddressModel.objects.filter(
                        user_id=user_id
                    ).order_by("-isDefault", "-id")

                    serializer = GetAddressSerializer(
                        addresses,
                        many=True
                    )

                    return response_fun(
                        RESPONSE_SUCCESS,
                        {
                            "data": serializer.data
                        }
                    )
                
                except Exception as e:
                        return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 

            

            @swagger_auto_schema(
                tags=["Address"],
                request_body=AddAddressSerializer,
                manual_parameters=[TOKEN, ADDRESS_ID]
            )
            @action(detail=True, methods=["put"])
            def address_update(self, request, pk=None):

                try:

                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                    
                    addressId = request.query_params.get("addressId")

                    address = AddressModel.objects.filter(
                        id=addressId,
                        user=user
                    ).first()

                    if address is None:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Address not found.",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )

                    serializer = GetAddressSerializer(
                        address,
                        data=request.data,
                        partial=True
                    )

                    if serializer.is_valid():
                        serializer.save()

                        return response_fun(
                            RESPONSE_SUCCESS,
                            {
                                "message": "Address updated successfully.",
                                "data": serializer.data
                            }
                        )

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "errors": serializer.errors,
                            "code": ERROR_CODE_BAD_REQUEST
                        }
                    )
                
                except Exception as e:
                        return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                


            @swagger_auto_schema(
                tags=["Address"],
                manual_parameters=[TOKEN, ADDRESS_ID]
            )
            @action(detail=True, methods=["delete"])
            def address_delete(self, request,):

                try:

                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                    
                    addressId = request.query_params.get("addressId")

                    address = AddressModel.objects.filter(
                        id=addressId,
                        user=user
                    ).first()

                    if address is None:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Address not found.",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )
                    
                    if OneTimeOrderModel.objects.filter(address=address).exists():
                       return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "This address is associated with existing orders and cannot be deleted."
                            },
                        )
                    
                    if OnDemandModel.objects.filter(address=address).exists():
                       return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "This address is associated with existing orders and cannot be deleted."
                            },
                        )

                    address.delete()

                    return response_fun(
                        RESPONSE_SUCCESS,
                        {
                            "message": "Address deleted successfully."
                        }
                    )
            
                
                except Exception as e:
                        print('eee ', e)
                        return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

            