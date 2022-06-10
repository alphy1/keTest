from django.db import models


# Create your models here.

# todo: Understand what not standard user means
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created')
    address = models.CharField(max_length=200)
    CREATED = 'CR'
    COLLECTING = 'CO'
    DELIVERING = 'DG'
    DELIVERED = 'DE'
    ISSUED = 'IS'
    CANCELLED = 'CA'
    STATUS_CHOICES = [
        (CREATED, 'Создан'),
        (COLLECTING, 'Собирается'),
        (DELIVERING, 'Доставляется'),
        (DELIVERED, 'Доставлен'),
        (ISSUED, 'Выдан'),
        (CANCELLED, 'Отменён')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=CREATED,
    )

    def __str__(self):
        return f'Order #{self.id}'

    def order_price(self):
        result = 0
        for item in self.orderitem_set.all():
            result += item.price * item.quantity
        return result


class Product(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
