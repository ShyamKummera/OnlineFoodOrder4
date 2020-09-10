from django.contrib import messages
from django.shortcuts import render,redirect
from pwn.models import AdminLoginModel, StateModel, CityModel,CuisineModel
from vendor.models import VendorRegistrationModel
from pwn.otpsending import sendASMS

def showIndex(request):
    return render(request,"pwn/login.html")


def pwn_login_check(request):
    if request.method == "POST":
        try:
            admin = AdminLoginModel.objects.get(username=request.POST.get("pwn_username"),
                                                password=request.POST.get("pwn_password"))
            request.session["admin_status"] = True
            return redirect('welcome')
        except:
            return render(request, "pwn/login.html", {"error": "Invalid User"})
    else:
        request.session["admin_status"] = False
        return render(request, "pwn/login.html", {"error": "Admin Logout Success"})



def welcome(request):
    return render(request,"pwn/home.html")


def openState(request):
    sm = StateModel.objects.all()
    return render(request, "pwn/openstate.html", {'data': sm})

def savestate(request):
    StateModel(name=request.POST.get('t1'),photo=request.FILES['t2']).save()
    messages.success(request,'State is Saved')
    return openState(request)


def updatestate(request):
    sid = request.GET.get('id')
    print(sid)
    sm = StateModel.objects.get(id=sid)
    sm_all = StateModel.objects.all()
    return render(request,'pwn/openstate.html',{'udata':sm,'data': sm_all})


def updatestateid(request):
    StateModel.objects.filter(id=request.GET.get('sid')).update(name=request.POST.get('t1'),photo=request.FILES.get('t2'))
    return redirect('state')


def sdelete(request):
    StateModel.objects.filter(id=request.GET.get('sid')).delete()
    messages.success(request,'state deleted')
    return redirect('state')




def openCity(request):
    return render(request,"pwn/opencity.html",{"s_data":StateModel.objects.all(),"c_data":CityModel.objects.all()})


def savecity(request):
    CityModel(name=request.POST.get("c1"),photo=request.FILES['c2'],city_state_id=request.POST.get("c3")).save()
    return openCity(request)


def openCusine(request):
    return render(request,"pwn/opencuisine.html",{"c_data":CuisineModel.objects.all()})


def saveCusine(request):
    CuisineModel(type=request.POST.get("c1"),photo=request.FILES['c2']).save()
    return openCusine(request)


def openVendor(request):
    return render(request,"pwn/openvendor.html",{"pending":VendorRegistrationModel.objects.filter(status="pending"),"approved":VendorRegistrationModel.objects.filter(status="approved")})


def openReporsts(request):
    return render(request,"pwn/openreports.html")


def pwn_vendor_approve(request):
    res = VendorRegistrationModel.objects.get(id=request.GET.get("idno"))
    sname = res.stall_name
    cno = res.contact_1
    res.status = 'approved'
    res.save()
    sendASMS(str(cno),"Hello "+sname+"! \n We are happy to inform that your registration is approved by Admin")
    return openVendor(request)