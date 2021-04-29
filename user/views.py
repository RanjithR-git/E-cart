from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.contrib import messages
from admin1.models import product, Categories
from . models import *
from twilio.rest import Client
import datetime
import razorpay
import json
import random
from admin1.models import *
from django.core.files import File
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if  Offer.objects.exists():
            offer = Offer.objects.all()
            for offers in offer:
                if offers.is_started == True:
                    offers.start = True
                    offers.save()
                if offers.is_valid == True:
                    offers.start = False
                    offers.save()
        prod = product.objects.all()
        user = request.user
        cart = Cart.objects.filter(user=user)
        item_count = cart.count()
        offer = Offer.objects.all() 
        context = {'products':prod , 'no':item_count, 'offers':offer}
        return render(request, 'index.html', context)
    else:
        return redirect(userlogin)

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

def contact(request):
    return render(request, 'mail.html')

# def login_with_otp(request):
#     return render(request, 'otp.html')

def otp_generate(request):
        if request.method == 'POST':
            
            phone = request.POST['Phone']
            user1 = UserData.objects.get(phone=phone)
            if user1 is not None:
                random_number = random.randint(1000, 9999)
                otp = random_number
                account_sid = 'AC662ca35ca062115f93bfcdef4c9d0846'
                auht_token = 'da644d6f37b02d85e8f763913c18c591'
                client = Client(account_sid, auht_token)

                message = client.messages.create(
                body=f"Your OTP is {otp}",
                from_='+18034898307',
                to=f'+919645513754'
            )
               
                context = { 'user':user1, 'otp':otp}
                return render(request, 'otp.html', context)
        else:
            return render(request, 'otp.html')

def otp_validate(request, id, otp):
    if request.method =='POST':
        # phone = request.session['phone']
        # user1 = UserData.objects.get(phone=phone)
        customer = UserData.objects.get(id=id)
        user = customer.user

        
        user_otp = request.POST['userOTP']
        
        if otp == int(user_otp):
            auth.login(request, user)
            return redirect(home)
        else:
            return redirect(otp_generate)
    else:
        return render(request, 'otp.html')


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            cart = Cart.objects.filter(user=user)
            user.first_name = request.POST['name']
            user.last_name = request.POST['mobile']
            user.email = request.POST['email']
            user.save()

            if Userprofile.objects.filter(user=user).exists():
                user_details = Userprofile.objects.get(user=user)

                if 'profile-image-upload' not in request.POST:
                    profile_pic = request.FILES.get('profile_image_upload')
                else:
                    profile_pic = user_details.profilepic
                
                user_details.profilepic = profile_pic
                user_details.save()
            else:
                profile_pic = request.FILES.get('profile-image-upload')
                Userprofile.objects.create(user=user, profilepic=profile_pic)
            
            return redirect(home)
        else:
            cartegory = Categories.objects.all()
            user = request.user
            cart = Cart.objects.filter(user= user)
            item_count = cart.count()
            if Userprofile.objects.filter(user=user).exists():
                user_details = Userprofile.objects.get(user=user)
                return render(request, 'user_profile.html', {'catergory_data':cartegory, 'no':item_count, 'userdetails':user_details})
            else:
                return render(request, 'user_profile.html', {'catergory_data':cartegory,'no': item_count})
    else: 
        return redirect(userlogin)
        
def userlogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(userlogin)

def add_to_cart(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            quantity = request.POST['quantity']
            user = request.user
            cart_product = product.objects.get(id=id)
            
            Cart.objects.create(quantity=quantity, cart_product=cart_product, user=user)
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
        for item in cart:
            item.totalprice = item.quantity * item.cart_product.price
            grandtotal += item.totalprice
        item_count = cart.count()
        if item_count == 0:
            return render(request, 'usercart.html', { 'no': item_count})
        else:
            return render(request, 'usercart.html', {'cart': cart, 'no': item_count, 'grandtotal': grandtotal})
    
    else:
        return redirect(home)

def delete_cart_item(request, id):
    if request.user.is_authenticated:
        cart =Cart.objects.filter(id=id)
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
        price = item.cart_product.price * item.quantity

        for item in cart:
            grandtotal= grandtotal + item.cart_product.price * item.quantity
    
    elif request.POST["value"] == "sub":
        item.quantity = item.quantity - count
        item.save()
        price = item.cart_product.price * item.quantity

        for item in cart:
            grandtotal = grandtotal + item.cart_product.price * item.quantity

    return JsonResponse({'total':price, 'grandtotal':grandtotal}, safe=False)
    


def show_address(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        item_count = cart.count()
        address = Address.objects.filter(user=user)
        return render(request, 'user_address.html', {'no':item_count, 'address':address})
    else:    
        return redirect(home)

def create_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            name = request.POST['firstname']
            email = request.POST['email']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            Address.objects.create(user=user, name=name, email=email, address=address, city=city, state=state, pincode=pincode)
            return redirect(show_address)
        else:
            return render(request, 'edit_address.html')
    
    return redirect(home)


def edit_address(request, id):
    if request.user.is_authenticated:
        address_data = Address.objects.get(id=id)
        if request.method == 'POST':
            address_data.name = request.POST['firstname']
            address_data.email = request.POST['email']
            address_data.address = request.POST['address']
            address_data.city = request.POST['city']
            address_data.state = request.POST['state']
            address_data.pincode = request.POST['pincode']
            address_data.save()
            return redirect(show_address)
        else:
            edit = 1
            return render(request, 'edit_address.html', {'address':address_data, 'edit':edit})
    else:
        return redirect(home)

def delete_address(request, id):
    if request.user.is_authenticated:
        address = Address.objects.get(id=id)
        address.delete()
        return redirect(show_address)
    else:
        return redirect(home)

def user_payment(request, id):
    if request.user.is_authenticated:
        if request.method== 'POST':
            user = request.user
            address = Address.objects.get(id=id)
            grandtotal = 0
            date = datetime.datetime.now()
            trans_id = datetime.datetime.now().timestamp()
            mode = request.POST['mode']
            address.name = request.POST['name']
            address.email = request.POST['email']
            address.address = request.POST['address']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.pincode = request.POST['pincode']
            address.save()
            cart = Cart.objects.filter(user=user)
            status = 'pending'
            for item in cart:
                item.totalprice= item.quantity * item.cart_product.price
                grandtotal = grandtotal + item.totalprice
            
            for item in cart:
                Purchase.objects.create(user=user, address=address, products=item.cart_product, quantity=item.quantity, totalprice=item.cart_product.price * item.quantity, tdate=date,  tid=trans_id, payment_mode=mode, order_status='pending', payment_status=status)
                item.cart_product.quantity = item.cart_product.quantity - item.quantity
                item.cart_product.save()
            cart.delete()
             
            
            if mode == 'COD':
                mode = "COD"
                messages.info(request, "Order placed Successfully")
                return JsonResponse({'mode':mode, 'tid':trans_id}, safe=False)
            
            elif mode == 'Paypal':
                mode = 'Paypal'
                return JsonResponse({'mode':mode, 'tid':trans_id}, safe=False)

            elif mode == 'Razorpay':
                mode = 'Razorpay'
                return JsonResponse({'mode':mode, 'tid': trans_id}, safe=False)
            
            else:
                coupon = Coupons.objects.get(user=user)
                coupon.used = False
                coupon.save()
                del request.session['price']
                return JsonResponse('false', safe=False)


        else:
            user= request.user
            address = Address.objects.get(user=request.user)
            cart= Cart.objects.filter(user=user)
            item_count = cart.count()
            grandtotal = 0
            for item in cart:
                item.totalprice = item.quantity * item.cart_product.price
                grandtotal = grandtotal + item.totalprice

            if  Coupons.objects.filter(user=user).exists():
                if request.session.has_key('coupon'):
                    code = request.session['coupon']
                    coupon = Coupons.objects.get(code=code, user=user)
                    discount = int(coupon.percent)
                    discount_price = grandtotal - (grandtotal*(discount/100))
                    paypal_price = discount_price/70
                    razorpay_price = discount_price*100
                    context = {'cart':cart, 'no':item_count, 'grandtotal':grandtotal, 'address':address,'price':discount_price,'discount':True, 'paypal_price':paypal_price, 'razorpay_price':razorpay_price}
                    return render(request, 'user_payment.html',context)
                else:
                    user= request.user
                    coupon = Coupons.objects.filter(user=user)
                    paypal_price=grandtotal/70
                    razorpay_price = grandtotal*100
                    context = {'cart':cart, 'no':item_count, 'grandtotal':grandtotal, 'address':address,'price':grandtotal, 'coupon':coupon, 'coupon_exist':True, 'paypal_price': paypal_price, 'razorpay_price':razorpay_price}
                    return render(request, 'user_payment.html', context)
            else:
                paypal_price=grandtotal/70
                razorpay_price = grandtotal*100
                context = {'cart':cart, 'no':item_count, 'grandtotal':grandtotal, 'address':address,'price':grandtotal, 'paypal_price':paypal_price, 'razorpay_price':razorpay_price}
                return render(request, 'user_payment.html', context)
    else:
        return redirect(home)

def paypal(request):
    tr_id = request.POST['tid']
    purchases = Purchase.objects.filter(tid=tr_id)
    for purchase in purchases:
        purchase.payment_status = 'SUCCESS'
        purchase.save()
    return JsonResponse('success', safe=False)

def razorpay(request):
    tr_id = request.POST['tid']
    purchases = Purchase.objects.filter(tid=tr_id)
    for purchase in purchases:
        purchase.payment_status = 'SUCCESS'
        purchase.save()
    return JsonResponse('success', safe=False)

def order_history(request):
    if request.user.is_authenticated:
        user = request.user
        purchases = Purchase.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        item_count = cart.count()
        return render(request, 'user_order_history.html',{'items_data':purchases, 'no':item_count})

def view_coupon(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return redirect(home)
        else:
            user = request.user
            if Coupons.objects.filter(user=user).exists():
                coupon = Coupons.objects.filter(user=user, end__gt=date.today())
                context = {'coupons':coupon}
                return render(request, 'view_coupon.html', context)
            else:
                return render(request, 'view_coupon.html')
    else:
        return redirect(home)

def check_coupon(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            check_code = request.POST['check_code']
            user = request.user
            if Coupons.objects.filter(code = check_code, user=user).exists():
                coupon = Coupons.objects.get(code=check_code, user=user)
                if coupon.start <= date.today() and coupon.end >= date.today():
                    if coupon.used == False:
                        coupon.used = True
                        coupon.save()
                        request.session['coupon'] = check_code
                        return JsonResponse('true', safe=False)
                    else:
                        return JsonResponse('used', safe= False)
                else:
                    return JsonResponse('date',safe= False) 
            else:
                return JsonResponse('false', safe=False)
        else:
            return redirect(home)
    return redirect(home)   

def search(request):
    if request.user.is_authenticated:
        key = request.GET['key']
        prod1 = product.objects.filter(product_name__icontains = key)
        prod2 = product.objects.filter(category__category__icontains = key)
        exist = True
        procucts = []
        for ad  in prod1:
            procucts.append(ad)
        
        for ad in prod2:
            if ad in procucts:
                pass
            else:
                procucts.append(ad)
        context = {
            'products':procucts
        }
        return render(request, 'filter.html',context)
    return redirect(home)
        