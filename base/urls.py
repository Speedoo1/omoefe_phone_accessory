from django.shortcuts import render

# Create your views here.
from django.urls import path

from base import views

app_name = 'base'

urlpatterns = [

    path('', views.index, name='index'),
    path('product/<str:pk>', views.product_page, name='product'),
    path('cart/', views.carts, name='cart'),
    path('add_cart/<str:pk>', views.add_cart, name='add_cart'),
    path('delete_cart/<str:pk>', views.delete_cart, name='delete_cart'),
    path('quantity/<str:pk>', views.quantity, name='quantity'),
    path('login/', views.loging, name='login'),
    path('logout/', views.logouting, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('orders/', views.orders, name='orders'),
    path('payment_successful/', views.payment_successful, name='successful')
]
