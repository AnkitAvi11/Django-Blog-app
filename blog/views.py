from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404

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
            
            #   getting rest of the contents of the blog
            body = request.POST.get('content')
            cover_pic = request.FILES.get('cover', None)
            is_private = True if request.POST.get('private') == 'on' else False
            pub_date = timezone.now()

            #   creatinjg a blog and saving into the database
            blog = Blog(user=user, title=title, description=description, body=body, cover_pic=cover_pic, is_private=is_private, pub_date=pub_date)
            blog.save()

            messages.success(request, 'Blog published')
            return redirect('/blog/create/')
        except Exception as e: 
            #   if something goes wrong
            messages.error(request, e)
            return redirect('/blog/create/')
        
    else : 
        return render(request, 'pages/createblog.html')

def viewBlog(request, id) : 
    try : 
        blog = Blog.objects.get(id=id)
        if blog is not None : 
            if blog.is_private == True and request.user!=blog.user: 
                raise NameError("Sorry! This blog is private and you don't have rights to view it.")
            else :
                return render(request, 'pages/viewblog.html', {"blog":blog})
        else : 
            raise Http404
    except Exception as e: 
        context = {
            "error" : e
        }
        return render(request, 'pages/errorpage.html', context)

@login_required(login_url='/account/login/')
def likePost(request) : 
    try : 
        if request.method == 'POST' : 
            blogid = request.POST.get('blogid')
            user = request.user
            blog = Blog.objects.get(id=blogid)

            if user in blog.likes.all() : 
                blog.likes.remove(user)
                message = 'far'
            else: 
                blog.likes.add(user)
                message = 'fas'

            return JsonResponse({
                'status' : message
            })
        else : 
            raise Http404()
    except Exception as e:
        context = {
            "error" : "You are not authorised to view this page"
        }
        return render(request, 'pages/errorpage.html', context)