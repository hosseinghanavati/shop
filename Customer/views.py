import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from Core.models import User
from Customer.forms import SignUpForm, AddressCreateForm, UserUpdateForm
from Customer.models import Customer, Address
from Customer.permissions import IsSuperUserOrReadOnly, IsOwnerOrStaff, IsSelf, IsStaff
from Customer.serializers import CustomerSerializer, UserSerializer, AddressSerializer, UserPreviewSerializer, \
    AddressPreviewSerializer
from Order.models import Order


class MyLoginView(LoginView):
    pass


class MyPanelView(PermissionRequiredMixin, generic.TemplateView):
    template_name = 'Panel/Dashboard.html'
    permission_required = 'Core.see_panel'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(phone=user.phone, password=raw_password)
            content_type = ContentType.objects.get_for_model(User)
            Customer.objects.create(user_id=user.id)
            permission = Permission.objects.get(
                codename='see_panel',
                content_type=content_type,
            )
            user.user_permissions.add(permission)
            user = get_object_or_404(User, pk=user.id)
            login(request, user)
            return redirect('Customer:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'Customer/SignUp.html', {'form': form})


class MyLogOutView(LogoutView):
    pass


class DashBoardView(LoginRequiredMixin, generic.ListView):
    template_name = 'Panel/Dashboard.html'

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return user

    def get_context_data(self, *, object_list=None, **kwargs):
        orders = Order.objects.filter(customer__user=self.request.user).order_by('-create_time_stamp')[:5]
        context = {
            'orders': orders
        }
        return super().get_context_data(**context)


class OrderPanelView(LoginRequiredMixin, generic.ListView):
    template_name = 'Panel/order_panel_view.html'

    def get_queryset(self):
        orders = Order.objects.filter(customer__user_id=self.request.user.id).order_by('-create_time_stamp')
        return orders

    context_object_name = 'orders'


class AddressPanelView(LoginRequiredMixin, generic.ListView, generic.FormView):
    template_name = 'Panel/addresses_panel_view.html'
    form_class = AddressCreateForm
    success_url = reverse_lazy('Customer:addresses')

    def form_valid(self, form):
        customer = Customer.objects.get(user=self.request.user)
        form.instance.owner = customer
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        self.addresses = Address.objects.filter(owner_id=customer.id)
        return self.addresses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = self.addresses
        return context


class AddressPanelDelete(LoginRequiredMixin, generic.DeleteView):
    model = Address
    success_url = reverse_lazy('Customer:addresses')

    def delete(self, request, *args, **kwargs):
        self.address = get_object_or_404(Address, id=kwargs['pk'])
        self.address.deleted = True
        self.address.delete_time_stamp = datetime.datetime.now()
        self.address.save()
        success_url = reverse_lazy('Customer:addresses')
        return HttpResponseRedirect(success_url)


class AddressUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Address
    fields = [
        "country",
        "province",
        "city",
        "exact_address",
        "house_number",
        "zip_code"
    ]
    template_name = 'Panel/address_update.html'
    success_url = reverse_lazy('Customer:addresses')


class AddressCreateView(LoginRequiredMixin, generic.FormView):
    form_class = AddressCreateForm
    template_name = 'Panel/addresses_panel_view.html'
    success_url = reverse_lazy('Customer:addresses')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'Panel/user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('Customer:panel')


# API
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelf]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            user = User.objects.filter(id=self.request.user.id)
            return Customer.objects.filter(user=user)


class BaseUserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


class UserPreViewSet(BaseUserViewSet):
    serializer_class = UserPreviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelf]


class UserViewSet(BaseUserViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelf]


class BaseAddressViewSet(ModelViewSet):
    queryset = Address.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Address.objects.all()
        else:
            customer = Customer.objects.get(user=self.request.user)
            return Address.objects.filter(owner=customer)


class AddressPreViewSet(BaseAddressViewSet):
    serializer_class = AddressPreviewSerializer
    permission_classes = [IsOwnerOrStaff, permissions.IsAuthenticated]


class AddressViewSet(BaseAddressViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrStaff, permissions.IsAuthenticated]

