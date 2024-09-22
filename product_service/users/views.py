import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from users import user_service
from users.user_service import register_user, login_user
from utils.cache import Cache, cache


def json_response(data, status=200, safe=True):
    content = json.dumps(data, ensure_ascii=safe)
    return HttpResponse(content, content_type='application/json', status=status)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result, status = register_user(data)
        return json_response(result, status=status)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # # key = data.get('username') + "_" + data.get('password')
        # # cache_resp = cache.get_key(key)
        # if cache_resp is not None:
        #     # print ("cache hit")
        #     # return json_response(cache_resp.get('result'), status=cache_resp.get('status'))
        #     return cache_resp
        # else:
        result, status = login_user(data)
        # resp = json_response(result, status=status)
        # cache.set(key, resp , ttl=600)
        # return resp
        # print (result)
        return json_response(result, status=status)
        # return json_response(data, status=200)

@csrf_exempt
def verify_token(request):
    auth_token = request.META.get('HTTP_AUTHORIZATION', None)
    if request.method == 'POST':
        if cache.get_key(auth_token) is not None:
            return json_response({'valid': True}, status=200)
        else :
            result, status = user_service.verify_token(auth_token)
            cache.set(auth_token, result, ttl=30)
            return json_response(result, status=status)

