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


admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Product)
