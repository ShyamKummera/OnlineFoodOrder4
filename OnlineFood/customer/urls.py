

from django.contrib import admin
from django.urls import path

from customer import views

urlpatterns = [
    path('',views.showIndex,name='index'),
    path('customer_register/',views.customer_register,name='customer_register'),
    path('customer_save/',views.customer_save,name='customer_save'),
    path('customer_check_otp/',views.customer_check_otp,name='customer_check_otp'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),

]
