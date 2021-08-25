from django.urls import path
from .views import *

app_name = 'Cart'
urlpatterns = [
    path('', detail, name='detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', cart_quantity_update, name='quantity_update'),
]
