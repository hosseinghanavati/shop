from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, generics, status
from .serializers import *
from .models import *


class ProductView(generic.ListView):
    template_name = 'product/product_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['products'] = Product.objects.all()
        return context
    queryset = get_context_data


@api_view(['GET', 'POST'])
def product_list_api(request):
    if request.method == 'GET':
        products = Product.objects.all()
        products_serializer = ProductSerializer(products, many=True)
        return Response({
            "products": products_serializer.data
        })
    elif request.method == 'POST':
        products_serializer = ProductSerializer(data=request.POST)
        if products_serializer.is_valid():
            products_serializer.save()
            return Response(products_serializer.data)
        else:
            return Response(products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailApiView():
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    # lookup_url_kwarg = 'name'
    # lookup_field = 'name'

