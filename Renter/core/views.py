from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')

def building(request):
    return render(request,'building.html')

def renter(request):
    return render(request,'renter.html')

def pending(request):
    return render(request,'pending.html')