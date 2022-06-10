from django.contrib import admin
from .models import Customer, Order, OrderItem, Product

admin.autodiscover()

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Product)
