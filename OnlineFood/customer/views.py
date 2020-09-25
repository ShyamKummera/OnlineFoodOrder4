from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from customer.middleware import returnAddress
from vendor.models import FoodItemsModel
from pwn.models import CityModel
from customer.models import CustomerRegistrationModel,CartItemModel,OrderModel
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


def add_to_cart(request):
    if request.session['customer_status']:
        i_id = request.POST.get("item")
        food = FoodItemsModel.objects.get(id=i_id)
        total = food.price
        return render(request,"customer/addcart.html",{"food":food,"count":1,"total":total})
    else:
        return redirect('customer_login')

count = 0
total = 0
def customer_quantity(request):
    _b = request.POST.get("b1")
    price = float(request.POST.get("price"))
    global count,total
    if _b == '+':
        count+=1
        total = price * count
    else:
        if count > 0:
            count-=1
            total = price * count

    i_id = request.POST.get("item")
    food = FoodItemsModel.objects.get(id=i_id)
    return render(request, "customer/addcart.html", {"food": food,"count":count,"total":total})


def customer_save_to_cart(request):
    i_id = request.POST.get("i_id")
    count = request.POST.get("count")
    c_id = request.session["customer_id"]
    CartItemModel(customer_id=c_id,food_id=i_id,quantity=count,status='active').save()
    return redirect('customer_menu')


def customer_cart_items(request):
    c_id = request.session["customer_id"]
    cart_items = CartItemModel.objects.filter(customer_id=c_id,status='active')
    return render(request,"customer/cart_items.html",{"cart_items":cart_items})


def customer_order(request):
    address = request.POST.get("address")
    total = request.POST.get("total")
    c_id = request.session["customer_id"]
    OrderModel(c_id_id=c_id,address=address,total=total).save()
    CartItemModel.objects.filter(customer_id=c_id).update(status='order')
    return redirect('customer_order_placed')


def customer_order_placed(request):
    c_id = request.session["customer_id"]
    cart_items = CartItemModel.objects.filter(customer_id=c_id, status='order')
    return render(request,"customer/orders.html",{"cart_items":cart_items})