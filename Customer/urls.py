from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

from .views import *

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'users', UserViewSet,)
router.register(r'preview-users', UserPreViewSet, basename='preu')
router.register(r'addresses', AddressViewSet)
router.register(r'preview-addresses', AddressPreViewSet, basename='prea')


app_name = 'Customer'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('panel/', MyPanelView.as_view(), name='panel'),
    path('logout/', MyLogOutView.as_view(), name='logout'),
    path('api/', include(router.urls), name='api'),
    path('panel/dashboard/', DashBoardView.as_view(), name='dashboard'),
    path('panel/orders-history/', OrderPanelView.as_view(), name='orders-history'),
    path('panel/addresses/', AddressPanelView.as_view(), name='addresses'),
    path('panel/delete-address/<int:pk>/', AddressPanelDelete.as_view(), name='delete-address'),
    path('panel/<pk>/address-update/', AddressUpdateView.as_view(), name='update-address'),
    path('panel/<pk>/user-update', UserUpdateView.as_view(), name='user-update'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_reset/password_change.html', success_url=reverse_lazy('Customer:password_change_done')),
         name='password_change'),
]
