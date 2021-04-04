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

    path('create_product/',views.create_product, name='create_product'),
    path('show_product/',views.show_product, name='show_product')
]
