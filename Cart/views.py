from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from Product.models import Product
from .forms import CartAddForm


# Create your views here.


def detail(request):
    cart = Cart(request)
    form = CartAddForm(request.POST)
    return render(request, 'Cart/cart_detail.html', {'cart': cart, 'form': form})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'])
    return redirect('Cart:detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('Cart:detail')


def cart_quantity_update(request, product_id):
    cart = Cart(request)
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.update(product=product, quantity=cd['quantity'])
    return redirect('Cart:detail')
