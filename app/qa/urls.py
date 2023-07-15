from django.urls import path, include
from . import views
from .views import (
    GetAnswers,
)

app_name = "qa"

urlpatterns = [
    path("", views.index, name="index"),
    path("answer/", GetAnswers.as_view(), name="answer"),
]
