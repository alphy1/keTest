from django.contrib import admin
from .models import Customer, Order, OrderItem, Product

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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')
    list_filter = ['status', 'customer__phone_number', 'created_date']
    list_display = ('id', 'customer', 'order_price')


admin.site.register(OrderItem)

admin.site.register(Product)
