# products/forms.py------------------------------------------------------------------------------
from django import forms
from .models import Product


class InputProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'