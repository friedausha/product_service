from django.conf.urls import url

from product_service import settings
from products import views as product_views
from users import views as user_views

from django.conf.urls import include
urlpatterns = [
    url(r'^api/users/register/$', user_views.register, name='register'),
    url(r'^api/users/login/$', user_views.login, name='login'),
    url(r'^api/products/$', product_views.products, name='products'),
    url(r'^api/products/(?P<id>\d+)/$', product_views.product_detail, name='product_detail'),
    url(r'^api/products/(?P<id>\d+)/comments/$', product_views.product_comments, name='product_comments'),
    url(r'^api/comments/(?P<id>\d+)/$', product_views.product_reply_comments, name='reply_comment'),
    url(r'^api/verify/$', user_views.verify_token, name='verify'),]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns