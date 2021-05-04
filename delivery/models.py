from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15)
    address = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.username}, {self.phone}"


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    category = models.CharField(max_length=50)
    price = models.FloatField()
    photo_url = models.TextField()
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_name', fields=['name'])
        ]

    


class Order(models.Model):
    user_client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_orders")
    user_delivery = models.ForeignKey(User, on_delete=models.CASCADE, related_name="delivery_orders")
    items = models.ManyToManyField(Item, through="OrderItem", related_name="orders")
    received_at = models.DateTimeField()
    submitted_at = models.DateTimeField()
    delivered_at = models.DateTimeField()
    state = models.TextField(max_length=10)

    def __str__(self):
        return f"{self.user.username}, made order number '{self.id}' at ({self.received_at})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()
