from django.contrib import admin

# Register your models here.
from base.models import phone, brand, cart, orders, User


class userAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'total_price', 'status', 'image', 'quantity']


admin.site.register([phone, brand, cart, User, ])
admin.site.register(orders, userAdmin)
