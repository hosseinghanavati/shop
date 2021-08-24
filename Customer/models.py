from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from Core.models import BaseModel, User
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user.is_staff = False
    # user.is_superuser = False

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Address(BaseModel):
    owner = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name=_("Owner"),
                              help_text=_("select owner"))
    country = models.CharField(verbose_name=_("Country"), help_text=_("enter the country name that you lived"),
                               max_length=50, default="Iran")
    province = models.CharField(verbose_name=_("Province"), help_text=_("enter the province name that you lived"),
                                max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"), help_text=_("enter the city name that you lived"), max_length=50,
                            null=True, blank=True)
    exact_address = models.TextField(max_length=200, verbose_name=_("Exact Address"),
                                     help_text=_("enter the exact address of where you lived"), null=True, blank=True)
    house_number = models.PositiveIntegerField(verbose_name=_("House number"), help_text=_("enter house number"),
                                               null=True, blank=True)
    zip_code = models.PositiveIntegerField(verbose_name=_("Zip-Code"), help_text=_("enter the zip-code"),
                                           null=True, blank=True)

    def __str__(self):
        return f"{self.province}-{self.city}: {self.zip_code}"

    @classmethod
    def filter_by_owner(cls, owner):
        query = cls.objects.filter(owner=owner)
        return query

    @classmethod
    def filter_by_country(cls, country):
        query = cls.objects.filter(country=country)
        return query

    @classmethod
    def filter_by_province(cls, province):
        query = cls.objects.filter(province=province)
        return query

    @classmethod
    def filter_by_city(cls, city):
        query = cls.objects.filter(city=city)
        return query

