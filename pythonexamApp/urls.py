from django.urls import path, include
from .import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("success", views.home),
    path("logout", views.logout),
    path("login", views.login),
    path("trips/add", views.addTrip),
    path("createtrip", views.createTrip),
    path("trips/<tripID>", views.showTrip),
    path("join/<tripID>", views.join)
]
