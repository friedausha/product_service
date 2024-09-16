from django.db import models

class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    display_name = models.CharField(max_length=200)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.BigIntegerField()
    shop_id = models.CharField(max_length=36)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    attributes = models.TextField(blank=True, null=True)
    product_images = models.TextField(blank=True, null=True)
    product_categories = models.TextField(blank=True, null=True)

class ProductCategory(models.Model):
    product = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

class Comment(models.Model):
    user_id = models.CharField(max_length=36)
    product_id = models.CharField(max_length=255)
    content = models.TextField()
    is_parent_comment = models.BooleanField(default=True)
    parent_comment_id = models.CharField(max_length=255, blank=True, null=True)
