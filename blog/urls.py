from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create/', views.createBlog, name='createblog'),
    path('read/<int:id>/', views.viewBlog, name='view'),
]