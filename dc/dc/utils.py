
from .constant import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import jwt
from .settings import SECRET_KEY,REDIS
from .errors import ERROR_CODE_INVALID_TOKEN
from .constant import INVALID_TOKEN
from customer.models import CustomerModel
from dc.errors import *

def response_fun(*args):
    status = args[0]
    if status == RESPONSE_SUCCESS:
        return Response({'statusCode': status, 'responseData': args[1]}, status=HTTP_200_OK)
    elif status == RESPONSE_INVALID:
        return Response({'statusCode': 0, 'error': args[1]}, status=HTTP_200_OK)
    else:
        return Response({'statusCode': status, 'error': {'message': args[1]}}, status=HTTP_400_BAD_REQUEST)
    
def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.DecodeError:
        return False
    
def authenticate_token(token):
    try:
        decoded_token = decode_token(token)
        if not decoded_token:
            return False
        email = decoded_token.get('phoneNumber')
        if token in REDIS.lrange(email, 0, -1):
            return decoded_token
        return False
    except Exception:
        return False
    
def authenticate_request(request):
    token = request.headers.get('token')
    print('request token ', token)
    authenticated = authenticate_token(token)
    if not authenticated:
        return False, response_fun(RESPONSE_INVALID, {'errors': INVALID_TOKEN, 'code': ERROR_CODE_INVALID_TOKEN})
    return True, authenticated


def get_user_or_error(user_id):
    """
    Return User instance if exists, else None.
    """
    return CustomerModel.objects.filter(id=user_id).first()


def authenticate_and_get_user(request):
    """
    Authenticate request (via token header), fetch user by userId in token response.
    Returns:
      - user instance if OK
      - (None, error_response) if auth fails or user not found
    """
    authenticated, resp = authenticate_request(request)
    if not authenticated:
        return None, resp

    user_id = resp.get('userId')
    user = CustomerModel.objects.filter(id=user_id).first()
    if user is None:
        return None, response_fun(
            RESPONSE_INVALID,
            { 'message': 'User not found!!', 'code': ERROR_CODE_NOT_FOUND }
        )
    return user, None
 