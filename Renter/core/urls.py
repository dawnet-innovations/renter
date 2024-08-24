from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index),
    path("building/<id>",views.building,name="building"),
    path('renter/<id>',views.renter,name='renter'),
    path('pending',views.pending,name='pending'),
    path('add-building',views.add_building,name='add-building'),
    path('add-room',views.add_room,name='add-room'),
    path('add-renter',views.add_renter,name='add-renter'),
]
