from django.contrib import admin
from .models import Customer, Shipping, Order
# Register your models here.
admin.site.register(Customer)
admin.site.register(Shipping)
admin.site.register(Order)
