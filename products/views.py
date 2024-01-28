# products/views.py------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InputProductForm
from .models import Product
from django.http import HttpResponse
import pandas as pd
import os


def input_product_view(request):
    product_form = InputProductForm()

    if request.method == 'POST':
        if 'product_form_submit' in request.POST:
            product_form = InputProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                return redirect('/')
    # Check if 'lot_num' is passed in the URL (GET parameter)
    part_number_formal = request.GET.get('part_number_formal')

    # If 'lot_num' is passed in the URL, pre-fill the form
    if part_number_formal:
        product_form.initial['part_number_formal'] = part_number_formal

    context = {
        'product_form': product_form,
    }

    return render(request, 'products/input_product.html', context)


def update_product_by_part_number_view(request, part_number_formal):
    product = get_object_or_404(Product, part_number_formal=part_number_formal)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        product_form = InputProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()  # Save the updated data
            return redirect('home')
    else:
        # If it's a GET request, create a form instance pre-filled with the product data
        product_form = InputProductForm(instance=product)

    context = {
        'product_form': product_form,
    }

    return render(request, 'products/input_product.html', context)


def export_products_to_excel(request):
    # Get all products from the database
    products = Product.objects.all()

    # Create a DataFrame from the queryset
    data = {
        'part_number_formal': [product.part_number_formal for product in products],
        'part_inf': [product.part_inf for product in products],
        'part_number_no_dash': [product.part_number_no_dash for product in products],
        'part_name_official': [product.part_name_official for product in products],
        'part_dmr': [product.part_dmr for product in products],
        'part_gtin_number': [product.part_gtin_number for product in products],
        'part_special_test': [product.part_special_test for product in products],
        'part_ifu': [product.part_ifu for product in products],
        'part_product_file': [product.part_product_file for product in products],
        'part_edhr': [product.part_edhr for product in products],
    }
    df = pd.DataFrame(data)

    # Create a temporary file path
    temp_file_path = os.path.join('C:\\try\\', 'product.xlsx')

    # Save the DataFrame to Excel
    df.to_excel(temp_file_path, index=False, sheet_name='Products')

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    # Write the file content to the response
    with open(temp_file_path, 'rb') as file:
        response.write(file.read())

    # Delete the temporary file
    os.remove(temp_file_path)

    return response


def import_products_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            # Load the Excel file into a pandas DataFrame
            df = pd.read_excel(excel_file)

            # Iterate through rows and create/update Product instances
            for index, row in df.iterrows():
                part_number_formal = row['part_number_formal']
                part_inf = row['part_inf']
                part_number_no_dash = row['part_number_no_dash']
                part_name_official = row['part_name_official']
                part_dmr = row['part_dmr']
                part_gtin_number = row['part_gtin_number']
                part_special_test = row['part_special_test']
                part_ifu = row['part_ifu']
                part_product_file = row['part_product_file']
                part_edhr = row['part_edhr']

                # Check if the record already exists based on part_number_formal
                product, created = Product.objects.get_or_create(
                    part_number_formal=part_number_formal,
                    defaults={
                        'part_inf': part_inf,
                        'part_number_no_dash': part_number_no_dash,
                        'part_name_official': part_name_official,
                        'part_dmr': part_dmr,
                        'part_gtin_number': part_gtin_number,
                        'part_special_test': part_special_test,
                        'part_ifu': part_ifu,
                        'part_product_file': part_product_file,
                        'part_edhr': part_edhr,
                    }
                )

                # If the record already exists, update the fields
                if not created:
                    product.part_inf = part_inf
                    product.part_number_no_dash = part_number_no_dash
                    product.part_name_official = part_name_official
                    product.part_dmr = part_dmr
                    product.part_gtin_number = part_gtin_number
                    product.part_special_test = part_special_test
                    product.part_ifu = part_ifu
                    product.part_product_file = part_product_file
                    product.part_edhr = part_edhr
                    product.save()

            return HttpResponse("Import successful!")
        except Exception as e:
            return HttpResponse(f"Import failed. Error: {str(e)}")

    return render(request, 'products/import_excel.html')






