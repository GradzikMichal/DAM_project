import io

from PIL import Image

from .image_class import ImageClass
from django.conf import settings


def handle_uploaded_pictures(image: ImageClass):
    img.frombytes(image.image_bytes)
    print(img.tobytes())
    img.save()