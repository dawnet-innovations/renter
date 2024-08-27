from django.forms import ModelForm

from .models import Renter, Room, Rent


class RenterForm(ModelForm):

    class Meta:
        model = Renter
        fields = "__all__"


class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = "__all__"


class RentForm(ModelForm):
    class Meta:
        model = Rent
        fields = "__all__"

