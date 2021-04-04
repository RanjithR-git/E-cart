from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.contrib import messages
from user.models import UserData
from . models import *
from . models import product, Categories
from django.core.files import File
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
        img = request.FILES.get('images')

        category_id= request.POST['category_id']
        product.objects.create(product_name=product_name,category_id=category_id,quantity=quantity,price=price,desc=desc,image=img)
        return redirect(show_product)
    else:
        category_id= Categories.objects.all()
        return render(request, 'admin_add_product.html',{'categories':category_id})


def show_product(request):
    if request.user.is_authenticated:
        products=product.objects.all()
        return render(request, 'create_product.html',{'product':products})
    else:
        return redirect(adminhome)
