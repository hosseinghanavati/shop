from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from rest_framework.viewsets import ModelViewSet

from Cart.cart import Cart
from Customer.models import Customer, Address
from Order.forms import AddressShowOrder
from Order.models import Order, OrderItem
from Order.permissions import IsStaffOrOwner
from Order.serializers import OrderSerializer, OrderItemSerializer, OrderPreviewSerializer, OrderItemPreviewSerializer


class OrderDetail(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'Order/order_detail.html'

    def get_context_data(self, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        order_items = OrderItem.objects.filter(order_id=self.kwargs['pk'])
        context = {
            'items': order_items,
            'order': order
        }
        return context


@login_required()
def create_order(request):
    cart = Cart(request)
    form = AddressShowOrder(request.POST, request.FILES)
    if form.is_valid():
        address = form.cleaned_data['address']
        customer = Customer.objects.get(user=request.user)
        address = Address.objects.get(id=address.id)
        order = Order.objects.create(customer=customer, address=address)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])
        order.total_price = cart.get_total_price()
        order.final_price = cart.get_final_price()
        order.save()
        cart.clear()
        return redirect('Order:pay-view', order.id)


@login_required()
def order_preview(request):
    cart = Cart(request)
    addresses = Address.objects.filter(owner__user_id=request.user.id)
    form = AddressShowOrder()
    form.fields['address'].queryset = Address.objects.filter(owner__user_id=request.user.id)
    return render(request, 'Order/order_preview.html', {'cart': cart, "form": form, 'addresses': addresses})


@login_required()
def pay_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'Order/order_pay.html', {'order': order})


@login_required()
def order_pay(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'paid'
    order.save()
    return redirect('Customer:dashboard')


@login_required()
def order_cancel(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'canceled'
    order.save()
    return redirect('Customer:dashboard')

# class CreateOrder(LoginRequiredMixin, generic.CreateView):
#     cart = ...
#     order = ...
#
#     def get(self, request, *args, **kwargs):
#         self.cart = Cart(request)
#         customer = Customer.objects.get(user=self.request.user)
#         self.order = Order.objects.create(customer=customer)
#         return super().get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         for item in self.cart:
#             OrderItem.objects.create(order=self.order, )
#         return super().post(request, *args, **kwargs)


# API
class BaseOrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            customer = Customer.objects.get(user=self.request.user)
            return Order.objects.filter(customer=customer)


class OrderPreViewSet(BaseOrderViewSet):

    serializer_class = OrderPreviewSerializer
    permission_classes = IsStaffOrOwner


class OrderViewSet(BaseOrderViewSet):
    serializer_class = OrderSerializer
    permission_classes = IsStaffOrOwner


class BaseOrderItemViewSet(ModelViewSet):
    # queryset = OrderItem.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()
        else:
            customer = Customer.objects.get(user=self.request.user)
            order = Order.objects.filter(customer=customer)
            return OrderItem.objects.filter(order=order)


class OrderItemPreViewSet(BaseOrderItemViewSet):

    serializer_class = OrderItemPreviewSerializer
    permission_classes = IsStaffOrOwner


class OrderItemViewSet(BaseOrderItemViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = IsStaffOrOwner


