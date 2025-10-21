from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageForm
from .helping_functions import handle_uploaded_pictures
# Create your views here.


def index(request):
    return render(request, 'home_page/index.html')

def index_recognition(request):
    file_saved = False
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            file_type = form.cleaned_data['picture_file'].name.split('.')[-1]
            handle_uploaded_pictures(form.cleaned_data['picture_file'], "test", file_type)
            file_saved = True
    else:
        form = ImageForm()
    return render(request, 'img_rec_page/index.html', {'form': form, 'file_saved': file_saved})
