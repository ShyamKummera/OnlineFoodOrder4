from django.contrib import admin
from django.urls import path

from vendor import views

urlpatterns = [
        path('',views.openLogin,name='vendor_main'),
    path('vendor_login_check/',views.vendor_login_check,name='vendor_login_check'),
    path('vendor_register/',views.vendor_register,name='vendor_register'),
    path('vendor_save/',views.vendor_save,name='vendor_save'),
    path('vendor_welcome/<int:pk>/',views.vendor_welcome,name='vendor_welcome'),
    path('vendor_logout/',views.vendor_login_check,name='vendor_logout'),
    path('vendor_foodtype/',views.vendor_foodtype,name='vendor_foodtype'),
    path('vendor_save_foodtype/',views.vendor_save_foodtype,name='vendor_save_foodtype'),
    path('vendor_food/',views.vendor_food,name='vendor_food'),
    path('vendor_save_food/',views.vendor_save_food,name='vendor_save_food'),
    path('vendor_customer_order/',views.vendor_customer_order,name='vendor_customer_order'),
]
