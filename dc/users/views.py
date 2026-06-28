from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *
from .utils import generate_salt, check_password, encode_token, store_token, check_password_match
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
from users.service import UserService
 


class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CreateUserSerializer,
        operation_description="Create user account",
        tags=["Users"]
    )
    @action(detail=False, methods=['post'])
    def register_user(self, request):
        try:
            request_data =  request.data.copy()
            phoneNumber = request_data.get('phoneNumber').lower()
            subOwnerId = request_data.get('subOwnerId')
            phoneNumber = str(phoneNumber).strip()

             # Validate phone number
            if not phoneNumber.isdigit():
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        'message': 'Phone number must contain only digits',
                        'code': ERROR_CODE_UNAUTHORIZED
                    }
                )

            if len(phoneNumber) != 10:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        'message': 'Phone number must be exactly 10 digits',
                        'code': ERROR_CODE_UNAUTHORIZED
                    }
                )

            
            if UserModel.objects.filter(phoneNumber=phoneNumber).exists():
                 return response_fun(RESPONSE_INVALID, {'message': "User already exists", 'code': ERROR_CODE_UNAUTHORIZED})
            
            print('subOwnerId ', subOwnerId)

            sub_owner = UserModel.objects.filter(
                id=subOwnerId,
                userType=UserModel.SUB_OWNER,
                is_active=True
            ).first()

            print('sub_owner ', sub_owner)

            if sub_owner is None:
                return response_fun(
                    RESPONSE_ERROR,
                    {
                        "message": "SubOwner not found.",
                        "code": ERROR_CODE_UNAUTHORIZED,
                    },
                )
            
            print('request_data ', request_data)
            random_salt = generate_salt()  # Generate salt
            request_data['password'] = make_password(request_data['password'], random_salt)
            request_data['salt'] = random_salt

            

            serializer = CreateUserSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                payload = {"phoneNumber": phoneNumber, "userId": serializer.data.get("id")}
                token = encode_token(payload)
                store_token(phoneNumber, token)

                response_data = {
                    'message': "User registered successful",
                    'token': token,
                    'data' : serializer.data 
                }
                
                return response_fun(RESPONSE_SUCCESS, response_data)
            
            return response_fun(RESPONSE_INVALID, {'message': serializer.errors, 'code': ERROR_CODE_UNAUTHORIZED})
        
        except Exception as e:
            print('SSSSSS ', e)
            return response_fun(RESPONSE_ERROR, {'message': str(e), 'code': ERROR_CODE_UNAUTHORIZED})
        

    
    
    @swagger_auto_schema(
        request_body=LogInSerializer,
        tags=["Users"]
    )        
    @action(detail=False, methods=['post'])
    def login_user(self, request):
        try:
            phoneNumber = request.data.get('phoneNumber').lower()
            print('SSSSSS ', phoneNumber)
            password = request.data.get('password')
            print('SSSSSS password ', password)
            user = UserModel.objects.filter(phoneNumber=phoneNumber).first()
           
            if not user:
                return response_fun(RESPONSE_INVALID, {'message': 'User does not exist', 'code': ERROR_CODE_UNAUTHORIZED})
            
            salt =  user.salt
            print('SSSSSS salt ', salt)
            
            hashed_password =  make_password(password, salt)
            print('SSSSSS hashed_password ',  hashed_password)
            print('SSSSSS user.password ', user.password)
            if not check_password(hashed_password, user.password):
                return response_fun(RESPONSE_INVALID, {'message': "Invalid credentials", 'code': ERROR_CODE_UNAUTHORIZED})
            
            payload =  {'phoneNumber': phoneNumber, "userId": user.id}
            token = encode_token(payload)
            store_token(phoneNumber, token)

            user_serializer =  CreateUserSerializer(user)

            response_data = {
                    'message': "Login successful",
                    'token': token,
                    'data': user_serializer.data
                }
            return response_fun(RESPONSE_SUCCESS, response_data)
    
        except Exception as e:
            print('SSSSSSSS Exception ', e)
            return response_fun(RESPONSE_ERROR, {'message': str(e), 'code': ERROR_CODE_UNAUTHORIZED})
    

    @swagger_auto_schema(
    tags=["Users"],
    request_body=ChangeSubscriptionSerializer,
    operation_description="Transfer customer subscription to another SubOwner",
    responses={200: ChangeSubscriptionSerializer},
    manual_parameters=[TOKEN],
    )
    @action(detail=False, methods=["post"])
    def change_subowner(self, request):
        try:
            user, error = authenticate_and_get_user(request)

            if error:
                return error

            if user.userType != UserModel.USER:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Only user can change subscription.",
                        "code": ERROR_CODE_BAD_REQUEST,
                    },
                )

            serializer = ChangeSubscriptionSerializer(data=request.data)

            if not serializer.is_valid():
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "errors": serializer.errors,
                        "code": ERROR_CODE_BAD_REQUEST,
                    },
                )
            
            print('111111')

            subscription = UserService.change_subowner(
                user=user,
                data=serializer.validated_data,
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Subscription transferred successfully.",
                    "data": {
                        "subscriptionId": subscription.id,
                        "subOwnerId": subscription.subOwner.id,
                        "subOwnerName": subscription.subOwner.name,
                        "productId": subscription.product.id,
                        "productName": subscription.product.name,
                        "startDate": subscription.start_date,
                        "endDate": subscription.end_date,
                        "status": subscription.status,
                    },
                },
            )

        except Exception as e:
            print(e)
            return response_fun(
                RESPONSE_ERROR,
                {
                    "message": str(e),
                    "code": ERROR_CODE_BAD_REQUEST,
                },
            )
        

    

    @swagger_auto_schema(
        tags=["Users"],
        request_body=UserAddressSerializer,
        manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["post"])
    def address_add(self, request):

        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            if user.userType != UserModel.USER:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Only User can add address.",
                        "code": ERROR_CODE_BAD_REQUEST
                    }
                )

            serializer = UserAddressSerializer(
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
        tags=["Users"],
        manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["get"])
    def address_list(self, request):

        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            addresses = UserAddress.objects.filter(
                user=user
            ).order_by("-isDefault", "-id")

            serializer = UserAddressSerializer(
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
        tags=["Users"],
        manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["get"])
    def address_default(self, request):

        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error
            
            if user.userType != UserModel.USER:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Only User can access this API.",
                        "code": ERROR_CODE_BAD_REQUEST,
                    },
                )


            addresses = UserAddress.objects.filter(
                user=user,
                isDefault = True
            ).first()

            serializer = UserAddressSerializer(addresses)

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
        tags=["Users"],
        request_body=UserAddressSerializer,
        manual_parameters=[TOKEN, ADDRESS_ID]
    )
    @action(detail=False, methods=["put"])
    def address_update(self, request):

        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            address_id = request.data.get("addressId")

            address = UserAddress.objects.filter(
                id=address_id,
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

            serializer = UserAddressSerializer(
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
        tags=["Users"],
        manual_parameters=[TOKEN, ADDRESS_ID]
    )
    @action(detail=False, methods=["delete"])
    def address_delete(self, request):

        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            address_id = request.query_params.get("addressId")

            address = UserAddress.objects.filter(
                id=address_id,
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

            address.delete()

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Address deleted successfully."
                }
            )
    
         
        except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
        
