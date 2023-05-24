from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index),
    path("submit/<str:project_name>", views.evaluate_project)
]
