from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from django import forms
from django.utils.text import slugify
import random
from .models import Blog
import string
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.decorators import is_admin

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 

@login_required(login_url='/account/login/')
@is_admin
# Create your views here.
def createBlog(request) : 
    if request.method == 'POST' : 
        user = request.user
        title = request.POST.get('title')
        description = request.POST.get('description')
        slug = slugify(title)
        #   checking if the slug exists
        if Blog.objects.filter(slug = slug).exists() : 
            slug = "{}--{}".format(slug, random_string_generator(size=4))
        body = request.POST.get('content')
        cover_pic = request.FILES.get('cover', None)
        is_private = True if request.POST.get('private') == 'on' else False
        pub_date = timezone.now()

        blog = Blog(user=user, title=title, description=description, slug = slug, body=body, cover_pic=cover_pic, is_private=is_private, pub_date=pub_date)

        blog.save()
        messages.success(request, 'Blog published')
        return redirect('/blog/create/')
        
    else : 
        return render(request, 'pages/createblog.html')