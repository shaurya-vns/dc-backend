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
 


class CustomerViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CustomerSerializer,
        tags=["Auth"]
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            request_data =  request.data.copy()
            phoneNumber = request_data.get('phoneNumber').lower()
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

            
            if CustomerModel.objects.filter(phoneNumber=phoneNumber).exists():
                 return response_fun(RESPONSE_INVALID, {'message': "User already exists", 'code': ERROR_CODE_UNAUTHORIZED})
            
            random_salt = generate_salt()  # Generate salt
            request_data['password'] = make_password(request_data['password'], random_salt)
            request_data['salt'] = random_salt
            
            serializer = CustomerSerializer(data=request_data)
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
        request_body=LogInSwaggerSerializer,
        tags=["Auth"]
    )        
    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            phoneNumber = request.data.get('phoneNumber').lower()
            print('SSSSSS ', phoneNumber)
            password = request.data.get('password')
            print('SSSSSS password ', password)
            user = CustomerModel.objects.filter(phoneNumber=phoneNumber).first()
           
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

            user_serializer =  CustomerSerializer(user)

            response_data = {
                    'message': "Login successful",
                    'token': token,
                    'data': user_serializer.data
                }
            return response_fun(RESPONSE_SUCCESS, response_data)
    
        except Exception as e:
            print('SSSSSSSS Exception ', e)
            return response_fun(RESPONSE_ERROR, {'message': str(e), 'code': ERROR_CODE_UNAUTHORIZED})
    