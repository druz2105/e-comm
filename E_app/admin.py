from django.contrib import admin
from .models import (Customer, OrderItem, Order, Address, Payment, Product_Detail, Shoes_Size, Shoes, Clothes,
                     Clothes_Size, Watches, Laptop, Mobile)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product_Detail)
admin.site.register(Shoes_Size)
admin.site.register(Shoes)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Clothes)
admin.site.register(Clothes_Size)
admin.site.register(Watches)
admin.site.register(Laptop)
admin.site.register(Mobile)
