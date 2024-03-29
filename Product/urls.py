from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from Shop_project import settings
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'Discounts', DiscountViewSet)
router.register(r'Brands', BrandViewSet)


app_name = 'Product'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('caregory', ProductView.as_view(), name='category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-details'),
    path('category/<slug:slug>/', ProductView.as_view(), name='category_filter'),
    # path('list_api/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='list_api'),
    # path('detail_api/<int:pk>/', ProductViewSet.as_view({
    #     'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='detail_api')
    path('api/', include(router.urls)),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
