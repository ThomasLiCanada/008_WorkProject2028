# supplier_products/forms.py------------------------------------------------------------------------------
from django import forms
from .models import Supplier_Product


class InputSupplier_ProductForm(forms.ModelForm):
    class Meta:
        model = Supplier_Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sps_part_reversion'].widget.attrs['placeholder'] = 'Part Reversion ...'
        self.fields['sps_ip_reversion'].widget.attrs['placeholder'] = 'IP Reversion ...'
        self.fields['sps_pn_supplier_edhr'].widget.attrs['placeholder'] = 'Part_Number/Supplier/eDHR ... (https://livelink.nam.zimmer.com/livelink/livelink.exe?... ...)'