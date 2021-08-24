from django.contrib import admin
from .models import *
from django.utils.translation import gettext as _
# Register your models here.

# admin.site.register(Category)
# admin.site.register(Brand)
# admin.site.register(Discount)
# admin.site.register(Product)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Name"), {'fields': ['name', 'slug']}),
        (_("sub"), {'fields': ['is_sub', 'sub_category']})
    ]
    # inlines = [ProductInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Name"), {'fields': ['name', 'slug']}),
        (_("Image"), {'fields': ['image']})
    ]
    # inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Name"), {'fields': ['name', 'slug']}),
        (_("Category"), {'fields': ['category']}),
        (_("Brand"), {'fields': ['brand']}),
        (_("Description"), {'fields': ['description']}),
        (_("Inventory"), {'fields': ['inventory']}),
        (_("About Price"), {'fields': ['price', 'discount']}),
        (_("Image"), {'fields': ['image']}),
    ]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Type"), {'fields': ['type']}),
        (_("Discount in percent"), {'fields': ['discount_in_percent', 'maximum_amount']}),
        (_("Discount in amount"), {'fields': ['discount_in_amount']}),
    ]
