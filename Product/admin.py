from django.contrib import admin
from .models import *
from django.utils.translation import gettext as _
# Register your models here.

# admin.site.register(Category)
# admin.site.register(Brand)
# admin.site.register(Discount)
# admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Delete"), {'fields': ['deleted', 'delete_time_stamp']}),
        (_("Name"), {'fields': ['name', 'slug']}),
        (_("sub"), {'fields': ['is_sub', 'sub_category']})
    ]
    list_display = ('name', 'is_sub', 'create_time_stamp')
    list_filter = ('is_sub', 'create_time_stamp')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Delete"), {'fields': ['deleted', 'delete_time_stamp']}),
        (_("Name"), {'fields': ['name', 'slug']}),
        (_("Image"), {'fields': ['image']})
    ]
    list_display = ('name', 'create_time_stamp')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Delete"), {'fields': ['deleted', 'delete_time_stamp']}),
        (_("Name"), {'fields': ['name', 'slug']}),
        (_("Category"), {'fields': ['category']}),
        (_("Brand"), {'fields': ['brand']}),
        (_("Description"), {'fields': ['description']}),
        (_("Inventory"), {'fields': ['inventory']}),
        (_("About Price"), {'fields': ['price', 'discount']}),
        (_("Image"), {'fields': ['image']}),
    ]
    list_display = ('name', 'brand', 'create_time_stamp', 'price', 'discount')
    list_filter = ('category', 'brand', 'create_time_stamp')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Delete"), {'fields': ['deleted', 'delete_time_stamp']}),
        (_("Type"), {'fields': ['type']}),
        (_("Discount in percent"), {'fields': ['discount_in_percent', 'maximum_amount']}),
        (_("Discount in amount"), {'fields': ['discount_in_amount']}),
    ]
    list_display = ('type', 'discount_in_percent', 'discount_in_amount', 'create_time_stamp')
    list_filter = ('type', 'create_time_stamp')
