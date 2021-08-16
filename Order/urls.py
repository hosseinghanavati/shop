from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'customers', OrderViewSet)


app_name = 'Order'
urlpatterns = [
    path('api/', include(router.urls), name='api')
]

