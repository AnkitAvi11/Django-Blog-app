from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile
from django.db.models import Q
from django.contrib import messages

from .decorators import is_authenticated, is_admin

@is_authenticated
@is_admin
def loginView(request) : 
    redirected_url = '/'
    if request.method == 'POST' : 
        try : 
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None : 
                login(request, user)
                return redirect('/')
            else : 
                messages.error(request, 'Invalid username or password')
                return redirect('/account/login')

        except: 
            pass
    else : 
        return render(request, 'account/login.html', {"next" : redirected_url})


@is_authenticated
@is_admin
def signupView(request) : 
    if request.method == 'POST' : 
        try : 
            #   checking if the user already exists
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = User.objects.get(Q(username=username)|Q(email=email))

            messages.error(request,'User already exists with those credentials')
            return redirect('/account/signup/')

        except User.DoesNotExist : 
            #   when the user doesnot exist we create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = UserProfile(
                user=user,
                username=username,
                profile_pic = request.FILES.get('profile_pic', 'default.png'),
                bio = request.POST.get('bio')
            )
            profile.save()
            user.save()
            messages.success(request, 'Account succesfully created. Please login to continue.')
            return redirect('/account/login/')

    else : 
        # request method is GET
        return render(request, 'account/signup.html')