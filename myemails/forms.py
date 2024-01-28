# myemails/forms.py
from django import forms
from multiupload.fields import MultiFileField


class FileUploadForm(forms.Form):
    recipient = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'To:'}))
    cc = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'CC:'}))
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Subject:'}))
    content = forms.CharField(max_length=2083, widget=forms.Textarea(
        attrs={'placeholder': 'Content:', 'rows': 10, 'cols': 173}))  # Adjust 'rows' to your desired height  , 'cols': 150
    files = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5, required=False)

