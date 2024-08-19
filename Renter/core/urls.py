from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index),
    path('building',views.building),
    path('renter',views.renter),
    path('pending',views.pending),
]
