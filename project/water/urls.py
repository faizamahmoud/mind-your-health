# path/, name of view, string name of route
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
]