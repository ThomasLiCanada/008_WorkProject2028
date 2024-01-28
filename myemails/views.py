# myemails/views.py
from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import FileUploadForm
from django.core.mail import get_connection
import openpyxl


def send_email_with_attachment(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            selected_files = request.FILES.getlist('files')

            # Splitting multiple email addresses by semicolon
            recipients = form.cleaned_data['recipient'].split(';')

            email = EmailMessage(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                'xiaogao.li.canada@gmail.com',
                recipients,
                cc=[form.cleaned_data['cc']] if form.cleaned_data['cc'] else None  # Add CC if it exists
            )

            for selected_file in selected_files:
                email.attach(selected_file.name, selected_file.read(), selected_file.content_type)

            email.send()
            return render(request, 'myemails/send_mail_success.html')
    else:
        form = FileUploadForm()

    return render(request, 'myemails/send_mail_web.html', {'form': form})


def send_email_form(request):
    # Retrieve data from session
    email_data = request.session.get('email_data')

    if email_data:
        initial_data = {
            'subject': email_data['subject'],
            'content': email_data['message'],
            'recipient': email_data['recipient_list'][0],  # Assuming a single recipient for simplicity
            'cc': email_data['cc'],
            'from_email': email_data['from_email'],
        }
        form = FileUploadForm(initial=initial_data)
    else:
        form = FileUploadForm()

    # send mail (same as "send_email_with_attachment".views)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                selected_files = request.FILES.getlist('files')

                # Splitting multiple email addresses by semicolon
                recipients = form.cleaned_data['recipient'].split(';')

                email = EmailMessage(
                    form.cleaned_data['subject'],
                    form.cleaned_data['content'],
                    email_data['from_email'],
                    recipients,
                    cc=[form.cleaned_data['cc']] if form.cleaned_data['cc'] else None  # Add CC if it exists
                )

            # gmail
                email.connection = get_connection(
                    host='smtp.gmail.com',
                    port=587,
                    username='qc.zcas.montreal.ca@gmail.com',
                    password='arrt odhq rtfw zdsl',
                    use_tls=True,
                )

            # Z_CAS mail
            #     email.connection = get_connection(
            #         host='smtp.office365.com',
            #         port=587,
            #         username='Xiaogao.li@zimmerbiomet.com',
            #         password='kjhafksdhfkahsdf',
            #         use_tls=True,
            #     )

                for selected_file in selected_files:
                    email.attach(selected_file.name, selected_file.read(), selected_file.content_type)

                email.send()
                return render(request, 'myemails/send_mail_success.html')
            except Exception as e:
                # Pass the exception message to the template
                error_message = str(e)
                return render(request, 'myemails/send_mail_failure.html', {'error_message': error_message})

    return render(request, 'myemails/send_mail_web.html', {'form': form})