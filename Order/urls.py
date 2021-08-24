from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')


app_name = 'Order'
urlpatterns = [
    path('api/', include(router.urls), name='api'),
    path('preview/', order_preview, name='preview'),
    path('create/', create_order, name='create-order'),
    path('<int:order_id>/', OrderDetail.as_view(), name='detail'),
    path('pay/view/<int:order_id>/', pay_view, name='pay-view'),
    path('pay/<int:order_id>/', order_pay, name='pay'),
]

