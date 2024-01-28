# receivings/views.py------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from .forms import InputReceivingForm
from .models import Receiving


def input_receiving_view(request):
    receiving_form = InputReceivingForm()

    if request.method == 'POST':
        if 'receiving_form_submit' in request.POST:
            receiving_form = InputReceivingForm(request.POST)
            if receiving_form.is_valid():
                receiving_form.save()
                return redirect('/')

    # Check if 'lot_num' is passed in the URL (GET parameter)
    part_description = request.GET.get('part_description')

    # If 'lot_num' is passed in the URL, pre-fill the form
    if part_description:
        receiving_form.initial['part_description'] = part_description
    context = {
        'receiving_form': receiving_form,
    }

    return render(request, 'receivings/input_receiving.html', context)
