from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('usersignup/',views.usersignup, name='usersignup'),
    path('userlogin/',views.userlogin, name='userlogin'),
    path('userregister/',views.userregister, name='userregister'),
    path('createuser/',views.createuser, name='createuser'),
    
    
    path('login_with_otp/', views.login_with_otp, name='login_with_otp'),
    path('otp_generate/', views.otp_generate, name='otp_generate'),
    path('otp_validate/', views.otp_validate, name='otp_validate'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('userlogout/',views.userlogout, name='userlogout'),
    
    
    path('add_to_cart/<int:id>/',views.add_to_cart, name='add_to_cart'),
    path('show_cart/',views.show_cart, name='show_cart'),
    path('delete_cart_item/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
    path('edit_cart/', views.edit_cart, name='edit_cart'),


    path('create_address/', views.create_address, name='create_address'),
    path('show_address/', views.show_address, name='show_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    

    
    
    path('user_payment/<int:id>/', views.user_payment, name='user_payment'),
    path('paypal/', views.paypal, name= 'paypal'),
    path('razorpay/', views.razorpay, name='razorpay'),
    path('order_history/', views.order_history, name='order_history')
    
]