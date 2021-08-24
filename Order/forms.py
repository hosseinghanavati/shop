from django import forms
from django.utils.translation import gettext_lazy as _

from Customer.models import Address
from Order.models import Order


class AddressShowOrder(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.all())

    def __init__(self, *args, **kwargs):
        owner_id = kwargs.pop('owner_id', None)
        super(AddressShowOrder, self).__init__(*args, **kwargs)

        if owner_id:
            self.fields['address'].queryset = Address.objects.filter(owner_id=owner_id)



