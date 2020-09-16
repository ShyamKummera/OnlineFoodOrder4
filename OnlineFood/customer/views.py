from django.core.paginator import Paginator
from django.shortcuts import render
from customer.middleware import returnAddress
from vendor.models import FoodItemsModel
from pwn.models import CityModel
from customer.models import CustomerRegistrationModel
import random
from pwn.otpsending import sendASMS

def showIndex(request):
    res = returnAddress()
    page_no = request.GET.get("pageno",1)
    data = FoodItemsModel.objects.all()
    p = Paginator(data, 3)
    if page_no:
        page = p.page(page_no)
    else:
        page = p.page(1)
    return render(request, "customer/index.html", {"address":res[0], "city":res[1], "food":page})


def add_to_cart(request):
    if request.session['customer_status']:
        pass
    else:
        pass


def customer_register(request):
    return render(request,"customer/register.html",{"city":CityModel.objects.all()})


def customer_save(request):
    name = request.POST.get("c1")
    contact = request.POST.get("c2")
    address = request.POST.get("c3")
    city = request.POST.get("c4")
    password = request.POST.get("c5")

    otp = random.randint(100000,999999)

    message = "Hello "+name+", Welcome to Online Food Order \n To complete Your Registration Use this OTP "+str(otp)

    print(message)

    sendASMS(contact,message)

    CustomerRegistrationModel(name=name,contact=contact,address=address,city_id=city,password=password,OTP=otp).save()

    return render(request,"customer/otp.html",{"contactNo":contact})


def customer_check_otp(request):
    try:
        CustomerRegistrationModel.objects.get(contact=request.POST.get("cno"),OTP=request.POST.get("otp"))
        return render(request,"customer/login.html")
    except CustomerRegistrationModel.DoesNotExist:
        return render(request,"customer/otp.html",{"contactNo":request.POST.get("cno"),"message":"Invalid OTP"})