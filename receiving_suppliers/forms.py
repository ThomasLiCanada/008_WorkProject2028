# receiving_suppliers/forms.py------------------------------------------------------------------------------
from django import forms
from .models import ReceivingSupplier


class InputReceivingSupplierForm(forms.ModelForm):
    class Meta:
        model = ReceivingSupplier
        fields = '__all__'