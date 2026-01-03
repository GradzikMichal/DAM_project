from django.shortcuts import render
from .forms import ImageForm
import logging
from .helping_functions import handle_uploaded_pictures
from .kafka_functions import add_img_to_db_using_kafka, receive_img_id_from_db_using_kafka, send_img_to_recognize, \
    receive_img_from_recognize
from .image_class import ImageClass
from PIL import Image


# Create your views here.


def index(request):
    return render(request, 'home_page/index.html')


def index_recognition(request):
    file_saved = False
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            #add logging on page
            logging.info("Got form data")
            image_data = ImageClass(
                image_name=form.cleaned_data["image_name"],
                image_path=form.cleaned_data["image_file"],
                image_type=form.cleaned_data['image_file'].name.split('.')[-1],
                image_file=Image.open(form.cleaned_data["image_file"])
            )
            add_img_to_db_using_kafka(image_data)
            image_data.image_id = receive_img_id_from_db_using_kafka()
            image_data.saveImage()
            image_data.file_saved = True
            send_img_to_recognize(image_data)
            receive_img_from_recognize()

    else:
        form = ImageForm()
    return render(request, 'img_rec_page/index.html', {'form': form, 'file_saved': file_saved})
