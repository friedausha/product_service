# from rest_framework import serializers
# from products.models import Product, Category
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'display_name']
#
# class ProductSerializer(serializers.ModelSerializer):
#     product_categories = CategorySerializer(many=True)
#     list_of_comments = serializers.ListField()
#
#     class Meta:
#         model = Product
#         fields = ['item_id', 'shop_id', 'title', 'description', 'image', 'attributes', 'stock', 'price',
#                   'product_categories', 'product_images', 'list_of_comments']
