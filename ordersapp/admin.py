from django.contrib import admin
from .models import Order, OrderItem

admin.register(Order)
admin.register(OrderItem)
