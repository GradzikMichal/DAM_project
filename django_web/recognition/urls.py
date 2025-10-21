from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("image_recognition/", views.index_recognition, name="index_recognition"),

]