# projects/forms.py------------------------------------------------------------------------------
from django import forms
from .models import Project
from django.utils import timezone


class InputProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     moved_pac_nc = cleaned_data.get('project_parts_moved_pac_nc')
    #     moved_pac_nc_date = cleaned_data.get('project_parts_moved_pac_nc_date')
    #
    #     # Set the current date and time if checkbox is checked
    #     if moved_pac_nc:
    #         if moved_pac_nc_date == None:
    #             print(moved_pac_nc_date)
    #             cleaned_data['project_parts_moved_pac_nc_date'] = timezone.now()
    #     else:
    #         # Set to None if checkbox is unchecked
    #         cleaned_data['project_parts_moved_pac_nc_date'] = None
    #
    #     return cleaned_data
