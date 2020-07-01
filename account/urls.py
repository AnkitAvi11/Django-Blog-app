from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('signup/', views.signupView, name='signup'),
    path('logout/', views.logoutView, name='userlogout'),
    path('setting/', views.settingView, name='usersetting'),
    path('delete/', views.deleteAccount, name='deleteAccount'),
    path('changepassword/', views.changePassword, name='changepassword'),
    path('changeUserinfo', views.changeUserinfo, name='userinfo'),
]