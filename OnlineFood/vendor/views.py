from django.shortcuts import render,redirect
from vendor.models import VendorRegistrationModel,FoodTypeModel,FoodItemsModel
from pwn.models import CuisineModel,CityModel
from django.contrib import messages
from customer.models import CartItemModel

def openLogin(request):
    return render(request,"vendor/login.html")


def vendor_login_check(request):
    if request.method == "POST":
        try:
            vendor_res = VendorRegistrationModel.objects.get(contact_1=request.POST.get("vendor_username"),
                                                password=request.POST.get("vendor_password"),status='approved')
            request.session["vendor_status"] = True
            request.session["vendor_id"] = vendor_res.id
            return redirect('vendor_welcome',pk=vendor_res.id)
        except:
            return render(request, "vendor/login.html", {"error": "Invalid User"})
    else:
        request.session["vendor_status"] = False
        return render(request, "vendor/login.html", {"error": "Vendor Logout Success"})


def vendor_register(request):
    return render(request,"vendor/vendor_register.html",{"cuisine":CuisineModel.objects.all(),"city":CityModel.objects.all()})


def vendor_save(request):
    sn = request.POST.get("v1")
    c1 = request.POST.get("v2")
    c2 = request.POST.get("v3")
    cui = request.POST.get("v4")
    ph = request.FILES["v5"]
    add = request.POST.get("v6")
    cty = request.POST.get("v7")
    pas = request.POST.get("v8")
    otp = 0000
    sta = "pending"
    VendorRegistrationModel(stall_name=sn,contact_1=c1,contact_2=c2,cuisine_type_id=cui,photo=ph,address=add,vendor_city_id=cty,password=pas,OTP=otp,status=sta).save()
    messages.success(request,"Registration is Done, Need Approval from Admin")
    return redirect('vendor_main')


def vendor_welcome(request,pk):
    request.session["vendor_id"] = pk
    vendor_details = VendorRegistrationModel.objects.get(id=pk)
    return render(request,"vendor/home.html",{"vendor_details":vendor_details})


def vendor_foodtype(request):
    vendor_details = VendorRegistrationModel.objects.get(id=request.session["vendor_id"])
    return render(request,"vendor/foodtype.html",{"vendor_details":vendor_details,"food_type":FoodTypeModel.objects.filter(vendor_id_id=request.session["vendor_id"])})


def vendor_save_foodtype(request):
    FoodTypeModel(name=request.POST.get("f1"),vendor_id_id=request.session["vendor_id"],status=request.POST.get("f2")).save()
    return vendor_foodtype(request)


def vendor_food(request):
    vendor_details = VendorRegistrationModel.objects.get(id=request.session["vendor_id"])
    return render(request, "vendor/food.html", {"vendor_details": vendor_details,"food_type":FoodTypeModel.objects.filter(vendor_id_id=request.session["vendor_id"]),"food":FoodItemsModel.objects.filter(food_type__vendor_id=request.session["vendor_id"])})


def vendor_save_food(request):
    FoodItemsModel(name=request.POST.get("f1"),food_type_id=request.POST.get("f2"),price=request.POST.get("f3"),photo=request.FILES["f4"]).save()
    return vendor_food(request)


def vendor_customer_order(request):

    v_id = request.session["vendor_id"]

    res = CartItemModel.objects.filter(status='order',food__food_type__vendor_id=v_id)

    return render(request,"vendor/customer_orders.html",{"data":res})