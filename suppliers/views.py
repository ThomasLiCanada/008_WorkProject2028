# suppliers/views.py------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InputSupplierForm
from .models import Supplier


def input_supplier_view(request):
    supplier_form = InputSupplierForm()

    if request.method == 'POST':
        if 'supplier_form_submit' in request.POST:
            supplier_form = InputSupplierForm(request.POST)
            if supplier_form.is_valid():
                supplier_form.save()
                return redirect('/')
    # Check if 'supplier_keyword' is passed in the URL (GET parameter)
    supplier_keyword = request.GET.get('supplier_keyword')

    # If 'supplier_keyword' is passed in the URL, pre-fill the form
    if supplier_keyword:
        supplier_form.initial['supplier_keyword'] = supplier_keyword
    context = {
        'supplier_form': supplier_form,
    }

    return render(request, 'suppliers/input_supplier.html', context)


def update_supplier_by_keyword_view(request, supplier_keyword):
    supplier = get_object_or_404(Supplier, supplier_keyword=supplier_keyword)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        supplier_form = InputSupplierForm(request.POST, instance=supplier)
        if supplier_form.is_valid():
            supplier_form.save()  # Save the updated data
            return redirect('home')
    else:
        # If it's a GET request, create a form instance pre-filled with the supplier data
        supplier_form = InputSupplierForm(instance=supplier)

    context = {
        'supplier_form': supplier_form,
    }

    return render(request, 'suppliers/input_supplier.html', context)