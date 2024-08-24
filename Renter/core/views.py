from django.shortcuts import render, redirect, get_object_or_404
from .models import Building, Renter, Room, Rent
from .forms import RenterForm, RoomForm

def add_building(request):
    if request.method == "GET":
        return render(request, "add-building.html")

    if request.method == "POST":
        name = request.POST.get("name")
        
        if name:
            Building.objects.create(name=name)
        return redirect("/")

def index(request):
    if request.method == "GET":
        context = {
            "buildings": Building.objects.all()
        }
        return render(request, "index.html", context=context)

def add_room(request):
    if request.method == "GET":
        context = {
            "buildings": Building.objects.all()
        }
        return render(request, "add-room.html", context=context)
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            context = {
                "buildings": Building.objects.all(),
                "form": form
            }
            return render(request, "add-room.html", context=context)

def add_renter(request):
    if request.method == "GET":
        context = {
            "buildings": Building.objects.all(),
            "rooms": Room.objects.all(),
        }
        return render(request, "add-renter.html", context=context)
    
    if request.method == "POST":
        form = RenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            context = {
                "buildings": Building.objects.all(),
                "rooms": Room.objects.all(),
                "form": form
            }
            return render(request, "add-renter.html", context=context)

def building(request, id):
    building = get_object_or_404(Building, id=id)
    rooms = Room.objects.filter(building=building)
    renters = Renter.objects.filter(room__in=rooms)
    context = {
        "building": building,
        "rooms": rooms,
        "renters": renters,
    }
    return render(request, 'building.html', context=context)

def renter(request, id):
    renter = Renter.objects.get(id=id)
    rents = Rent.objects.filter(renter=renter).all()
    context = {
        "renter": renter,
        "rent": rents,
    }
    return render(request, 'renter.html', context=context)

def pending(request):
    return render(request, 'pending.html')
