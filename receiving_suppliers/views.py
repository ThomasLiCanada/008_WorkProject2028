# receiving_supplies/views.py------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from .forms import InputReceivingSupplierForm
from .models import ReceivingSupplier


def input_receiving_supplier_view(request):
    receiving_supplier_form = InputReceivingSupplierForm()

    if request.method == 'POST':
        if 'receiving_supplier_form_submit' in request.POST:
            receiving_supplier_form = InputReceivingSupplierForm(request.POST)
            if receiving_supplier_form.is_valid():
                receiving_supplier_form.save()
                return redirect('/')

    # Check if 'supplier_name' is passed in the URL (GET parameter)
    supplier_name = request.GET.get('supplier_name')

    # If 'supplier_name' is passed in the URL, pre-fill the form
    if supplier_name:
        receiving_supplier_form.initial['supplier_name'] = supplier_name

    context = {
        'receiving_supplier_form': receiving_supplier_form,
    }

    return render(request, 'receiving_suppliers/input_receiving_supplier.html', context)
