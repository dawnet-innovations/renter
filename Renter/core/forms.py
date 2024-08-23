from django.forms import ModelForm

from .models import Renter


class RenterForm(ModelForm):

    class Meta:
        model = Renter
        fields = "__all__"
