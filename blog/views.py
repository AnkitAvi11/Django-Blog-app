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
def createBlog(request) : 
    if request.method == 'POST' : 
        try : 
            user = request.user
            title = request.POST.get('title')
            description = request.POST.get('description')
            slug = slugify(title)

            #   checking if the slug exists already
            if Blog.objects.filter(slug = slug).exists() : 
                slug = "{}-{}".format(slug, random_string_generator(size=10))

            #   getting rest of the contents of the blog
            body = request.POST.get('content')
            cover_pic = request.FILES.get('cover', None)
            is_private = True if request.POST.get('private') == 'on' else False
            pub_date = timezone.now()

            #   creatinjg a blog and saving into the database
            blog = Blog(user=user, title=title, description=description, slug = slug, body=body, cover_pic=cover_pic, is_private=is_private, pub_date=pub_date)
            blog.save()

            messages.success(request, 'Blog published')
            return redirect('/blog/create/')

        except :
            #   block of code to handle if something goes wrong
            messages.error(request, 'Some errors have occurred')
            return redirect('/blog/create/')
        
    else : 
        return render(request, 'pages/createblog.html')