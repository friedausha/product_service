from product_service.comment_service import comment_to_dict
from products.models import Product, Comment

def get_products(params):
    products = Product.objects.all()
    if params.get('keyword'):
        products = products.filter(title__icontains=params['keyword'])
    if params.get('category_id'):
        products = products.filter(product_categories__icontains=params['category_id'])

    page_size = int(params.get('page_size', 100))
    cursor = params.get('cursor')
    if cursor:
        products = products.filter(item_id__gt=cursor)

    products = products.order_by('item_id')[:page_size + 1]
    has_next = len(products) > page_size

    if has_next:
        next_cursor = products[page_size].item_id
    else:
        next_cursor = None

    results = [product_to_dict(p) for p in products[:page_size]]
    return {
        'count': len(results),
        'next': next_cursor,
        'results': results
    }


def get_product(product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return product_to_dict_with_comments(product)
    except Product.DoesNotExist:
        return {"error": "Product not found"}


def product_to_dict(product):
    return {
        "id": product.item_id,
        "shop_id": product.shop_id,
        "title": product.title,
        "description": product.description,
        "image": product.image,
        "attributes": product.attributes,
        "stock": product.stock,
        "price": float(product.price),
        "categories": product.product_categories,
        # "comments": [comment_to_dict(c) for c in product.comments.all()]
    }
def product_to_dict_with_comments(product):
    comments = Comment.objects.filter(product_id=product.item_id)
    comments_dict = [comment_to_dict(c) for c in comments]
    return {
        "id": product.item_id,
        "shop_id": product.shop_id,
        "title": product.title,
        "description": product.description,
        "image": product.image,
        "attributes": product.attributes,
        "stock": product.stock,
        "price": float(product.price),
        "categories": product.product_categories,
        "comments": comments_dict
    }

