from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("error/", views.error, name="error404"),
    path("contact/", views.contact, name="contact"),
]