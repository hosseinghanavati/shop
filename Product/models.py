from django.db import models
from .validators import *

# Create your models here.
from django.utils.translation import gettext_lazy as _

from Core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50, help_text=_("Insert name of category"))
    slug = models.SlugField(verbose_name=_("Slug"), help_text=_("Insert Slug name"))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_("Category"),
                               help_text=_("choose parent category"), null=True, blank=True,
                               related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Brand(BaseModel):
    name = models.CharField(verbose_name=_("Name"), help_text=_("Brand name"), max_length=50, unique=True)
    image = models.FileField(upload_to='Brands/images/', blank=True, null=True, verbose_name=_("category image"),
                             help_text=_("upload the category image"))

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    name = models.CharField(verbose_name=_("Name"), help_text=_("product name"), max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand"),
                              help_text=_("choose brand of product"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"),
                                 help_text=_("choose category of product"))
    image = models.FileField(upload_to='Product/images/', blank=True, null=True, verbose_name=_("product image"),
                             help_text=_("upload the product image"))
    inventory = models.PositiveIntegerField(verbose_name=_("Inventory"),
                                            help_text=_("how many of this product we have in our inventory"))
    price = models.PositiveIntegerField(verbose_name=_("Price"), help_text=_("set price of product"))
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, verbose_name=_("Discount"),
                                 help_text=_("choose the discount"), null=True, blank=True)

    # @property
    # def img_url(self):
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url

    def __str__(self):
        return f"{self.name}-{self.brand}"

    def final_price(self):
        if self.discount:
            if self.discount.discount_in_amount:
                return self.price - self.discount.discount_in_amount
            elif self.discount.discount_in_percent:
                disc = self.price * self.discount.discount_in_percent / 100
                if disc <= self.discount.maximum_amount:
                    return self.price - disc
                else:
                    return self.price - self.discount.maximum_amount
        else:
            return self.price

    @classmethod
    def filter_by_category(cls, category):
        query = cls.objects.filter(category=category)
        return query

    @classmethod
    def filter_by_brands(cls, brand):
        query = cls.objects.filter(brand=brand)
        return query

    @classmethod
    def max_price(cls):
        query = cls.objects.aggregate(models.Max("price"))
        return query

    @classmethod
    def avg_price(cls):
        query = cls.objects.aggregate(models.Avg("price"))
        return query


class Discount(BaseModel):
    types = [
        ('PT', 'percent'),
        ('AT', 'amount')
    ]
    type = models.CharField(
        verbose_name=_("Type"),
        help_text=_("Choose type of discount"),
        choices=types,
        default='PT',
        max_length=2
    )
    discount_in_percent = models.FloatField(verbose_name=_("Amount in percent"),
                                            help_text=_("set discount in percent type"),
                                            null=True, blank=True, validators=[discount_percent_validator])
    discount_in_amount = models.PositiveIntegerField(verbose_name=_("Discount in amount"),
                                                     help_text=_("set discount in amount"), null=True, blank=True)
    maximum_amount = models.IntegerField(
        verbose_name=_("Maximum amount"),
        help_text=_("if you choose percent type you can insert maximum amount"),
        null=True,
        blank=True
    )

    def __str__(self):
        if self.type == 'PT':
            return f"{self.type}->{self.discount_in_percent}-{self.maximum_amount}"
        else:
            return f"{self.type}->{self.discount_in_amount}"

