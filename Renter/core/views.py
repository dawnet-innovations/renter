from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import RenterForm, RoomForm, RentForm
from .models import Building, Renter, Room, Rent


def add_building(request):
    if request.method == "GET":
        return render(request, "add-building.html")

    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            Building.objects.create(name=name)
        return redirect("/")


def edit_building(request, id):
    building = get_object_or_404(Building, id=id)
    if request.method == "GET":
        return render(request, "add-building.html", context={"building": building})

    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            building.name = name
            building.save()
        return redirect("/")


def delete_building(request, id):
    building = get_object_or_404(Building, id=id)
    if request.method == "GET":
        building.delete()
        return redirect("/")


def index(request):
    buildings = Building.objects.all()

    now = datetime.now()
    month_rents = Rent.objects.filter(date__month=now.month, date__year=now.year)
    total = 0
    for rent in month_rents:
        total += rent.amount_paid

    rents = Rent.objects.all()
    pending_count = {building: 0 for building in buildings}
    monthly_total = {building: 0 for building in buildings}
    for rent in rents:
        monthly_total[rent.renter.room.building] += rent.amount_paid
        if not rent.is_paid():
            if not Rent.objects.filter(renter=rent.renter, date__month=rent.date.month, balance=0).exists():
                pending_count[rent.renter.room.building] += 1

    if request.method == "GET":
        context = {
            "buildings": buildings.order_by("-id"),
            "renters": Renter.objects.all().order_by("-id"),
            "total": total,
            "pending_count": pending_count,
            "monthly_total": monthly_total,
        }
        return render(request, "index.html", context=context)


def add_room(request):
    if request.method == "GET":
        context = {
            "buildings": Building.objects.all(),
        }
        return render(request, "add-room.html", context=context)

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            context = {
                "buildings": Building.objects.all().order_by("-id"),
            }
            return render(request, "add-room.html", context=context)


def edit_room(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == "GET":
        context = {
            "buildings": Building.objects.all(),
            "room": room,
        }
        return render(request, "add-room.html", context=context)

    if request.method == "POST":
        name = request.POST['name']
        room.name = name
        room.save()
        return redirect("/")


def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == "GET":
        room.delete()
        return redirect("/")


def add_renter(request):
    if request.method == "GET":
        context = {
            "buildings": Building.objects.all().order_by("-id"),
            "rooms": Room.objects.all().order_by("-id"),
        }
        return render(request, "add-renter.html", context=context)

    if request.method == "POST":
        form = RenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            context = {
                "buildings": Building.objects.all().order_by("-id"),
                "rooms": Room.objects.all().order_by("-id"),
            }
            return render(request, "add-renter.html", context=context)


def edit_renter(request, id):
    renter = get_object_or_404(Renter, id=id)
    if request.method == "GET":
        context = {
            "buildings": Building.objects.all().order_by("-id"),
            "rooms": Room.objects.all().order_by("-id"),
            "renter": renter,
        }
        return render(request, "add-renter.html", context=context)

    if request.method == "POST":
        form = RenterForm(request.POST, instance=renter)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            context = {
                "buildings": Building.objects.all().order_by("-id"),
                "rooms": Room.objects.all().order_by("-id"),
            }
            return render(request, "add-renter.html", context=context)


def delete_renter(request, id):
    renter = get_object_or_404(Renter, id=id)
    if request.method == "GET":
        renter.delete()
        return redirect("/")


def building(request, id):
    now = datetime.now()
    building = get_object_or_404(Building, id=id)
    rooms = Room.objects.filter(building=building)
    renters = Renter.objects.filter(room__in=rooms)
    rents = Rent.objects.filter(date__month=now.month)
    total = 0
    for rent in rents:
        if rent.renter.room.building.id == building.id:
            total += rent.amount_paid
    context = {
        "building": building,
        "rooms": rooms.order_by("-id"),
        "renters": renters.order_by("-id"),
        "total": total
    }
    return render(request, 'building.html', context=context)


def renter(request, id):
    renter = Renter.objects.get(id=id)
    rents = Rent.objects.filter(renter=renter).all()
    total_rent = 0
    for rent in rents:
        total_rent += rent.amount_paid
    due = 0
    for rent in rents:
        due += rent.balance
    duemc = 0
    if renter.agreement_start:
        for date in months_between(renter.agreement_start, renter.agreement_end):
            if datetime(day=date.day, month=date.month, year=date.year) <= datetime.now():
                rents = Rent.objects.filter(date__month=date.month, date__year=date.year, renter=renter)
                if not rents.exists():
                    duemc += 1
    if duemc != 0:
        due += duemc*renter.rent

    context = {
        "renter": renter,
        "rents": rents.order_by("-id"),
        "total_rent": total_rent,
        "due": due
    }
    return render(request, 'renter.html', context=context)


def rent_pay(request, id):
    renter = Renter.objects.get(id=id)
    if request.method == "GET":
        return render(request, "rent.html")

    if request.method == "POST":
        form = RentForm(request.POST)
        form.instance.renter = renter

        print(form.errors)
        if form.is_valid():
            amount_paid = form.cleaned_data["amount_paid"]
            if amount_paid != renter.rent:
                form.balance = renter.rent - amount_paid
            form.save()
            return redirect(reverse_lazy("renter", kwargs={"id": id}))


def edit_pay(request, id):
    rent = Rent.objects.get(id=id)
    if request.method == "GET":
        return render(request, "rent.html", context={"rent": rent})

    if request.method == "POST":
        amount_paid = request.POST["amount_paid"]
        rent.amount_paid = amount_paid
        if amount_paid != rent.renter.rent:
            rent.balance = float(rent.renter.rent) - float(amount_paid)
        rent.save()
        return redirect(reverse_lazy("renter", kwargs={"id": rent.renter.id}))


def bill(request, id):
    rent = Rent.objects.get(id=id)
    if request.method == "GET":
        return render(request, "bill.html", {"rent": rent})


def months_between(start, end):
    current_date = start
    while current_date <= end:
        yield current_date
        current_date += relativedelta(months=1)


def pending(request, id):
    building = get_object_or_404(Building, id=id)
    now = datetime.now()
    renters = Renter.objects.filter(room__building=building)

    pending_rents = []
    if renter.agreement_start:
        for renter in renters:
            for date in months_between(renter.agreement_start, renter.agreement_end):
                if datetime(day=date.day, month=date.month, year=date.year) <= now:
                    rents = Rent.objects.filter(date__month=date.month, date__year=date.year, renter=renter)
                    if rents.exists():
                        for rent in rents:
                            if not rent.is_paid():
                                if not Rent.objects.filter(renter=rent.renter, date__month=rent.date.month,
                                                           date__year=rent.date.year,
                                                           balance=0).exists():
                                    if renter not in pending_rents:
                                        pending_rents.append(renter)
                    else:
                        if renter not in pending_rents:
                            pending_rents.append(renter)

    context = {
        "renters": pending_rents,
    }
    return render(request, 'pending.html', context=context)


def renter_pendings(request, id):
    now = datetime.now()
    renter = Renter.objects.get(id=id)

    pending_rents = []
    monthly_rent = []
    if renter.agreement_start:
        for date in months_between(renter.agreement_start, renter.agreement_end):
            if datetime(day=date.day, month=date.month, year=date.year) <= now:
                rents = Rent.objects.filter(date__month=date.month, date__year=date.year, renter=renter)
                if rents.exists():
                    for rent in rents:
                        if not rent.is_paid():
                            if not Rent.objects.filter(renter=rent.renter, date__month=rent.date.month, date__year=rent.date.year,
                                                       balance=0).exists():
                                pending_rents.append(rent)
                else:
                    monthly_rent.append(date)

    context = {"rents": pending_rents, "rentfee": renter.rent, "monthly_rent": monthly_rent}

    return render(request, 'renter_pending.html', context=context)
