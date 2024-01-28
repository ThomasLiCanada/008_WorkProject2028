# projects/forms.py------------------------------------------------------------------------------
from django import forms
from .models import Supplier


class InputSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'