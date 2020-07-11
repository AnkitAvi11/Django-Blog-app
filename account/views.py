from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest

from .decorators import is_authenticated, is_admin, is_valid_email, is_valid_username

from .models import UserProfile

@is_authenticated
@is_admin
def loginView(request) : 
    redirected_url = request.GET.get('next', '/')
    if request.method == 'POST' : 
        try : 
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None : 
                login(request, user)
                return redirect(redirected_url)
            else : 
                messages.error(request, 'Invalid username or password')
                return redirect('/account/login?next='+redirected_url)

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

            if not is_valid_email(email) or not is_valid_username(username) :
                messages.error(request, 'Invalid username or email address')
                return redirect('/account/signup/')
            
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() : 
                messages.error(request,'User already exists with those credentials')
                return redirect('/account/signup/')
            else :
                raise User.DoesNotExist()

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

@login_required(login_url='/account/login/')
@is_admin
def logoutView(request) :
    if request.method == 'POST' : 
        logout(request)
        return redirect('/')
    else : 
        return redirect('/')

@login_required(login_url='/account/login/')
@is_admin
def settingView(request) :
    return render(request, 'account/setting.html')

@login_required(login_url='/account/login/')
@is_admin
def deleteAccount(request) : 
    if request.method == 'POST':
        user = authenticate(username=request.user.username, password = request.POST.get('password'))

        if user is not None : 
            user.userprofile.delete()
            user.delete()
            messages.success(request, 'Account successfully deleted')
            return redirect('/account/login/')
        else :
            messages.error(request, 'Incorrect password')
            return redirect('/account/setting/')
    else :
        return redirect('/')



@login_required(login_url='/account/login/')
@is_admin
def changePassword(request) : 
    if request.method == 'POST' : 
        oldpassword = request.POST.get('oldpassword')
        user = authenticate(username=request.user.username, password=oldpassword)

        if user is not None : 
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 == password2 : 
                user.set_password(password1)
                messages.success(request, 'Password changed succesfully')
                user.save()
                logout(request)
                return redirect('/account/login/')
            else : 
                messages.error(request, 'Password mismatched')
                return redirect('/account/setting/')
        else : 
            messages.error(request, 'Incorrect old password entered')
            return redirect('/account/setting/')
    else :
        return redirect('/')

@login_required(login_url='/account/login/')
@is_admin
def changeUserinfo(request) : 
    if request.method == 'POST' : 
        user = request.user 
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.userprofile.bio = request.POST.get('bio')
        user.userprofile.save()
        user.save()
        messages.success(request,'Changes made successfully')
        return redirect('/account/setting/')
    else :
        return redirect('/')


@login_required(login_url='/account/login/')
@is_admin
def changeProfilepic(request) : 
    if request.method == 'POST' :
        try : 
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.profile_pic = request.FILES.get('profile_pic')
            userprofile.save()
            data = {
                'message' : 'Success'
            }
        except : 
            data = {
                'message' : 'Error occurred'
            }
        return JsonResponse(data)
    else : 
        return redirect('/')
