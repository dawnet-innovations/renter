from django.shortcuts import render, redirect, get_object_or_404
from .models import Building, Renter, Room
from .forms import RenterForm, RoomForm

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
    
def building(request, id):
    building = get_object_or_404(Building, id=id)
    rooms = Room.objects.filter(building=building)
    context = {
        "building": building,
        "rooms": rooms,
    }
    return render(request, 'building.html', context=context)

def renter(request):
    return render(request, 'renter.html')

def pending(request):
    return render(request, 'pending.html')
