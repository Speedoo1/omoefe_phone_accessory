import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, redirect

from base.models import phone, brand, cart, User, orders


def index(request):
    all_phone = phone.objects.all()
    brands = brand.objects.all()

    try:
        list_cart = request.user.cart_set.all().count
    except:
        list_cart = 0
    top_sale = phone.objects.all().order_by('-Total_sold')
    new_product = phone.objects.all().order_by('-created')
    context = {'phone': all_phone, 'brands': brands, 'top_sale': top_sale, 'new': new_product, 'cart_total': list_cart}
    return render(request, 'base/index.html', context)


def product_page(request, pk):
    single_product = phone.objects.get(id=pk)
    list_cart = request.user.cart_set.all().count
    top_sale = phone.objects.all().order_by('-Total_sold')
    context = {'single_product': single_product, 'top_sale': top_sale, 'cart_total': list_cart}

    return render(request, 'base/product.html', context)


@login_required(login_url=' base: login')
def add_cart(request, pk):
    single_product = phone.objects.get(id=pk)
    price = single_product.current_price * 1
    try:
        cart_add = request.user.cart_set.get(name=single_product.name)
    except:
        messages.success(request, 'Your item has been added to cart successfully ')

        add = cart.objects.create(user=request.user, image=single_product.image, name=single_product.name,
                                  color=single_product.color,
                                  current_price=price, good_item=single_product.current_price,
                                  brand=single_product.brand, quantity='1')
        return redirect('base:product', single_product.id)

    messages.error(request, 'Item already Exit  in your cart page')

    return redirect('base:product', single_product.id)


@login_required(login_url='base:login')
def carts(request):
    lists = request.user.cart_set.all()
    pro = User.objects.get(email=request.user)
    new_product = phone.objects.all().order_by('-created')
    list_cart = request.user.cart_set.all().count
    subtotal = 0
    for i in lists:
        subtotal = subtotal + int(i.current_price)
    context = {'cart': lists, 'profile': pro, 'subtotal': subtotal, 'cart_total': list_cart, 'phone': new_product}
    return render(request, 'base/cart.html', context)


def quantity(request, pk):
    lists = request.user.cart_set.get(id=pk)
    if request.method == 'POST':
        qua = request.POST.get('in')
        if qua:
            lists.quantity = qua
            if int(qua) > 1:
                lists.current_price = lists.current_price * int(qua)
                lists.save()
                return redirect('base:cart')
            else:
                lists.current_price = lists.good_item
                lists.save()
                return redirect('base:cart')


def delete_cart(request, pk):
    get = cart.objects.get(id=pk)
    get.delete()
    return redirect('base:cart')


def loging(request):
    if request.user.is_authenticated:
        return redirect('base:index')
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("base:index")
        else:
            messages.error(request, "Email or password is incorrect")

    return render(request, 'base/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('index:index')
    if request.method == "POST":
        name = request.POST.get('username')
        address = request.POST.get('address')
        mail = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get("confirm_password")
        number = request.POST.get('number')
        gender = request.POST.get('gender')
        try:
            mail = User.objects.get(email=mail)
        except:
            if password == confirm:
                get_pass = make_password(password)
                account = User(username=name, address=address, password=get_pass, email=mail,
                               phone=number, gender=gender)
                account.save()
                messages.success(request, 'Account created successfully,')
                user = authenticate(request, username=mail, password=password)

                if user:
                    return redirect("base:login")

            else:
                messages.error(request, 'Password doesnt match ')
                return redirect("base:signup")
        messages.error(request, 'User Already have an Account')

        # return redirect("index:create")

    return render(request, 'base/signup.html')


def orderss(request):
    ord = orders.objects.all()
    context = {'order': ord}
    return render(request, 'base/orders.html', context)


def logouting(request):
    logout(request)
    return redirect('base:login')


def payment_successful(request):
    car = request.user.cart_set.all()
    for i in car:
        addoder = request.user.orders_set.create(name=i.name, status='Pending', brand=i.brand, image=i.image,
                                                 quantity=i.quantity, total_price=i.current_price)
        addoder.save()
    messages.success(request, 'Your payment as been made and your goods will be delivered to you as soon as possible')
    car.delete()
    return redirect('base:index')


@login_required(login_url='base:login')
def profile(request):
    list_cart = request.user.cart_set.all().count
    pro = User.objects.get(email=request.user)
    context = {'profile': pro, 'cart_total': list_cart}
    return render(request, 'base/profile.html', context)


def updateprofile(request):
    list_cart = request.user.cart_set.all().count
    pro = User.objects.get(email=request.user)
    if request.method == 'POST':
        name = request.POST.get('username')
        mail = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        pro.email = mail
        pro.gender = gender
        pro.address = address
        pro.username = name
        pro.phone = phone

        pro.save()
        messages.success(request, 'Profile Updated successfully')
        return redirect('base:profile')
    context = {'profile': pro, 'cart_total': list_cart}
    return render(request, 'base/updateprofile.html', context)
