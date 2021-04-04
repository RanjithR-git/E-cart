from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.contrib import messages
from admin1.models import product, Categories
from . models import *

# Create your views here.

def home(request):
    prod = product.objects.all()
    return render(request, 'index.html',{'products':prod})


def usersignup(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            if User.objects.filter(username=username).exists(): 
                return JsonResponse('user', safe=False)
            elif User.objects.filter(email=email).exists():
                return JsonResponse('user', safe=False)
            elif UserData.objects.filter(phone=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                user = UserData.objects.create(phone = phone,user = user)
                return JsonResponse('true', safe=False)
        
        else:
            return render(request, 'user/registered.html')

def userlogin(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user= auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'login.html')

def userregister(request):
    return render(request, 'registered.html')

def createuser(request):
    return render(request, 'registered.html')
        
def userlogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(userlogin)

def add_to_cart(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            quantity = request.POST['quantity']
            user = request.user
            products = product.objects.get(id=id)
            print(quantity, products)
            Cart.objects.create(quantity=quantity, product=products, user=user)
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('true', safe=False)
    else:
        return redirect(home)

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        grandtotal = 0
        print(cart.count())
        for item in cart:
            item.totalprice = item.quantity * item.product.price
            grandtotal= grandtotal + item.totalprice
        products = product.objects.all()
        item_count = cart.count()
        if item_count == 0:
            return render(request, 'usercart.html', {'products': products, 'no': item_count})
        else:
            return render(request, 'usercart.html', {'cart': cart, 'products': products, 'no': item_count, 'grandtotal': grandtotal})
    
    else:
        return redirect(home)

def delete_cart_item(request, id):
    if request.user.is_authenticated:
        cart =Cart.objects.filter(id=id)
        print(cart)
        cart.delete()
        return redirect(show_cart)
    else:
        return redirect(home)

def edit_cart(request):
    id = request.POST["id"]
    count = 1
    grandtotal = 0
    cart = Cart.objects.filter(user=request.user)
    item = Cart.objects.get(id=id)
    if request.POST["value"] == "add":
        item.quantity = item.quantity + count
        item.save()
        price = item.product.price * item.quantity

        for item in cart:
            grandtotal= grandtotal + item.product.price * item.quantity
    
    elif request.POST["value"] == "sub":
        item.quantity = item.quantity - count
        item.save()
        price = item.product.price * item.quantity

        for item in cart:
            grandtotal = grandtotal + item.product.price * item.quantity

    return JsonResponse({'total':price, 'grandtotal':grandtotal}, safe=False)
    

def view_product(request):
    pass

