# projects/views.py------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from .forms import InputProjectForm
from suppliers.forms import InputSupplierForm
from products.forms import InputProductForm
from supplier_products.forms import InputSupplier_ProductForm
from .models import Project
from django.urls import reverse
from products.models import Product
from receivings.models import Receiving
from receiving_suppliers.models import ReceivingSupplier
from suppliers.models import Supplier
from supplier_products.models import Supplier_Product
from django.http import HttpResponseRedirect
import pandas as pd
import openpyxl
from email.message import EmailMessage
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from datetime import datetime
from pathlib import Path
import os
from django.contrib.auth.decorators import login_required


def project_list(request):
    projects = Project.objects.all().order_by('-id')
    project_all_info = []

    for project in projects:
        project_info = {}
        supplier_info = {}
        supplier_product_info = {}  # Reset for each project

        # project.part_description -> receiving.part_number_formal -> product
        try:
            receiving = Receiving.objects.get(part_description__iexact=project.part_description)
            try:
                product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
                project_info = {
                    'project': project,
                    'receiving': receiving,
                    'product': product,
                }
            except Product.DoesNotExist:
                project_info = {
                    'project': project,
                    'receiving': receiving,
                }
                # input product
                return redirect(reverse('input_product') + '?part_number_formal=' + receiving.part_number_formal)

        except Receiving.DoesNotExist:
            project_info = {
                'project': project,
            }
            # input receiving
            return redirect(reverse('input_receiving') + '?part_description=' + project.part_description)

        # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
        try:
            receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
            try:
                supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
                supplier_info = {
                    'supplier': supplier,
                }
            except Supplier.DoesNotExist:
                pass
                supplier_info = {}
                # input supplier
                return redirect(reverse('input_supplier') + '?supplier_keyword=' + receiving_supplier.supplier_keyword)
        except ReceivingSupplier.DoesNotExist:
            pass
            supplier_info = {}
            # input receiving_supplier
            return redirect(reverse('input_receiving_supplier') + '?supplier_name=' + project.supplier_name)

        # Check if both supplier and product exist for this project
        if 'supplier' in supplier_info and 'product' in project_info:
            try:
                supplier_product = Supplier_Product.objects.get(
                    # supplier_keyword__iexact=supplier.supplier_keyword,
                    supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                    part_number_formal__iexact=project_info['product'].part_number_formal
                )
                supplier_product_info = {
                    'supplier_product': supplier_product,
                }
            except Supplier_Product.DoesNotExist:
                pass
                # input supplier_product
                return redirect(reverse('input_supplier_product') + '?supplier_keyword=' + supplier_info[
                    'supplier'].supplier_keyword + '&part_number_formal=' + project_info['product'].part_number_formal)

        # Append project information even if supplier_product_info is empty
        project_all_info.append({
            'project_info': project_info,
            'supplier_info': supplier_info,
            'supplier_product_info': supplier_product_info
        })

    context = {
        'projects': project_all_info,
        'list_name': 'ALL Projects List'
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def ongoing_project_list(request):

    projects = Project.objects.filter(project_parts_moved_pac_nc=False, project_inspector=request.user.username).order_by('-id')
    project_all_info = []

    for project in projects:
        project_info = {}
        supplier_info = {}
        supplier_product_info = {}  # Reset for each project

        # project.part_description -> receiving.part_number_formal -> product
        try:
            receiving = Receiving.objects.get(part_description__iexact=project.part_description)
            try:
                product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
                project_info = {
                    'project': project,
                    'receiving': receiving,
                    'product': product,
                }
            except Product.DoesNotExist:
                project_info = {
                    'project': project,
                    'receiving': receiving,
                }
                # input product
                return redirect(reverse('input_product') + '?part_number_formal=' + receiving.part_number_formal)

        except Receiving.DoesNotExist:
            project_info = {
                'project': project,
            }
            # input receiving
            return redirect(reverse('input_receiving') + '?part_description=' + project.part_description)

        # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
        try:
            receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
            try:
                supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
                supplier_info = {
                    'supplier': supplier,
                }
            except Supplier.DoesNotExist:
                pass
                supplier_info = {}
                # input supplier
                return redirect(reverse('input_supplier') + '?supplier_keyword=' + receiving_supplier.supplier_keyword)
        except ReceivingSupplier.DoesNotExist:
            pass
            supplier_info = {}
            # input receiving_supplier
            return redirect(reverse('input_receiving_supplier') + '?supplier_name=' + project.supplier_name)

        # Check if both supplier and product exist for this project
        if 'supplier' in supplier_info and 'product' in project_info:
            try:
                supplier_product = Supplier_Product.objects.get(
                    # supplier_keyword__iexact=supplier.supplier_keyword,
                    supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                    part_number_formal__iexact=project_info['product'].part_number_formal
                )
                supplier_product_info = {
                    'supplier_product': supplier_product,
                }
            except Supplier_Product.DoesNotExist:
                pass
                # input supplier_product
                return redirect(reverse('input_supplier_product') + '?supplier_keyword=' + supplier_info[
                    'supplier'].supplier_keyword + '&part_number_formal=' + project_info['product'].part_number_formal)

        # Append project information even if supplier_product_info is empty
        project_all_info.append({
            'project_info': project_info,
            'supplier_info': supplier_info,
            'supplier_product_info': supplier_product_info,
        })

    context = {
        'projects': project_all_info,
        'list_name': 'Ongoing Projects List'
    }
    return render(request, 'projects/project_list.html', context)


def single_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }

    return render(request, 'projects/project_list.html', {'projects': [project_data]})


# process_project_form is common code for input_project_view and input_project_initial_view
def process_project_form(request, template_name, initial_project=None):
    project_form = InputProjectForm()

    if request.method == 'POST':
        if 'project_form_submit' in request.POST:
            project_form = InputProjectForm(request.POST)
            if project_form.is_valid():
                project_form.save()
                return redirect('/')

    lot_num = request.GET.get('lot_num')

    if lot_num:
        project_form.initial['lot_num'] = lot_num

    project_inspector = request.GET.get('project_inspector')

    if project_inspector:
        project_form.initial['project_inspector'] = project_inspector

    if initial_project:
        project_form.instance = initial_project

    context = {
        'project_form': project_form,
        'project': initial_project,
    }

    return render(request, template_name, context)


def input_project_view(request):
    return process_project_form(request, 'projects/input_project.html')


def input_project_initial_view(request):
    project = Project()
    return process_project_form(request, 'projects/input_project_initial_part.html', initial_project=project)


def update_project_view(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")

    # input product information---start---------------------------
    product = get_object_or_404(Product, part_number_formal=product.part_number_formal)

    if request.method == 'POST':
        product_form = InputProductForm(request.POST, instance=product)
        if 'product_form_submit' in request.POST:
            if product_form.is_valid():
                product_form.save()
                return redirect('update_project', project_id=project_id)
        else:
            product_form = InputProductForm(instance=product)
    else:
        product_form = InputProductForm(instance=product)
    # input product---- end -----------------------------------------

    # input supplier information---start---------------------------
    supplier = get_object_or_404(Supplier, supplier_keyword=supplier.supplier_keyword)

    if request.method == 'POST':
        supplier_form = InputSupplierForm(request.POST, instance=supplier)
        if 'supplier_form_submit' in request.POST:
            if supplier_form.is_valid():
                supplier_form.save()
                return redirect('update_project', project_id=project_id)
        else:
            supplier_form = InputSupplierForm(instance=supplier)
    else:
        supplier_form = InputSupplierForm(instance=supplier)
    # input supplier---- end -----------------------------------------

    # input supplier_product information---start---------------------------
    supplier_product = get_object_or_404(Supplier_Product, supplier_keyword=supplier.supplier_keyword,
                                         part_number_formal=product.part_number_formal)

    if request.method == 'POST':
        supplier_product_form = InputSupplier_ProductForm(request.POST, instance=supplier_product)
        if 'supplier_product_form_submit' in request.POST:
            if supplier_product_form.is_valid():
                supplier_product_form.save()
                return redirect('update_project', project_id=project_id)
        else:
            supplier_product_form = InputSupplier_ProductForm(instance=supplier_product)
    else:
        supplier_product_form = InputSupplier_ProductForm(instance=supplier_product)
    # input supplier_product---- end -----------------------------------------
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
        'product_form': product_form,  # add this for input product information
        'supplier_form': supplier_form,  # add this for input product information
        'supplier_product_form': supplier_product_form,  # add this for input product information
    }

    return render(request, 'projects/update_project.html', context)


# import excel file data by lot number
@login_required
def input_new_project_by_lot_num_view(request):
    if request.user.is_authenticated:
        project_inspector = request.user.username

        if request.method == 'POST':
            lot_num = request.POST.get('lot_num')

            # Read the Excel file  attention: path user "/"  not "\"
            relative_path = 'data_files/Receiving_list_linked_with_Original.xlsx'
            excel_file = os.path.join(settings.BASE_DIR, relative_path)

            # excel_file = '/home/ThomasLi/008_WorkProject2028/data_files/Receiving_list_linked_with_Original.xlsx'  # Replace with your file path

            # excel_file = 'T:/Thomas_Li/008_WorkProject2028/Receiving_list/Receiving_list_linked_with_Original.xlsx'  # Replace with your file path

            try:
                df = pd.read_excel(excel_file, sheet_name='Sheet1')
                # Process the DataFrame or perform actions with the data
                # print(df.head())  # Just an example to show data loading
            except Exception as e:
                pass
                error_message = str(e)
                # return redirect('home')
                return redirect(
                    reverse('input_project_initial') + '?lot_num=' + lot_num + '&project_inspector=' + project_inspector)

            # Convert both user input and customer names from Excel to lowercase for case-insensitive comparison
            lot_num_lower = lot_num.lower()
            df['excel_lot_num_lower'] = df['LOT NUMBER'].str.lower()

            # Filter the DataFrame for the entered customer name (case-insensitive)
            project_data = df[df['excel_lot_num_lower'] == lot_num_lower]
            # print(f"Project data: {project_data}, ")

            if not project_data.empty:
                # Retrieve all the rows for the given customer name
                project_info = []
                for index, row in project_data.iterrows():
                    try:
                        original_lot_num = row['LOT NUMBER']
                        product_description = row['DESCRIPTION']
                        product_description_stripped = product_description.rstrip()
                        supplier_name = row['SUPPLIER NAME ']
                        received_date = row['RECEIVED DATE']
                        po_num = row['PO #']
                        qty = row['# of units Received']
                        location = row['Location'] if row['Location'] else 'STKTST'
                        # project_inspector = user_name
                    except Exception as e:
                        pass
                        error_message = str(e)
                        # return redirect('home')
                        return redirect(reverse('input_project_initial') + '?lot_num=' + lot_num + '&project_inspector=' + project_inspector)


                    # print(f"Lot number: {original_lot_num}, Product description: {product_description}")  # Debug print
                    project_info.append(
                        # (original_lot_num, product_description, supplier_name, received_date, po_num, qty, location, project_inspector))
                        (original_lot_num, product_description, supplier_name, received_date, po_num, qty, location))

                # Create or update the Customer model with the retrieved data
                # for original_lot_num, product_description, supplier_name, received_date, po_num, qty, location, project_inspector in project_info:
                for original_lot_num, product_description, supplier_name, received_date, po_num, qty, location in project_info:
                    project, created = Project.objects.get_or_create(
                        lot_num=original_lot_num,
                        # part_description=product_description,
                        part_description=product_description_stripped,
                        supplier_name=supplier_name,
                        received_date=received_date,
                        po_num=po_num,
                        qty=qty,
                        location=location,
                        # project_inspector=project_inspector,
                        project_inspector=request.user.username,
                    )
                return redirect('home')  # to be changed as need
            else:
                # print(lot_num)
                # return redirect('input_project')
                return redirect(
                    reverse('input_project_initial') + '?lot_num=' + lot_num + '&project_inspector=' + project_inspector)

        return render(request, 'projects/input_new_project_by_lot_num.html')
    else:
        return redirect('home')


def send_office365_email(subject, message, to_email):
    email = EmailMessage(subject, message, to=[to_email], from_email=settings.EMAIL_HOST_USER)
    email.send()


def send_email(request):
    subject = 'Test Email'
    message = 'This is a test email sent via Office 365 SMTP in Django.'
    to_email = 'Xiaogao.li@zimmerbiomet.com'  # Replace with the recipient's email

    send_office365_email(subject, message, to_email)

    # return render(request, 'email_sent.html')
    return HttpResponse('Email sent out.')


def send_custom_email(request):
    subject = 'try to send the mail from my app django'
    message = 'This is the body of the email: send this mail from django app, which i code it.'
    from_email = 'xiaogao.li.canada@gmail.com'
    recipient_list = ['xiaogao.li.canada@gmail.com']

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Email sent successfully!')

@login_required
def send_doc_check_email_view(request, subject, message, from_email, recipient_list):
    if request.method == 'POST':
        # Email sending logic
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Email sent successfully!')
    else:
        return HttpResponse('Invalid request method')


def update_project_to_ip_pdf_view(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
    }
    # send data to ip template ---------------------------------------------------

    # Path to the IP PDF template guideline file
    relative_path = 'data_files/IP_template_develop_guideline.pdf'
    default_pdf_path = os.path.join(settings.BASE_DIR, relative_path)

    # default_pdf_path = "/home/ThomasLi/008_WorkProject2028/data_files/IP_template_develop_guideline.pdf"
    # default_pdf_path = "T:/Thomas_Li/008_WorkProject2028/IP_template_fields/IP_template_develop_guideline.pdf"

    # # below 3 lines for input ip template path into model, however, webpage cannot read local files, obsolete
    # if supplier_product.supplier_product_ip_with_fields:
    #     pdf_template_path = supplier_product.supplier_product_ip_with_fields
    # else:

    relative_path = f'data_files/IP_{product.part_number_formal}{supplier_product.sps_part_reversion}_REV_{supplier_product.sps_ip_reversion}_Fields.pdf'
    pdf_template_path = os.path.join(settings.BASE_DIR, relative_path)

    # pdf_template_path = f'/home/ThomasLi/008_WorkProject2028/data_files/IP_{product.part_number_formal}{supplier_product.sps_part_reversion}_REV_{supplier_product.sps_ip_reversion}_Fields.pdf'
    # pdf_template_path = f'T:/Thomas_Li/008_WorkProject2028/IP_template_fields/IP_{product.part_number_formal}{supplier_product.sps_part_reversion}_REV_{supplier_product.sps_ip_reversion}_Fields.pdf'

    pdf_template_path = Path(pdf_template_path).resolve()

    try:
        reader = PdfReader(pdf_template_path)
    except FileNotFoundError:
        try:
            reader = PdfReader(default_pdf_path)
        except FileNotFoundError:
            return redirect('home')  # if the ip development guideline cannot be found,home

    # Create a writer object to modify the existing PDF
    writer = PdfWriter()

    # page = reader.pages[0]
    # fields = reader.get_fields()

    writer.append(reader)

    label_annex1_na_value = "N/A" if project.project_final_accept_qty == 0 else "see Annex 1"
    nc_qty_value = project.project_ncr_qty if project.project_ncr_qty else "0"
    ncr_num_value = 'NCR-' + project.project_ncr_num if project.project_ncr_num else "N/A"
    received_qty_3times = project.qty * 3
    received_qty_6times = project.qty * 6

    for page_number in range(len(reader.pages)):
        writer.update_page_form_field_values(
            writer.pages[page_number],
            {"lot_num": project.lot_num,
             "received_qty": project.qty,
             # "inspection_date": "03-Jan-2024",
             "inspection_date": datetime.now().strftime("%d-%b-%Y"),
             "ok_qty": project.project_final_accept_qty,
             "nc_qty": nc_qty_value,
             "ncr_num": ncr_num_value,
             "sign_date": datetime.now().strftime("%d-%b-%Y"),
             "label_annex1_na": label_annex1_na_value,
             "received_qty_3times": received_qty_3times,
             "received_qty_6times": received_qty_6times,
             },
        )

    # Create an in-memory buffer for the resulting PDF
    output_buffer = BytesIO()
    writer.write(output_buffer)

    # Content type header for PDF response
    response = HttpResponse(content_type='application/pdf')
    # define the file name as "IP_20-8020-002-00A_REV_B_preFilled.pdf"
    filename = f'IP_{product.part_number_formal}{supplier_product.sps_part_reversion}_REV_{supplier_product.sps_ip_reversion}_preFilled.pdf'
    # response['Content-Disposition'] = 'attachment; filename="Filled_IP.pdf"'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Write the PDF content to the response
    response.write(output_buffer.getvalue())
    output_buffer.close()

    return response
    # -------------------

    return render(request, 'projects/update_project.html', context)


@login_required
def update_project_to_dhr_review_annex_1_view(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
    }
    # send data to DHR review annex 1 template ---------------------------------------------------

    # Path to your PDF template file
    if project.project_final_accept_qty == 0:

        relative_path = 'data_files/DHR_REVIEW_All_NC.pdf'
        pdf_template_path = os.path.join(settings.BASE_DIR, relative_path)

        # # below line is ok for pycham
        # pdf_template_path = "T:/Thomas_Li/008_WorkProject2028/DHR_Review/DHR_REVIEW_All_NC.pdf"

        # # below line function ok for python anywhere
        # pdf_template_path = "/home/ThomasLi/008_WorkProject2028/data_files/DHR_REVIEW_All_NC.pdf"
    else:
        relative_path = 'data_files/DHR_REVIEW_Annex_Fields.pdf'
        pdf_template_path = os.path.join(settings.BASE_DIR, relative_path)

        # pdf_template_path = "T:/Thomas_Li/008_WorkProject2028/DHR_Review/DHR_REVIEW_Annex_Fields.pdf"
        # pdf_template_path = "/home/ThomasLi/008_WorkProject2028/data_files/DHR_REVIEW_Annex_Fields.pdf"
    try:
        reader = PdfReader(pdf_template_path)
    except FileNotFoundError:
        return redirect('home')

    # Create a writer object to modify the existing PDF
    writer = PdfWriter()

    # page = reader.pages[0]
    # fields = reader.get_fields()

    writer.append(reader)

    # calculation for fields value
    label_annex1_na_value = "N/A" if project.project_final_accept_qty == 0 else "see Annex 1"
    nc_qty_value = project.project_ncr_qty if project.project_ncr_qty else "0"
    ncr_num_value = 'NCR-' + project.project_ncr_num if project.project_ncr_num else "N/A"

    # avoid error, when part_reversion is null
    supplier_product.sps_part_reversion = supplier_product.sps_part_reversion if supplier_product.sps_part_reversion else "?"

    part_num_formal_reversion = product.part_number_formal + " / " + supplier_product.sps_part_reversion

    if project.project_po_reversion:
        po_num_reversion = project.project_po_number_only + " Rev. " + project.project_po_reversion
    else:
        po_num_reversion = project.project_po_number_only

    if project.project_ncr_num:
        qty_for_nc = f"{project.project_ncr_qty} for NCR-{project.project_ncr_num}"
        nc_original_location = project.location
        stknc_or_na = "STKNC"
        trf_or_na = "TRF"
    else:
        qty_for_nc = ""
        nc_original_location = "N/A"
        stknc_or_na = "N/A"
        trf_or_na = "N/A"

    # get user name from excel file user_inf.
    #     user_name = 'Thomas Li'

    verifier_name = request.user.username

    for page_number in range(len(reader.pages)):
        writer.update_page_form_field_values(
            writer.pages[page_number],
            {"part_num_formal_reversion": part_num_formal_reversion,
             "po_num_reversion": po_num_reversion,
             "lot_num": project.lot_num,
             "received_qty": project.qty,
             "release_num": project.project_release_num,
             "final_acc_qty": project.project_final_accept_qty,
             # "ncr_num": project.project_ncr_num,
             "qty_for_nc": qty_for_nc,
             "location": project.location,
             "stkpac": "STKPAC",
             "nc_original_location": nc_original_location,
             "stknc_or_na": stknc_or_na,
             "trf_or_na": trf_or_na,
             "label_printed_qty": project.project_final_accept_qty + 1,
             "ifu": product.part_ifu,
             "ifu_qty": project.project_final_accept_qty,
             "verifier": verifier_name,
             "label_date": datetime.now().strftime("%d-%b-%Y"),
             },
        )

    # Create an in-memory buffer for the resulting PDF
    output_buffer = BytesIO()
    writer.write(output_buffer)

    # Content type header for PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Filled_DHR_review_Annex.pdf"'

    # Write the PDF content to the response
    response.write(output_buffer.getvalue())
    output_buffer.close()

    return response
    # -------------------

    return render(request, 'projects/update_project.html', context)


@login_required
def update_project_view_send_mail(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
    }
    # send mail about doc checked result-----------------------------------------

    # get user_name and email address from excle file
    user_name = request.user.username
    # email_address = 'xiaogao.li@zimmerbiomet.com'
    email_address = request.user.email

    # Prepare data for sending email
    subject = asana_info + ' documentation check result'
    message = (f'Hello,'
               f'\n'''
               f'\n{asana_info} documentation has been checked and found: '
               f'\n'''
               f'\n{project.project_documentation_check_result}'
               f'\n'''
               f'\nCould you please check it and update the documentation?'
               f'\n'''
               f'\nThanks,'
               f'\n{user_name}'
               f'\nemail: {email_address}')
    from_email = email_address
    # recipient_list = ['xiaogao.li.canada@gmail.com']
    recipient_list = [supplier.supplier_contact_email]

    # Send the email
    if project.project_documentation_check_result:
        # Store data in session
        request.session['email_data'] = {
            'subject': subject,
            'message': message,
            'recipient_list': recipient_list,
            'cc': 'QCCAS-Team@zimmerbiomet.com',
            'from_email': from_email,
        }
        return redirect('send_email_form')  # Redirect to the email form


@login_required
def update_project_view_send_mail_trf_pac(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
    }
    # send mail about doc checked result-----------------------------------------
    # get user_name and email address from excle file
    user_name = request.user.username
    email_address = 'xiaogao.li@zimmerbiomet.com'

    # Prepare data for sending email
    release_info = (f"{supplier.supplier_keyword} / "
                    f"PN: {product.part_number_formal} / "
                    f"Lot: {project.lot_num} / "
                    f"Qty: {project.project_final_accept_qty} / "
                    f"{project.po_num} / "
                    f"Release-{project.project_release_num} "
                    )
    subject = 'TRF to PAC for ' + release_info
    message = (f'Hello Sourcing team,'
               f'\n'''
               f'\nBelow parts have been inspected and OK, could you please provide TRF: '
               f'\n'''
               f'\n{release_info}'
               f'\n'''
               f'\nfrom {project.location} to STKPAC?'
               f'\n'''
               f'\nThanks,'
               f'\n{user_name}')

    from_email = email_address
    recipient_list = ['SourcingCAS-Team@zimmerbiomet.com']

    # Send the email
    # Store data in session
    request.session['email_data'] = {
        'subject': subject,
        'message': message,
        'recipient_list': recipient_list,
        'cc': 'QCCAS-Team@zimmerbiomet.com',
        'from_email': from_email,
    }
    return redirect('send_email_form')  # Redirect to the email form


@login_required
def update_project_view_send_mail_trf_pro(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
    }
    # send mail about doc checked result-----------------------------------------
    # get user_name and email address from excle file
    excel_file1_path = "C:\\008_WorkProject2028\\User_information.xlsx"
    try:
        workbook1 = openpyxl.load_workbook(excel_file1_path)
        sheet_name1 = "Sheet1"
        sheet1 = workbook1[sheet_name1]
        user_name = sheet1['A2'].value
        email_address = sheet1['B2'].value
        email_password = sheet1['C2'].value
        workbook1.close()
    except FileNotFoundError:
        user_name = request.user.username
        email_address = 'xiaogao.li@zimmerbiomet.com'

    # Prepare data for sending email
    release_info = (f"{supplier.supplier_keyword} / "
                    f"PN: {product.part_number_formal} / "
                    f"Lot: {project.lot_num} / "
                    f"Qty: {project.project_final_accept_qty} / "
                    f"{project.po_num} / "
                    f"Release-{project.project_release_num} "
                    )
    subject = 'TRF to PRO for ' + release_info
    message = (f'Hello Sourcing team,'
               f'\n'''
               f'\nBelow DHR has been reviewed, could you please provide TRF: '
               f'\n'''
               f'\n{release_info}'
               f'\n'''
               f'\nfrom STKPAC to STKPRO?'
               f'\n'''
               f'\nThanks,'
               f'\n{user_name}')

    from_email = email_address
    # recipient_list = ['xiaogao.li.canada@gmail.com']
    recipient_list = ['SourcingCAS-Team@zimmerbiomet.com']

    # Send the email
    # Store data in session
    request.session['email_data'] = {
        'subject': subject,
        'message': message,
        'recipient_list': recipient_list,
        'cc': 'QCCAS-Team@zimmerbiomet.com',
        'from_email': from_email,
    }
    return redirect('send_email_form')  # Redirect to the email form


@login_required
def update_project_view_send_mail_trf_nc(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
    }
    # send mail about doc checked result-----------------------------------------
    # get user_name and email address from excle file

    user_name = request.user.username
    email_address = 'xiaogao.li@zimmerbiomet.com'

    # Prepare data for sending email
    release_info = (f"{supplier.supplier_keyword} / "
                    f"PN: {product.part_number_formal} / "
                    f"Lot: {project.lot_num} / "
                    f"Qty: {project.project_ncr_qty} / "
                    f"{project.po_num} / "
                    f"NCR-{project.project_ncr_num} "
                    )
    subject = 'TRF to STKNC for ' + release_info
    message = (f'Hello Sourcing team,'
               f'\n'''
               f'\nBelow NCR is opened, could you please provide TRF: '
               f'\n'''
               f'\n{release_info}'
               f'\n'''
               f'\nfrom {project.location} to STKNC?'
               f'\n'''
               f'\nThanks,'
               f'\n{user_name}')

    from_email = email_address
    # recipient_list = ['xiaogao.li.canada@gmail.com']
    recipient_list = ['SourcingCAS-Team@zimmerbiomet.com']

    # Send the email
    # Store data in session
    request.session['email_data'] = {
        'subject': subject,
        'message': message,
        'recipient_list': recipient_list,
        'cc': 'QCCAS-Team@zimmerbiomet.com',
        'from_email': from_email,
    }
    return redirect('send_email_form')  # Redirect to the email form


@login_required
def update_project_view_send_mail_ncr_notice(request, project_id):
    # update project data --------------------------------------------------------
    project = get_object_or_404(Project, id=project_id)
    form = InputProjectForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    project = get_object_or_404(Project, id=project_id)

    # Same data retrieval logic as in project_list view for this specific project
    project_info = {}
    supplier_info = {}
    supplier_product_info = {}

    # project.part_description -> receiving.part_number_formal -> product
    try:
        receiving = Receiving.objects.get(part_description__iexact=project.part_description)
        try:
            product = Product.objects.get(part_number_formal__iexact=receiving.part_number_formal)
            project_info = {
                'project': project,
                'receiving': receiving,
                'product': product,
            }
        except Product.DoesNotExist:
            project_info = {
                'project': project,
                'receiving': receiving,
            }
    except Receiving.DoesNotExist:
        project_info = {
            'project': project,
        }

    # project.supplier_name -> receiving_supplier.supplier_keyword -> supplier
    try:
        receiving_supplier = ReceivingSupplier.objects.get(supplier_name__iexact=project.supplier_name)
        try:
            supplier = Supplier.objects.get(supplier_keyword__iexact=receiving_supplier.supplier_keyword)
            supplier_info = {
                'supplier': supplier,
            }
        except Supplier.DoesNotExist:
            pass
            supplier_info = {}
    except ReceivingSupplier.DoesNotExist:
        pass
        supplier_info = {}

    # Check if both supplier and product exist for this project
    if 'supplier' in supplier_info and 'product' in project_info:
        try:
            supplier_product = Supplier_Product.objects.get(
                # supplier_keyword__iexact=supplier.supplier_keyword,
                supplier_keyword__iexact=supplier_info['supplier'].supplier_keyword,
                part_number_formal__iexact=project_info['product'].part_number_formal
            )
            supplier_product_info = {
                'supplier_product': supplier_product,
            }
        except Supplier_Product.DoesNotExist:
            pass

    # Prepare data to pass to the template
    project_data = {
        'project_info': project_info,
        'supplier_info': supplier_info,
        'supplier_product_info': supplier_product_info
    }
    asana_info = (f"{supplier.supplier_keyword} / "
                  f"PN: {product.part_number_formal} / "
                  f"Lot: {project.lot_num} / "
                  f"Qty: {project.qty} / "
                  f"{project.po_num}")
    context = {
        'form': form,
        'project': project,
        'projects': [project_data],
        'asana_info': asana_info,
    }
    # send mail about doc checked result-----------------------------------------
    # get user_name and email address from excle file

    user_name = request.user.username
    email_address = 'xiaogao.li@zimmerbiomet.com'

    # Prepare data for sending email
    release_info = (f"Notice of NCR-{project.project_ncr_num} ")
    subject = release_info
    message = (f'Hello,'
               f'\n'''
               f'\nPlease see attached Notice of NCR-{project.project_ncr_num}. '
               f'\n'''
               f'\nIf any, please feel free to contact with sarah.eltarazi@zimmerbiomet.com for following up this NCR.'
               f'\n'''
               f'\nThanks,'
               f'\n{user_name}')

    from_email = email_address
    # recipient_list = ['xiaogao.li.canada@gmail.com']
    recipient_list = [supplier.supplier_contact_email]

    # Send the email
    # Store data in session
    request.session['email_data'] = {
        'subject': subject,
        'message': message,
        'recipient_list': recipient_list,
        'cc': 'QCCAS-Team@zimmerbiomet.com; CAS-NC@zimmerbiomet.com',
        'from_email': from_email,
    }
    return redirect('send_email_form')  # Redirect to the email form


def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('/')

    context = {'project': project}
    return render(request, 'projects/delete_project.html', context)