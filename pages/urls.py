from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('profile/<str:username>', views.getUser, name='viewuser')
]