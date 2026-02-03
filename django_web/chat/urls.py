from django.urls import path, include
from . import views

urlpatterns = [
    path('chats', views.chat_history),
    path('chats/', views.chat_messages)
]