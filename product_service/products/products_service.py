from products.comment_service import comment_to_dict
from products.models import Product, Comment, ProductCategory


def get_products(params):
    try:
        print (params)
        products = Product.objects.all()

        page_size = int(params.get('page_size', 100))
        if page_size > 100:
            page_size = 100
        # TO DO : keyword doesnt work
        if params.get('keyword'):
            # print (params['keyword'])
            products = products.filter(title__icontains=params['keyword'])
        if params.get('category_id'):
            category_id = params['category_id']
            product_category_ids = ProductCategory.objects.filter(category_id=category_id).values_list('product_id',
                                                                                                       flat=True)
            product_category_ids_chunked = list(product_category_ids[:page_size + 1])  # Batch processing
            products = products.filter(item_id__in=product_category_ids_chunked)

        cursor = params.get('cursor')
        get_next = params.get('get_next', True)
        if cursor and get_next:
            # print (cursor)
            products = products.filter(item_id__gt=cursor)
        elif cursor:
            # print (cursor)
            products = products.filter(item_id__lt=cursor)

        products = products.order_by('item_id')[:page_size + 1]

        has_next = len(products) > page_size
        # item_ids = [p.item_id for p in products]
        # print (item_ids)
        if has_next:
            next_cursor = products[page_size].item_id
        else:
            next_cursor = None

        results = [product_to_dict(p) for p in products[:page_size]]
        # print (results)
        previous_cursor = products[0] if products else None
        return {
            'count': len(results),
            'next': next_cursor,
            'results': results,
            'previous': previous_cursor.item_id if previous_cursor else None,
        }
    except Exception as e:
        return {"error": str(e)}


def get_product(product_id):
    try:
        product = Product.objects.filter(item_id=product_id).first()
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

