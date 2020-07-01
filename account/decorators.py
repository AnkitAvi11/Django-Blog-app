#   decorator to check whether the user authenticated or not
#   preventing from going back to login or signup page

from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
import re

def is_authenticated(view_function) : 
    def wrapper_function(request, *args, **kwargs) : 
        if request.user.is_authenticated : 
            return redirect('/')
        return view_function(request, *args, **kwargs)

    return wrapper_function

def is_admin(view_function) : 
    def wrapper_function(request, *args, **kwargs) : 
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser) :
            logout(request)
            messages.error(request, 'You were loggedin as an admin. You have been logged. Login with your user account to continue.')
            return redirect('/account/login/')
        return view_function(request, *args, **kwargs)
    return wrapper_function

def is_valid_email(email) : 
    regex = re.compile('^([a-zA-Z0-9\-\_\.])+\@([a-zA-Z0-9\-\_\.])+\.([a-zA-Z0-9]{2,4})$')
    return re.match(regex, email)

def is_valid_username(username) : 
    regex = re.compile('^([a-zA-Z0-9\_]{8,})$')
    return re.match(regex, username)
    