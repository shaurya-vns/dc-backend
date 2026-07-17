from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from users.utils import generate_salt, check_password, encode_token, store_token
from dc.utils import response_fun
from dc.constant import RESPONSE_INVALID, RESPONSE_SUCCESS, RESPONSE_ERROR
from dc.errors import ERROR_CODE_UNAUTHORIZED, ERROR_CODE_NOT_FOUND
from django.core.validators import validate_email
from django.contrib.auth.hashers        import make_password
from dc.parameters import TOKEN
from dc.errors import *
from dc.parameters import * 
from dc.utils import authenticate_and_get_user
from users.serializers import CreateUserSerializer, LogInSerializer
from users.models import UserModel
from users.serializers import UserBasicInfoSerializer

 

class DeliveryViewSet(viewsets.ViewSet):
            @swagger_auto_schema(
                request_body=CreateUserSerializer,
                operation_description="Create delivery account",
                tags=["Delivery"],
                manual_parameters=[TOKEN]
            )
            @action(detail=False, methods=['post'])
            def register_delivery(self, request):
                try:

                    user, error = authenticate_and_get_user(request)
                    if error:
                            return error
                    
                    if user.userType != UserModel.VENDOR:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Only vendor allowed",
                                "code": ERROR_CODE_BAD_REQUEST
                            }
                        )

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

        
                    print('request_data 11 ')
                    
                    serializer = CreateUserSerializer(data=request_data)
                    if serializer.is_valid():
                            print('request_data 33 ')
                        
                            serializer.save(
                                parent=user,
                                userType=UserModel.DELIVERY,
                            )
                            payload = {"phoneNumber": phoneNumber, "userId": serializer.data.get("id")}
                            token = encode_token(payload)
                            store_token(phoneNumber, token)

                            response_data = {
                                'message': "Delivery partner registered successful",
                                'token': token,
                                'data' : serializer.data 
                            }
                            
                            return response_fun(RESPONSE_SUCCESS, response_data)
                    
                    return response_fun(RESPONSE_INVALID, {'message': serializer.errors, 'code': ERROR_CODE_UNAUTHORIZED})
                
                except Exception as e:
                    print('SSSSSS ', e)
                    return response_fun(RESPONSE_ERROR, {'message': str(e), 'code': ERROR_CODE_UNAUTHORIZED})
                
            @swagger_auto_schema(
                tags=["Delivery"],
                manual_parameters=[TOKEN]
            )
            @action(detail=False, methods=["get"])
            def list_partner(self, request):

                try:
                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                 
                    delivery = UserModel.objects.filter(
                        userType  = UserModel.DELIVERY,
                        parent = user

                    ).order_by("-id")

                    serializer = UserBasicInfoSerializer(delivery, many=True  )

                    return response_fun(
                        RESPONSE_SUCCESS,
                        {
                            "data": serializer.data
                        }
                    )
                
                except Exception as e:
                        return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 

            
