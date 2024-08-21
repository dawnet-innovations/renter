from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Building

# Create your views here.

def add_building(request):
    if request.method == "GET":
        return render(request, "add-building.html")

    if request.method == "POST":
        name = request.POST.get("name")
        
        building = Building(name=name)
        building.save()
        
        return redirect("/")

def index(request):
    if request.method == "GET":
        context = {
            "building": Building.objects.all()
        }
        return render(request, "index.html", context=context)


def add_renter(request):
    return render(request,'add-renter.html')

def building(request):
    return render(request,'building.html')

def renter(request):
    return render(request,'renter.html')

def pending(request):
    return render(request,'pending.html')


