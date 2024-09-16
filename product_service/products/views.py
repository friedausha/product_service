import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from product_service.products_service import get_products, get_product
from product_service.comment_service import add_comment, reply_comment
from product_service.user_service import register_user, login_user


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
        result, status = login_user(data)
        return json_response(result, status=status)


def products(request):
    if request.method == 'GET':
        result = get_products(request.GET)
        return json_response(result, safe=False, status=200)


def product_detail(request, id):
    if request.method == 'GET':
        result = get_product(id)
        return json_response(result, safe=False, status=200)


@csrf_exempt
def product_comments(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        result, status = add_comment(id, data)
        return json_response(result, status=status)

#TO DO: validation n comments level
@csrf_exempt
def product_reply_comments(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        result, status = reply_comment(id, data)
        return json_response(result, status=status)

