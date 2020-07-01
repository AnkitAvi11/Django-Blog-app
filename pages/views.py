from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse

def homeView(request) :
    return render(request, 'pages/home.html')