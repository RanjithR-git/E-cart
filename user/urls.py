from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('usersignup/',views.usersignup, name='usersignup'),
    path('userlogin/',views.userlogin, name='userlogin'),
    path('userregister/',views.userregister, name='userregister'),
    path('createuser/',views.createuser, name='createuser'),
    path('userlogout/',views.userlogout, name='userlogout'),
    
    
    path('add_to_cart/<int:id>/',views.add_to_cart, name='add_to_cart'),
    path('show_cart/',views.show_cart, name='show_cart'),
    path('view_product/',views.view_product, name='view_product'),
    path('delete_cart_item/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
    path('edit_cart/', views.edit_cart, name='edit_cart')
]