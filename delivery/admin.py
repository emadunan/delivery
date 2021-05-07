from django.contrib import admin
from .models import User, Item, Order, OrderItem

# Models Registered in the Admin-site.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
