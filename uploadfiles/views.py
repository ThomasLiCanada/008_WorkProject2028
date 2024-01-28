from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('document')
        fs = FileSystemStorage()
        urls = []

        for uploaded_file in uploaded_files:

            # below 2 lines for overwrite the file with same name
            if fs.exists(uploaded_file.name):
                fs.delete(uploaded_file.name)

            name = fs.save(uploaded_file.name, uploaded_file)
            urls.append(fs.url(name))

        context['urls'] = urls

    return render(request, 'uploadfiles/upload.html', context)