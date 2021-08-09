from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic

from Customer.forms import SignUpForm


class MyLoginView(LoginView):
    pass


class MyPanelView(PermissionRequiredMixin, generic.TemplateView):
    template_name = 'Customer/panel.html'
    permission_required = 'auth.see_panel'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(phone=user.phone, password=raw_password)
            permission = Permission.objects.get(name='see_panel')
            user.user_permissions.add(permission)
            login(request, user)
            return redirect('Customer:panel')
    else:
        form = SignUpForm()
    return render(request, 'Customer/SignUp.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('Customer:login')
