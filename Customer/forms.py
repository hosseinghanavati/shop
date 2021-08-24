from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from Core.models import User
from Customer.models import Customer, Address


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=13, min_length=11, label=_('Phone'))
    password = forms.CharField(max_length=32, label=_('Password'))


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = user.phone
        if commit:
            user.save()
        return user


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'email')


class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('country', 'province', 'city', 'exact_address', 'house_number', 'zip_code')


