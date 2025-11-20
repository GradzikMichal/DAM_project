from django import forms
from django.conf import settings


class ImageForm(forms.Form):
    image_name = forms.CharField(label='Title', max_length=100)
    image_file = forms.FileField(label='picture')

