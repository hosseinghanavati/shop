from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from Core.models import User
from Customer.models import Customer


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
