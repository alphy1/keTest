from django.contrib import admin
from .models import Customer, Order, OrderItem, Product
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

admin.autodiscover()

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PriceFilter(SimpleListFilter):
    title = 'order price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('<1000', _('less than 1k')),
            ('1000-2000', _('from 1k to 2k')),
            ('>2000', _('more than 2k')),
        )

    def queryset(self, request, queryset):
        qs = [(obj.id, obj.order_price()) for obj in queryset.all()]
        ids = [obj.id for obj in queryset.all()]
        if self.value() == '<1000':
            ids = [objId for objId, price in qs if price < 1000]
        elif self.value() == '1000-2000':
            ids = [objId for objId, price in qs if 1000 <= price <= 2000]
        elif self.value() == '>2000':
            ids = [objId for objId, price in qs if price > 2000]

        return queryset.filter(id__in=ids)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_price')
    list_filter = ['status', 'customer__phone_number', PriceFilter, 'created_date']


admin.site.register(OrderItem)

admin.site.register(Product)
