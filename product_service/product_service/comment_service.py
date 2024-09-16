from products.models import Comment, Product


def add_comment(product_id, data):
    try:
        product = Product.objects.get(item_id=product_id)
        print (product.item_id)
        print (product)
        comment = Comment(
            user_id=data["user_id"],
            product_id=product_id,
            content=data["content"],
            is_parent_comment=data.get("is_parent_comment", True),
            parent_comment_id=data.get("parent_comment_id")
        )
        comment.save()
        return comment_to_dict(comment), 201
    except Product.DoesNotExist:
        return {"error": "Product not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 400

def reply_comment(comment_id, data):
    try:
        parent_comment = Comment.objects.get(pk=comment_id)

        # Validate that there are no more than 5 levels of comments
        if parent_comment.is_parent_comment:
            depth_query = Comment.objects.filter(parent_comment_id=comment_id)
        else:
            depth_query = Comment.objects.all().none()

        depth = 1 if parent_comment.is_parent_comment else 2
        print (depth_query)

        while depth_query.exists():
            print (depth)
            if depth > 10:
                return {"error": "Cannot reply beyond 10 levels of comments"}, 400

            parent_comment_ids = depth_query.values_list('id', flat=True)
            depth_query = Comment.objects.filter(parent_comment_id__in=parent_comment_ids)
            depth += 1

        # Proceed with adding the comment if validation is passed
        comment = Comment(
            user_id=data["user_id"],
            product_id=parent_comment.product_id,
            content=data["content"],
            is_parent_comment=False,
            parent_comment_id=comment_id
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
