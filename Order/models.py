from django.db import models

# Create your models here.

from Core.models import *
from Customer.models import Customer, Address
from Product.models import Product
from django.utils.translation import gettext_lazy as _


class OrderItem(BaseModel):
    order = models.ForeignKey('Order', on_delete=models.PROTECT, verbose_name=_("Order"),
                              help_text=_("order that item belong to it"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"),
                                help_text=_("product that chosen"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), help_text=_("quantity of that product"),
                                           default=1)

    def __str__(self):
        return f"{self.product}: {self.quantity} -> {self.order}"


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"),
                                 help_text=_("choose the customer"))
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name=_("Address"),
                                help_text=_("choose the address"))
    status = models.CharField(choices=[
        ('recorded', 'recorded'),
        ('confirmed', 'confirmed'),
        ('canceled', 'canceled'),
        ('paid', 'paid'),
        ('sent', 'sent'),
        ('received', 'received')
    ], default='recorded', verbose_name=_("Status"), help_text=_("choose status of order"), max_length=10)
    products = models.ManyToManyField(Product, through=OrderItem, through_fields=['order_id', 'product_id'],
                                      verbose_name=_("Products"), help_text=_("Products of order"))
    total_price = models.PositiveIntegerField(verbose_name=_("Total Price"), help_text=_("total price of order"),
                                              null=True, blank=True)
    final_price = models.PositiveIntegerField(verbose_name=_("Final Price"), null=True, blank=True,
                                              help_text=_("final price of order after calculate the discount"))

    def __str__(self):
        return f"{self.id}: {self.status} -> {self.customer}"
