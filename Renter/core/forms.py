from django.forms import ModelForm

from .models import Renter,Room


class RenterForm(ModelForm):

    class Meta:
        model = Renter
        fields = "__all__"


class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = "__all__"
