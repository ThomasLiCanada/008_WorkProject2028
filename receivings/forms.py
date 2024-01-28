# receivings/forms.py------------------------------------------------------------------------------
from django import forms
from .models import Receiving


class InputReceivingForm(forms.ModelForm):
    class Meta:
        model = Receiving
        fields = '__all__'