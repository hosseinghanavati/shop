
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import generic
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from Core.models import User
from Customer.forms import SignUpForm
from Customer.models import Customer, Address
from Customer.permissions import IsSuperUserOrReadOnly, IsOwnerOrStaff, IsSelf, IsStaff
from Customer.serializers import CustomerSerializer, UserSerializer, AddressSerializer


class MyLoginView(LoginView):
    pass


class MyPanelView(PermissionRequiredMixin, generic.TemplateView):
    template_name = 'Customer/panel.html'
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
            return redirect('Customer:panel')
    else:
        form = SignUpForm()
    return render(request, 'Customer/SignUp.html', {'form': form})


class MyLogOutView(LogoutView):
    pass


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsSelf, permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            user = User.objects.filter(id=self.request.user.id)
            return Customer.objects.filter(user=user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelf, permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrStaff, permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Address.objects.all()
        else:
            customer = Customer.objects.get(user=self.request.user)
            return Address.objects.filter(owner=customer)

