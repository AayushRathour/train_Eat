from django.contrib import admin
from .models import Order, OrderItem, PNROrder, Cart, CartItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PNROrder)
admin.site.register(Cart)
admin.site.register(CartItem)
