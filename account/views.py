from django.shortcuts import render, redirect

def loginView(request) : 
    if request.method == 'POST' : 
        pass
    else : 
        return render(request, 'account/login.html')