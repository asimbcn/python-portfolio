from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('Logout/',views.logout,name='logout'),
    path('register/', views.register, name='register'),
    path('index/',views.index ,name='index'),
    path('OTF/',views.OTF,name='otf'),
    path('view/',views.table,name='view'),
    path('edit-user/',views.edit_user,name='editUser'),

    path('add-work/',views.add_work,name='addWork'),
    path('edit-work/<int:id>',views.edit_work,name='editWork'),
    path('delete-work/<int:id>',views.delete_work,name='deleteWork'),
    
    path('add-education/',views.add_education,name='addEducation'),
    path('edit-education/<int:id>',views.edit_education,name='editEducation'),
    path('delete-education/<int:id>',views.delete_education,name='deleteEducation'),
    
    path('add-project/',views.add_project,name='addProject'),    
    path('edit-project/<int:id>',views.edit_project,name='editProject'),
    path('delete-project/<int:id>',views.delete_project,name='deleteProject'),

    path('front-end/',views.front_end,name='frontend'),
    path('delete-user/',views.delete_user,name='deleteUser'),
    
]