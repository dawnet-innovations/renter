from datetime import datetime

import pdfkit
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy

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


def index(request):
    buildings = Building.objects.all()

    now = datetime.now()
    month_rents = Rent.objects.filter(date__month=now.month)
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
            "buildings": buildings,
            "renters": Renter.objects.all(),
            "total": total,
            "pending_count": pending_count,
            "monthly_total": monthly_total,
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
        "rooms": rooms,
        "renters": renters,
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
    context = {
        "renter": renter,
        "rents": rents,
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
        form.renter = renter
        amount_paid = form.cleaned_data["amount_paid"]
        if amount_paid != renter.rent:
            form.balance = renter.rent - amount_paid

        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("renter", kwargs={"id": id}))


def generate_bill(html_content):
    print(settings.BASE_DIR)
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOX_PATH)
    options = {
        'page-size': 'A4',  # Page size options: 'A4', 'Letter', etc.
        'margin-top': '10mm',  # Top margin
        'margin-right': '10mm',  # Right margin
        'margin-bottom': '10mm',  # Bottom margin
        'margin-left': '10mm',  # Left margin
    }
    pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)
    return pdf


def rent_bill_view(request, id):
    rent = Rent.objects.get(id=id)
    html_content = render_to_string("bill.html", {"rent": rent})
    bill = generate_bill(html_content)
    response = HttpResponse(bill, content_type='application/pdf')
    return response


def rent_bill_download(request, id):
    rent = Rent.objects.get(id=id)
    html_content = render_to_string("bill.html", {"rent": rent})
    bill = generate_bill(html_content)
    response = HttpResponse(bill, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rent_{rent.renter.name}.pdf"'
    return response


def pending(request, id):
    building = get_object_or_404(Building, id=id)
    rents = Rent.objects.all()
    pending = []
    for rent in rents:
        if not rent.is_paid():
            if not Rent.objects.filter(renter=rent.renter, date__month=rent.date.month, balance=0).exists():
                if rent.renter.room.building.id == building.id:
                    pending.append(rent)

    context = {
        "renters": [rent.renter for rent in pending],
    }
    return render(request, 'pending.html', context=context)
