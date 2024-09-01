from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [

    path('', login_required(views.index), name='index'),
    path("building/<id>", login_required(views.building), name="building"),
    path('renter/<id>', login_required(views.renter), name='renter'),
    path('pending/<int:id>', login_required(views.pending), name='pending'),
    path('renter/pending/<int:id>', login_required(views.renter_pendings), name='renter_pending'),
    path('add-building', login_required(views.add_building), name='add-building'),
    path('edit-building/<int:id>', login_required(views.edit_building), name='edit-building'),
    path('delete-building/<int:id>', login_required(views.delete_building), name='delete-building'),
    path('add-room', login_required(views.add_room), name='add-room'),
    path('edit-room/<int:id>', login_required(views.edit_room), name='edit-room'),
    path('delete-room/<int:id>', login_required(views.delete_room), name='delete-room'),
    path('add-renter', login_required(views.add_renter), name='add-renter'),
    path('edit-renter/<int:id>', login_required(views.edit_renter), name='edit-renter'),
    path('delete-renter/<int:id>', login_required(views.delete_renter), name='delete-renter'),
    path('pay-rent/<int:id>', login_required(views.rent_pay), name='pay-rent'),
    path('edit-rent/<int:id>', login_required(views.edit_pay), name='edit-rent'),
    path('delete-rent/<int:id>', login_required(views.delete_rent), name='delete-rent'),
    path('bill/<int:id>', login_required(views.bill), name='bill'),
]
