from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path("building/<id>", login_required(views.building), name="building"),
    path('renter/<id>', login_required(views.renter), name='renter'),
    path('pending/<int:id>', login_required(views.pending), name='pending'),
    path('add-building', login_required(views.add_building), name='add-building'),
    path('add-room', login_required(views.add_room), name='add-room'),
    path('add-renter', login_required(views.add_renter), name='add-renter'),
    path('pay-rent/<int:id>', login_required(views.rent_pay), name='pay-rent'),
    path('bill/<int:id>', login_required(views.rent_bill_view), name='bill'),
    path('bill/download/<int:id>', login_required(views.rent_bill_download), name='bill_download'),
]
