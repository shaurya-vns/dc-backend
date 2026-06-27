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
from subscription.models import SubscriptionModel
from subscription.serializers import SubscriptionListSerializer
from users.serializers import SubOwnerListSerializer
 


class OwnerViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CreateSubOwnerSerializer,
        operation_description="Create sub owner",
        tags=["SubOwner"]
    )
    @action(detail=False, methods=['post'])
    def register_sub_owner(self, request):
        try:
            request_data =  request.data.copy()
            phoneNumber = request_data.get('phoneNumber').lower()
            phoneNumber = str(phoneNumber).strip()

            print('request_data ', request_data)


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
            
            random_salt = generate_salt()  # Generate salt
            request_data['password'] = make_password(request_data['password'], random_salt)
            request_data['salt'] = random_salt

            print('request_data 22 ')

            request_data['userType'] = UserModel.SUB_OWNER

            print('request_data 11 ')
            
            serializer = CreateSubOwnerSerializer(data=request_data)
            if serializer.is_valid():
                print('request_data 33 ')
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
        request_body=LoginSubOwnerSerializer,
        tags=["SubOwner"]
    )        
    @action(detail=False, methods=['post'])
    def login_sub_owner(self, request):
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

            user_serializer =  CreateSubOwnerSerializer(user)

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
        tags=["SubOwner"],
            operation_description="List of all subscription by subowner",
            manual_parameters=[TOKEN]
        )
    @action(detail=False, methods=['get'])
    def subscription_list(self, request):
            try:

                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
               
                if error:
                    return error
                
                print('userType ', user.userType)
                
                if user.userType != UserModel.SUB_OWNER:
                     return response_fun(RESPONSE_INVALID, {'message': 'Permission denia','code': ERROR_CODE_NOT_FOUND}) 

                    
                subscription = SubscriptionModel.objects.filter(
                    subOwner = user,
                 
                ).order_by("-created_at")

                
                print('request subscription ', subscription)

                serializer = SubscriptionListSerializer(subscription,   many=True)

                return response_fun(RESPONSE_SUCCESS,
                                    {
                                          'message':"Get all subscription list by subowner.",
                                          'data': serializer.data
                                    })
            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 



    @swagger_auto_schema(
        tags=["SubOwner"],
            operation_description="List of all customer by subowner",
            manual_parameters=[TOKEN]
        )
    @action(detail=False, methods=['get'])
    def customer_list(self, request):
            try:

                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
               
                if error:
                    return error
                
                print('userType ', user.userType)
                
                if user.userType != UserModel.SUB_OWNER:
                     return response_fun(RESPONSE_INVALID, {'message': 'Permission denia','code': ERROR_CODE_NOT_FOUND}) 

                    
                users = UserModel.objects.filter(
                    parent = user,
                 
                ).order_by("-created_at")

                
                print('request users ', users)

                serializer = SubOwnerListSerializer(users,   many=True)

                return response_fun(RESPONSE_SUCCESS,
                                    {
                                          'message':"List of all customer by subowner",
                                          'data': serializer.data
                                    })
            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 




    