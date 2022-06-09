from django.db import models


# Create your models here.

# todo: Understand what not standard user means
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return f"Customer: {self.name}"

