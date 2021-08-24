from django.contrib import admin
from .models import Order, OrderItem
from django.utils.translation import gettext_lazy as _
# Register your models here.

# admin.site.register(Order)
# admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 3
    raw_id_fields = ('product', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Time"), {'fields': ['create_time_stamp', 'modify_time_stamp', 'delete_time_stamp']}),
        (_("Customer"), {'fields': ['customer', 'address']}),
        (_("Product"), {'fields': ['product', 'total_price', 'final_price']}),
        (_("Status"), {'fields': ['status']}),
    ]
    list_display = ('id', 'customer', 'status', 'create_time_stamp')
    list_filter = ('status', )
    inlines = (OrderItemInline, )
