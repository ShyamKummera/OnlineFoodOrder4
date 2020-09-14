from django.shortcuts import render
from customer.middleware import returnAddress

def showIndex(request):
    res = returnAddress()
    data = {"address":res[0],"city":res[1]}
    return render(request,"index.html",data)