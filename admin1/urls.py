from django.urls import path

from . import views

urlpatterns = [
    path('',views.adminlogin, name='adminlogin'),
    path('adminhome/',views.adminhome, name='adminhome'),
    path('usertable/',views.usertable, name='usertable'),
    path('adduser/',views.adduser, name='adduser'),


    # path('adminedit/<int:id>/',views.adminedit, name='adminedit'),
    # path('admindelete/<int:id>/',views.admindelete, name='admindelete'),
    path('adminlogout/',views.adminlogout, name='adminlogout'),
    path('user_block/<int:id>',views.user_block, name='user_block'),


    path('add_category/',views.add_category, name='add_category'),
    path('view_category/',views.view_category, name='view_category'),
    path('edit_category/<int:id>/',views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/',views.delete_category, name='delete_category'),

    path('create_product/', views.create_product, name='create_product'),
    path('show_product/', views.show_product, name='show_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),

    path('admin_orders/',views.admin_orders, name='admin_orders'),
    path('admin_sub_orders/<str:status>', views.admin_sub_orders, name='admin_sub_orders'),
    path('cancel_order/<str:tid>', views.cancel_order, name='cancel_order'),
    path('confirm_order/<str:tid>', views.confirm_order, name='confirm_order'),
    
    
    path('admin_reports/', views.admin_reports, name='admin_reports'),
    path('admin_sub_reports/<str:status>', views.admin_sub_reports, name='admin_sub_reports'),
    path('add_coupon/', views.add_coupon, name = 'add_coupon'),
    path('view_offer/', views.view_offer, name= 'viwe_offer'),
    path('delete_coupon/', views.delete_coupon, name='delete_coupon'),
    path('add_offer/', views.add_offer, name='add_offer'),
    path('delete_offer/<int:id>/', views.delete_offer, name='delete_offer')

]
