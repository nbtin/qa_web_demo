# account/urls.py
from django.urls import path, include
from account import views


urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signupuser, name="signupuser"),
    path('login/', views.loginuser, name="loginuser"),
    path('handlelogout/', views.handlelogout, name="handlelogout"),
    path('changepass/', views.ChangePassword.as_view(), name="changepass"),
    path('vqa/', include('vqa.urls')),
]
