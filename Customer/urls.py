from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'users', UserViewSet)
router.register(r'addresses', AddressViewSet)
# router.register(r'own-addresses', OwnerAddressViewSet)

app_name = 'Customer'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('panel/', MyPanelView.as_view(), name='panel'),
    path('logout/', MyLogOutView.as_view(), name='logout'),
    path('api/', include(router.urls), name='api')
]