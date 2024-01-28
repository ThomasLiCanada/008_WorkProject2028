# supplier_products/views.py------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Supplier_Product
from .forms import InputSupplier_ProductForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def input_supplier_product_view(request):
    supplier_product_form = InputSupplier_ProductForm()

    if request.method == 'POST':
        if 'supplier_product_form_submit' in request.POST:
            supplier_product_form = InputSupplier_ProductForm(request.POST)
            if supplier_product_form.is_valid():
                supplier_product_form.save()
                return redirect('/')

    # Check if 'supplier_keyword' is passed in the URL (GET parameter)
    supplier_keyword = request.GET.get('supplier_keyword')

    # If 'supplier_keyword' is passed in the URL, pre-fill the form
    if supplier_keyword:
        supplier_product_form.initial['supplier_keyword'] = supplier_keyword

    # Check if 'part_number_formal' is passed in the URL (GET parameter)
    part_number_formal = request.GET.get('part_number_formal')

    # If 'part_number_formal' is passed in the URL, pre-fill the form
    if part_number_formal:
        supplier_product_form.initial['part_number_formal'] = part_number_formal

    context = {
        'supplier_product_form': supplier_product_form,
    }
    return render(request, 'supplier_products/input_supplier_product.html', context)


def update_supplier_product(request, supplier_keyword, part_number_formal):
    supplier_product = get_object_or_404(Supplier_Product, supplier_keyword=supplier_keyword,
                                         part_number_formal=part_number_formal)

    if request.method == 'POST':
        form = InputSupplier_ProductForm(request.POST, instance=supplier_product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = InputSupplier_ProductForm(instance=supplier_product)

    return render(request, 'supplier_products/input_supplier_product.html', {'supplier_product_form': form})
