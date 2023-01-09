from django.contrib import admin

# Register your models here.
from base.models import phone, brand, cart, orders, User

admin.site.register([phone, brand, cart, orders,User])
