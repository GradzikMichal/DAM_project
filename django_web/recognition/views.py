from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageForm
import logging
from .helping_functions import handle_uploaded_pictures
from .kafka_functions import send_img_data_using_kafka, receive_img_data_using_kafka
from .image_class import ImageClass
# Create your views here.


def index(request):
    return render(request, 'home_page/index.html')

def index_recognition(request):
    file_saved = False
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            #add logging on page
            logging.info("Get form data")
            print("Got form data")
            image_data = ImageClass(
                image_name=form.cleaned_data["image_name"],
                image_file=form.cleaned_data["image_file"],
            )
            send_img_data_using_kafka(image_data)
            image_data['image_id'] = receive_img_data_using_kafka()
            file_type = form.cleaned_data['image_file'].name.split('.')[-1]
            handle_uploaded_pictures(image_bytes, image_data['image_id'], file_type)
            image_data['file_saved'] = True
            send_img_data_using_kafka(image_data)
    else:
        form = ImageForm()
    return render(request, 'img_rec_page/index.html', {'form': form, 'file_saved': file_saved})
