from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse

from blog.models import Blog

def homeView(request) :
    if request.user.is_authenticated : 
        blogs = Blog.objects.exclude(user=request.user).exclude(cover_pic__iexact="").exclude(cover_pic__isnull=True).order_by('-pub_date')
    else :
        blogs = Blog.objects.exclude(cover_pic__iexact="").exclude(cover_pic__isnull=True).order_by('-pub_date')

    context = {
        "blogs" : blogs
    }

    return render(request, 'pages/home.html', context)