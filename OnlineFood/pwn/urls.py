
from django.urls import path

from pwn import views

urlpatterns = [

    path('',views.showIndex,name='pwn_main'),
    path('pwn_login_check/',views.pwn_login_check,name='pwn_login_check'),
    path('welcome/',views.welcome,name='welcome'),

    path('state/',views.openState,name='state'),
    path('savestate/',views.savestate,name='savestate'),
    path('updatestate/',views.updatestate,name='updatestate'),
    path('updatestateid/',views.updatestateid,name='updatestateid'),
    path('sdelete/',views.sdelete,name='sdelete'),

    path('city/',views.openCity,name='city'),
    path('savecity/',views.savecity,name='savecity'),


    path('cuisine/',views.openCusine,name='cuisine'),
    path('savecuisine/',views.saveCusine,name='savecuisine'),

    path('vendor/',views.openVendor,name='vendor'),
    path('pwn_vendor_approve/',views.pwn_vendor_approve,name='pwn_vendor_approve'),

    path('resports/',views.openReporsts,name='reports'),

    path('logout/',views.pwn_login_check,name='logout'),
]
