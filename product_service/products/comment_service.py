from dns.e164 import query

from products.models import Comment, Product

def add_comment(product_id, data):
    try:
        product = Product.objects.get(item_id=product_id)
        if product.item_id is None:
            return {"error": "Product not found"}, 404
        comment = Comment(
            user_id=data["user_id"],
            product_id=product_id,
            content=data["content"],
            is_parent_comment=data.get("is_parent_comment", True),
            parent_comment_id=None
        )
        comment.save()
        return comment_to_dict(comment), 201
    except Product.DoesNotExist:
        return {"error": "Product not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 400

def reply_comment(comment_id, data):
    try:
        initial_parent_comment = Comment.objects.get(pk=comment_id)
        max_depth = 5
        depth = 1
        parent_comment = initial_parent_comment
        while parent_comment.parent_comment_id is not None:
            parent_comment = Comment.objects.get(pk=parent_comment.parent_comment_id)
            depth += 1
            # print (depth)
            if depth > max_depth:
                return {"error": "Comment reply to comment, depth exceeded"}, 400
        # Proceed with adding the comment if validation is passed
        comment = Comment(
            user_id=data["user_id"],
            product_id=parent_comment.product_id,
            content=data["content"],
            is_parent_comment=False,
            parent_comment_id=initial_parent_comment.id
        )
        comment.save()
        return comment_to_dict(comment), 201
    except Comment.DoesNotExist:
        return {"error": "Comment not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


def comment_to_dict(comment):
    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "product_id": comment.product_id,
        "content": comment.content,
        "is_parent_comment": comment.is_parent_comment,
        "parent_comment_id": comment.parent_comment_id,
    }
