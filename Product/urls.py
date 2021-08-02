from django.conf.urls.static import static
from django.urls import path

from Shop_project import settings
from .views import *

app_name = 'Product'
urlpatterns = [
    path('', ProductView.as_view(), name='products')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
