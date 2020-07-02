from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse

from blog.models import Blog

def homeView(request) :
    if request.user.is_authenticated : 
        blogs = Blog.objects.all().exclude(user=request.user).order_by('-pub_date')
    else :
        blogs = Blog.objects.all().order_by('-pub_date')

    context = {
        "blogs" : blogs
    }

    return render(request, 'pages/home.html', context)