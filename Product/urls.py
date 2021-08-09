from django.conf.urls.static import static
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from Shop_project import settings
from .views import *

app_name = 'Product'
urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('list_api/', ProductListApiView.as_view(), name='list_api'),
    path('detail_api/int:pk', ProductDetailApiView, name='detail_api')
]
urlpatterns = format_suffix_patterns(urlpatterns)
