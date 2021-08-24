from django import forms
from django.utils.translation import gettext_lazy as _


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(label=_("Quantity"), min_value=1, max_value=9)

