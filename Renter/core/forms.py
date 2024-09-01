from django.forms import ModelForm

from .models import Renter, Room, Rent


class RenterForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RenterForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['whatsapp'].required = False
        self.fields['agreement_start'].required = False
        self.fields['agreement_end'].required = False

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
        fields = ("amount_paid", "pay_for")

