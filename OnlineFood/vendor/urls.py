from django.contrib import admin
from django.urls import path

from vendor import views

urlpatterns = [
        path('',views.openLogin,name='vendor_main'),
    path('vendor_login_check/',views.vendor_login_check,name='vendor_login_check'),
    path('vendor_register/',views.vendor_register,name='vendor_register'),
    path('vendor_save/',views.vendor_save,name='vendor_save'),
    path('vendor_welcome/',views.vendor_welcome,name='vendor_welcome'),
]
