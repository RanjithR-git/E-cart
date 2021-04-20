from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.contrib import messages
from user.models import UserData
from . models import *
from user.models import *
from . models import product, Categories
from django.core.files import File
from datetime import date, datetime, timedelta
from PIL import Image
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
# Create your views here.

def adminlogin(request):
    if request.session.has_key('password'):
        return redirect(adminhome)
    else:
        if request.method== 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username=='ranjith' and password=='2020':
                request.session['password']=password
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'adminlogin.html')

def adminhome(request):
    if request.session.has_key('password'):
        if request.method=='POST':
            pass
        else:
            user = UserData.objects.all()
            return render(request, 'adminhome.html', {'user':user}) 
    else:
        return redirect(adminlogin)

def adduser(request):
    if request.session.has_key('password'):
        if request.method=='POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            if User.objects.filter(username=username).exists():
                return JsonResponse('user', safe=False)
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            else:
                user= User.objects.create_user(first_name=first_name, last_name=last_name, username=username,email=email,password=password)
                UserData.objects.create(user=user,phone=phone)
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'adduser.html')
    else:
        return redirect(adminlogin)

# def adminedit(request,id):
#     if request.session.has_key('password'):
#         if request.method=='POST' :
#             user1 = UserData.objects.get(id=id)
#             user = User.objects.get(id=user1.user_id)
#             user.first_name= request.POST['first_name']
#             user.last_name= request.POST['last_name']
#             user.username= request.POST['username']
#             user.save()
#             phone = request.POST['phone']
#             user1.phone= phone
#             user1.save()
#             return JsonResponse('true',safe=False)
#         else:
#             user = UserData.objects.get(id=id)
#             return render(request, 'adminedit.html',{'user':user})
#     else:
#         return redirect(adminlogin) 
# def admindelete(request,id):
#     if request.session.has_key('password'):
#         user = UserData.objects.get(id=id)
#         user.delete()
#         return redirect(usertable)
#     else:
#         return redirect(adminlogin)

def adminlogout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(adminlogin)

def usertable(request):
    user = UserData.objects.all()
    return render(request, 'usertable.html', {'user' : user})

def user_block(request, id):
    if request.session.has_key('password'):
        user = User.objects.get(id = id) 
        if user.is_active == True:
            user.is_active = False
        else:
            user.is_active = True 
        user.save()
        return redirect(usertable)
    else:
        return redirect(adminlogin)

def add_category(request):
    if request.method == 'POST':
        name = request.POST['category']
        catagory = Categories.objects.create(category=name)
        catagory.save()
        return redirect(view_category)
    else:
        return render(request,'add_category.html')    
 
def view_category(request):
    categories = Categories.objects.all()
    return render(request, 'category.html',{'categories':categories})

def edit_category(request,id):
    if request.method== 'POST':
        category= Categories.objects.get(id=id)
        name = request.POST['category']
        category.category=name  
        category.save()
        return redirect(view_category)
    category = Categories.objects.get(id=id)
    return render(request, 'edit_category.html',{'category':category})

def delete_category(request,id):
    if request.session.has_key('password'):
        category= Categories.objects.get(id=id)
        category.delete()
        return render(request, 'adminhome.html',{'category':category})
    else:
        return redirect(view_category)

def create_product(request):
    if request.method== 'POST':
        product_name = request.POST['product_name']
        quantity= request.POST['quantity']
        price= request.POST['price']
        desc = request.POST['desc']
        # img = request.FILES.get('images')
        image_data = request.POST['pro_img']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        print('hai',ext)
        
        img_decoded = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        category_id= request.POST['category_id']
        product.objects.create(product_name=product_name,category_id=category_id,quantity=quantity,price=price,desc=desc,image=img_decoded)
        return redirect(show_product)
    else:
        category_id= Categories.objects.all()
        return render(request, 'admin_add_product.html',{'categories':category_id})


def show_product(request):
    if request.user.is_authenticated:
        products=product.objects.all()
        return render(request, 'admin_view_product.html',{'product':products})
    else:
        return redirect(adminhome)

def delete_product(request, id):
    products= product.objects.get(id=id)
    products.delete()
    return redirect(show_product)

def edit_product(request, id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            product_name = request.POST['product_name']
            quantity= request.POST['quantity']
            price= request.POST['price']
            desc = request.POST['desc']

            products = product.objects.get(id=id)
            products.product_name= product_name
            products.quantity = quantity
            products.price = price
            products.desc =desc
            if 'image' not in request.POST:
                image = request.FILES.get('image')
            else:
                image = products.image
            products.image= image
            products.save()
           
            return redirect(show_product)
        else:
            products = product.objects.get(id=id)
            return render(request, 'admin_product_edit.html',{'products':products})
    else:
        return redirect(adminlogin)       


def admin_orders(request):
    if request.session.has_key('password'):
        purchases = Purchase.objects.filter(order_status ='pending')
        purchase_sorted  = {}
        for purchased in purchases:
            if not purchased.tid in purchase_sorted.keys():
                purchase_sorted[purchased.tid] = purchased
                purchase_sorted[purchased.tid].purchasedprice = purchased.totalprice
            else:
                purchase_sorted[purchased.tid].purchasedprice += purchased.totalprice
        
        return render(request, 'admin_orders.html', {'table_data': purchase_sorted})
    else:
        return redirect(adminlogin)

def admin_sub_orders(request, status):
    if status =='Confirmed':
        purchases = Purchase.objects.filter(order_status=status)
        purchase_sorted = {}
        for purchased in purchases:
            if purchased.tid in purchase_sorted.keys():
                purchase_sorted[purchased.tid] = purchased
                purchase_sorted[purchased.tid].purchasedprice = purchased.totalprice
            else:
                purchase_sorted[purchased.tid].purchasedprice = purchased.totalprice
        return render(request, 'admin_sub_orders.html', {'table_data': purchase_sorted, 'heading': status})

    elif status == 'Cancelled':
        purchases = Purchase.objects.filter(order_status = status)
        purchase_sorted = {}
        for purchased in purchases:
            if purchased.tid in purchase_sorted.keys():
                purchase_sorted[purchased.tid] = purchased
                purchase_sorted[purchased.tid].purchasedprice = purchased.totalprice
            else:
                purchase_sorted[purchased.tid].purchasedprice = purchased.totalprice
        return render(request, 'admin_sub_orders.html', {'table_data': purchase_sorted, 'heading': status})

def cancel_order(request, tid):
    if request.session.has_key('password'):
        Purchases = Purchase.objects.filter(tid=tid)
        for items in Purchases:
            items.purchase_status = 'Cancelled'
            items.save()
        return redirect(admin_orders)
    else:
        return redirect(adminlogin)

def confirm_order(request, tid):
    if request.session.has_key('password'):
        Purchases = Purchase.objects.filter(tid=tid)
        for items in Purchases:
            items.purchase_status = 'Confirmed'
            items.save()
        return redirect(admin_sub_orders)
    else:
        return redirect(adminlogin)

def admin_reports(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            if 'date_report' in  request.POST:
                from_date = request.POST['from']
                to_date = request.POST['to']
                purchases = Purchase.objects.filter(tdate__range=[from_date, to_date])
                purchase_sorted_tid = {}
                for purchased in purchases:
                    if not purchased.tid in purchase_sorted_tid.keys():
                        purchase_sorted_tid[purchased.tid] = purchased
                        purchase_sorted_tid[purchased.tid].purchasedprice = purchased.totalprice
                        purchase_sorted_tid[purchased.tid].total_products = 1
                    else:
                        purchase_sorted_tid[purchased.tid].purchasedprice += purchased.totalprice
                        purchase_sorted_tid[purchased.tid].total_products += 1
                purchase_sorted_date = {}

                for purchases, purchase_sorted in purchase_sorted_tid.items():
                    if not purchase_sorted.tdate in purchase_sorted_date.keys():
                        purchase_sorted_date[purchase_sorted.tdate] = {"order_count" : 1, "price": purchase_sorted.purchasedprice, "total_products": purchase_sorted.total_products}
                    else:
                        purchase_sorted_date[purchase_sorted.tdate]["order_count"] += 1
                        purchase_sorted_date[purchase_sorted.tdate]["price"] += purchase_sorted.purchasedprice
                        purchase_sorted_date[purchase_sorted.tdate]["total_products"] += purchase_sorted.total_products
                return render(request, 'admin_reports.html', {'table_data': purchase_sorted_date})
            
            elif 'category_report' in request.POST:
                report_type = request.POST['report_type']
                if report_type == 'this_day':
                    heading = 'Today'
                    today_date = date.today()
                    purchases = Purchase.objects.filter(tdate= today_date)
                    purchase_sorted_tid = {}
                    for purchased in purchases:
                        if not purchased.tid in purchase_sorted_tid.keys():
                            purchase_sorted_tid[purchased.tid] = purchased
                            purchase_sorted_tid[purchased.tid].purchasedprice = purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products = 1
                        else:
                            purchase_sorted_tid[purchased.tid].purchasedprice += purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products += 1
                    purchase_sorted_date = {}

                    for purchases, purchase_sorted in purchase_sorted_tid.items():
                        if not purchase_sorted.tdate in purchase_sorted_date.keys():
                            purchase_sorted_date[purchase_sorted.tdate] = {"order_count" : 1, "price": purchase_sorted.purchasedprice, "total_products": purchase_sorted.total_products}
                        else:
                            purchase_sorted_date[purchase_sorted.tdate]["order_count"] += 1
                            purchase_sorted_date[purchase_sorted.tdate]["price"] += purchase_sorted.purchasedprice
                            purchase_sorted_date[purchase_sorted.tdate]["total_products"] += purchase_sorted.total_products
                    return render(request, 'admin_reports.html', {'table_data' : purchase_sorted_date, 'heading': heading})

                elif report_type == 'last_7_days':
                    heading = 'Last 7 days'
                    today_date = date.today()
                    last_week_from_date = today_date - timedelta(days=7)
                    purchases = Purchase.objects.filter(tdate__range= [last_week_from_date, today_date])
                    purchase_sorted_tid = {}
                    for purchased in purchases:
                        if not purchased.tid in purchase_sorted_tid.keys():
                            purchase_sorted_tid[purchased.tid] = purchased
                            purchase_sorted_tid[purchased.tid].purchasedprice = purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products = 1
                        else:
                            purchase_sorted_tid[purchased.tid].purchasedprice += purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products += 1
                    purchase_sorted_date = {}

                    for purchases, purchase_sorted in purchase_sorted_tid.items():
                        if not purchase_sorted.tdate in purchase_sorted_date.keys():
                            purchase_sorted_date[purchase_sorted.tdate] = {"order_count" : 1, "price": purchase_sorted.purchasedprice, "total_products": purchase_sorted.total_products}
                        else:
                            purchase_sorted_date[purchase_sorted.tdate]["order_count"] += 1
                            purchase_sorted_date[purchase_sorted.tdate]["price"] += purchase_sorted.purchasedprice
                            purchase_sorted_date[purchase_sorted.tdate]["total_products"] += purchase_sorted.total_products
                    return render(request, 'admin_reports.html', {'table_data' : purchase_sorted_date, 'heading':heading})
                
                elif report_type == 'this_month':
                    today_date = date.today()
                    month = today_date.strftime('%B')
                    purchases = Purchase.objects.filter(tdate__month = today_date.month)
                    purchase_sorted_tid = {}
                    for purchased in purchases:
                        if not purchased.tid in purchase_sorted_tid.keys():
                            purchase_sorted_tid[purchased.tid] = purchased
                            purchase_sorted_tid[purchased.tid].purchasedprice = purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products = 1
                        else:
                            purchase_sorted_tid[purchased.tid].purchasedprice += purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products += 1
                    purchase_sorted_date = {}

                    for purchases, purchase_sorted in purchase_sorted_tid.items():
                        if not purchase_sorted.tdate in purchase_sorted_date.keys():
                            purchase_sorted_date[purchase_sorted.tdate] = {"order_count" : 1, "price": purchase_sorted.purchasedprice, "total_products": purchase_sorted.total_products}
                        else:
                            purchase_sorted_date[purchase_sorted.tdate]["order_count"] += 1
                            purchase_sorted_date[purchase_sorted.tdate]["price"] += purchase_sorted.purchasedprice
                            purchase_sorted_date[purchase_sorted.tdate]["total_products"] += purchase_sorted.total_products
                    return render(request, 'admin_reports.html', {'table_data': purchase_sorted_date, 'heading': month})

                elif report_type == 'annual':
                    today_date = date.today()
                    year = today_date.year
                    purchases = Purchase.objects.filter(tdate__year = today_date.year)
                    purchase_sorted_tid = {}
                    for purchased in purchases:
                        if not purchased.tid in purchase_sorted_tid.keys():
                            purchase_sorted_tid[purchased.tid] = purchased
                            purchase_sorted_tid[purchased.tid].purchasedprice = purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products = 1
                        else:
                            purchase_sorted_tid[purchased.tid].purchasedprice += purchased.totalprice
                            purchase_sorted_tid[purchased.tid].total_products += 1
                    purchase_sorted_date = {}

                    for purchases, purchase_sorted in purchase_sorted_tid.items():
                        if not purchase_sorted.tdate in purchase_sorted_date.keys():
                            purchase_sorted_date[purchase_sorted.tdate] = {"order_count" : 1, "price": purchase_sorted.purchasedprice, "total_products": purchase_sorted.total_products}
                        else:
                            purchase_sorted_date[purchase_sorted.tdate]["order_count"] += 1
                            purchase_sorted_date[purchase_sorted.tdate]["price"] += purchase_sorted.purchasedprice
                            purchase_sorted_date[purchase_sorted.tdate]["total_products"] += purchase_sorted.total_products
                    return render(request, 'admin_reports.html', {'table_data': purchase_sorted_date, 'heading': year})      
        else:
            heading = 'Today'
            today_date = date.today()
            purchases = Purchase.objects.filter(tdate=today_date)
            purchase_sorted_tid = {}
            for purchased in purchases:
                if not purchased.tid in purchase_sorted_tid.keys():
                    purchase_sorted_tid[purchased.tid] = purchased
                    purchase_sorted_tid[purchased.tid].total_products = 1
                    purchase_sorted_tid[purchased.tid].purchasedprice = purchased.totalprice
                else:
                    purchase_sorted_tid[purchased.tid].total_products += 1
                    purchase_sorted_tid[purchased.tid].purchasedprice += purchased.totalprice
            purchase_sorted_date = {}

            for purchases, purchase_sorted in purchase_sorted_tid.items():
                if not purchase_sorted.tdate in purchase_sorted_date.keys():
                    purchase_sorted_date[purchase_sorted.tdate] = {"order_count" : 1, "price": purchase_sorted.purchasedprice, "total_products": purchase_sorted.total_products}
                else:
                    purchase_sorted_date[purchase_sorted.tdate]["order_count"] += 1
                    purchase_sorted_date[purchase_sorted.tdate]["price"] += purchase_sorted.purchasedprice
                    purchase_sorted_date[purchase_sorted.tdate]["total_products"] += purchase_sorted.total_products
            return render(request, 'admin_reports.html', {'table_data': purchase_sorted_date, 'heading': heading})
    
    else:
        return redirect(adminlogin)    

# def admin_sub_reports(request, status):
#     if status == 'Confirm':
#         purchases = Purchase.objects.filter(order_status= status)
#         purchase_sorted_tid = {}
#         for purchased in purchases:
#             if purchased.tid in purchases_tid.keys():
#                 purchase_sorted_tid [purchased.tid] = purchased
#                 purchase_sorted_tid [purchased.tid].purchasedprice = purchased.totalprice
#             else:
#                 purchase_sorted_tid [purchased.tid]. purchasedprice += purchased.totalprice
#         return render(request, 'admin_sub_reports.html', {'table_data' : purchase_sorted_tid, 'heading': status})
    
#     elif status == 'Cancelled':
#         purchases = Purchase.objects.filter(order_status=status)
#         purchase_sorted_tid = {}
#         for purchased in purchases:
#             if purchase.tid in purchase_tid.keys():
#                 purchase_sorted_tid [purchased.tid] = purchased
#                 purchase_sorted_tid [purchased.tid].purchasedprice = purchased.totalprice
#             else:
#                 purchase_sorted_tid[purchased.tid].purchasedprice += purchased.totalprice
#         return render(request, 'admin_sub_reports.html', {'table_data': purchase_sorted_tid, 'heading':status})
