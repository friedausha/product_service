import json

from users.user_serializer import UserSerializer
from utils.tcp_client import send_tcp_command


# REGISTER_URL = USER_SERVICE  + 'api/register'
# LOGIN_URL = USER_SERVICE + 'api/token'

def register_user(data):
    json_data = json.dumps(data, ensure_ascii=False)
    response = send_tcp_command("REGISTER", json_data)
    if 'id' in response:
        data['id'] = response['id']
        user = UserSerializer.from_dict(data)
        return UserSerializer.to_dict(user), 201
    else:
        return {"error": response['error']}, 400


def login_user(data):
    json_data = json.dumps(data, ensure_ascii=False)
    response = send_tcp_command("LOGIN", json_data)
    if 'token' in response and response.get('token') != '':
        return response, 200
    else:
        return {"error": response}, 500

def verify_token(token):
    response = send_tcp_command("VERIFY_TOKEN", token)
    if 'valid' in response and response['valid'] == True:
        return response, 200
    else:
        return response, 401
