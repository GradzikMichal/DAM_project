from django import forms


class ImageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    picture_file = forms.FileField(label='picture')
