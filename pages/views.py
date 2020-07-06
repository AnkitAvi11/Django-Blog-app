from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse

from blog.models import Blog
from django.contrib.auth.models import User
from account.models import UserProfile

def homeView(request) :
    if request.user.is_authenticated : 
        blogs = Blog.objects.exclude(user=request.user).exclude(is_private=True).order_by('-pub_date')
    else :
        blogs = Blog.objects.exclude(is_private=True).order_by('-pub_date')

    context = {
        "blogs" : blogs[:10]
    }

    return render(request, 'pages/home.html', context)

def getUser(request, username) : 
    try : 
        profile = UserProfile.objects.get(user__username=username)
        # checking if user is authenticated
        if request.user.is_authenticated : 
            #   checking if the authenticated user is same as the searched one
            if request.user.username == username : 
                blogs = Blog.objects.filter(user=profile.user).order_by('-pub_date')
            else : 
                blogs = Blog.objects.filter(user=profile.user).exclude(is_private=True).order_by('-pub_date')
        else : 
            blogs = Blog.objects.filter(user=profile.user).exclude(is_private=True).order_by('-pub_date')

        sameuser = True if request.user.username == username else False
        
        context = {
            "profile" : profile,
            "blogs" : blogs,
            "is_same_user" : sameuser
        }

    except Exception as e: 
        print("Exception = ", e)
        raise Http404
    return render(request, 'pages/viewprofile.html', context)