from django.urls import path, include
from . import views
from .views import (
    GetAnswers,
)

urlpatterns = [
    path("", views.index),
    path("answer", GetAnswers.as_view()),
]
