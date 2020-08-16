from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('index/',views.index ,name='index'),
    path('OTF/',views.OTF,name='otf'),
    path('view/',views.table,name='view'),
    path('edit-user/',views.edit_user,name='editUser'),
    path('edit-work/',views.edit_work,name='editWork'),
    path('Logout/',views.logout,name='logout')
]