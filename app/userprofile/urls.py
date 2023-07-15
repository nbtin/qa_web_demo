from django.urls import path
from . import views
app_name = 'userprofile'
urlpatterns = [
    path('saveProfile', views.saveProfile, name='saveProfile'),
    path('<str:username>', views.userprofile, name='userprofile'),
]
