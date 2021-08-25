from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, generics, status, permissions
from rest_framework.viewsets import ModelViewSet

from Cart.forms import CartAddForm
from .permissions import IsStaffOrReadOnly
from .serializers import *
from .models import *
from django.core.paginator import Paginator



class HomeView(generic.ListView):
    template_name = 'product/home.html'
    queryset = Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        categories = Category.objects.filter(is_sub=False)
        products = Product.objects.all().order_by('-create_time_stamp')[:8]

        context = {
            'categories': categories,
            'products': products,
        }
        return context


class ProductView(View):
    def get(self, request, slug=None):
        products = Product.objects.all()
        categories = Category.objects.filter(is_sub=False)
        paginator = Paginator(products, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if slug:
            category = Category.objects.get(slug=slug)
            products = products.filter(category=category)
        return render(request, 'product/product_view.html', {'products': products, 'categories': categories, 'page_obj': page_obj})


class ProductDetailView(generic.DetailView, generic.FormView):
    model = Product
    template_name = 'product/product_detail.html'
    form_class = CartAddForm

    def get_queryset(self):
        product = Product.objects.filter(slug=self.kwargs['slug'])
        return product


# API

# @api_view(['GET', 'POST'])
# def product_list_api(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         products_serializer = ProductSerializer(products, many=True)
#         return Response({
#             "products": products_serializer.data
#         })
#     elif request.method == 'POST':
#         products_serializer = ProductSerializer(data=request.POST)
#         if products_serializer.is_valid():
#             products_serializer.save()
#             return Response(products_serializer.data)
#         else:
#             return Response(products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductListApiView(generics.ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#
#
# class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsStaffOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


class DiscountViewSet(ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsStaffOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsStaffOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


