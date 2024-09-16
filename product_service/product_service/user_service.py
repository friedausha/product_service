import requests

from product_service.settings import USER_SERVICE
from serializers.user_serializer import UserSerializer

REGISTER_URL = USER_SERVICE  + 'api/register'
LOGIN_URL = USER_SERVICE + 'api/token'


def register_user(data):
    response = requests.post(REGISTER_URL, json=data)
    print (response.json())
    if response.status_code == 201:
        user_data = response.json()
        print (user_data)
        data['id'] = user_data['id']
        user = UserSerializer.from_dict(data)
        print (user)
        return UserSerializer.to_dict(user), 201
    else:
        return {"error": "Registration failed"}, response.status_code


def login_user(data):
    response = requests.post(LOGIN_URL, json=data)
    print (response.json())
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {"error": "Invalid credentials"}, 401
