from django.core.paginator import Paginator
from django.shortcuts import render, redirect
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
        i_id = request.POST.get("item")

    else:
        return redirect('customer_login')


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
        return render(request,"customer/welcome.html")
    except CustomerRegistrationModel.DoesNotExist:
        return render(request,"customer/otp.html",{"contactNo":request.POST.get("cno"),"message":"Invalid OTP"})


def customer_login(request):
    return render(request,"customer/login.html")


def customer_login_check(request):
    if request.method == "POST":
        cno = request.POST.get("c1")
        pa = request.POST.get("c2")
        try:
            res = CustomerRegistrationModel.objects.get(contact=cno, password=pa)
            request.session["customer_status"] = True
            request.session["customer_id"] = res.id
            return redirect('customer_welcome', pk=res.id)
        except CustomerRegistrationModel.DoesNotExist:
            return render(request, 'customer/login.html', {"error": "Invalid User"})

    else:
        request.session["customer_status"] = False
        return render(request, "customer/login.html", {"error": "Customer Logout Success"})


def customer_welcome(request,pk):
    request.session["vendor_id"] = pk
    customer_details = CustomerRegistrationModel.objects.get(id=pk)
    return render(request, "customer/home.html", {"customer_details": customer_details})


def customer_menu(request):

    customer_details = CustomerRegistrationModel.objects.get(id=request.session["customer_id"])

    res = returnAddress()
    page_no = request.GET.get("pageno", 1)
    data = FoodItemsModel.objects.all()
    p = Paginator(data, 3)
    if page_no:
        page = p.page(page_no)
    else:
        page = p.page(1)

    return render(request,"customer/menu.html",{"customer_details": customer_details,"address":res[0], "city":res[1], "food":page})