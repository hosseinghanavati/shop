from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View, generic
from .models import *


class ProductView(generic.ListView):
    template_name = 'product/product_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['products'] = Brand.objects.all()
        return context
    queryset = get_context_data


