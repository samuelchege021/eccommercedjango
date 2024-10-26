from django.contrib import admin
from my_app.models import Product
# from my_app.models import Payment
from my_app.models import CartItem

# Register your models here.
admin.site.register(Product),
# admin.site.register(Payment)

admin.site.register(CartItem)