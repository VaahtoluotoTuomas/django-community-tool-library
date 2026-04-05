from django.urls import path
from . import views

urlpatterns = [
    path('', views.tyokalu_lista, name='työkalu_lista'),
]