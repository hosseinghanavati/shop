from django.urls import path
from .views import *

app_name = 'Customer'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('panel/', MyPanelView.as_view(), name='panel'),
    path('logout/', logout_view, name='logout')
]