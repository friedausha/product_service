from django.conf.urls import url
from products import views

urlpatterns = [
    url(r'^api/users/register/$', views.register, name='register'),
    url(r'^api/users/login/$', views.login, name='login'),
    url(r'^api/products/$', views.products, name='products'),
    url(r'^api/products/(?P<id>\d+)/$', views.product_detail, name='product_detail'),
    url(r'^api/products/(?P<id>\d+)/comments/$', views.product_comments, name='product_comments'),
    url(r'^api/comments/(?P<id>\d+)/$', views.product_reply_comments, name='reply_comment')
]
