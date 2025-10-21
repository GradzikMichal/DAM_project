from django.core.files.uploadedfile import InMemoryUploadedFile

from django.conf import settings


def handle_uploaded_pictures(uploaded_pictures: InMemoryUploadedFile, file_id: str, file_type: str):
    with open(settings.MEDIA_ROOT + '\\' + file_id + "." + file_type, 'wb+') as destination:
        for chunk in uploaded_pictures.chunks():
            destination.write(chunk)
