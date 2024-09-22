import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from products.products_service import get_products, get_product
from products.comment_service import add_comment, reply_comment


def json_response(data, status=200, safe=True):
    content = json.dumps(data, ensure_ascii=safe)
    return HttpResponse(content, content_type='application/json', status=status)

def products(request):
    if request.method == 'GET':
        result = get_products(request.GET)
        return json_response(result, safe=False, status=200)


def product_detail(request, id):
    if request.method == 'GET':
        result = get_product(id)
        return json_response(result, safe=False, status=200)

#@csrf_exempt
def product_comments(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        data['user_id'] = request.user_id
        result, status = add_comment(id, data)
        return json_response(result, status=status)

#  @csrf_exempt
def product_reply_comments(request, id):
    # print (request.user_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        data['user_id'] = request.user_id
        result, status = reply_comment(id, data)
        return json_response(result, status=status)

