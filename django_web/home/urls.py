from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user-home', views.home),
    path('login', views.user_login),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)