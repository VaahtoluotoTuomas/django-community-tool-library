from django.urls import path
from . import views

urlpatterns = [
    path('', views.tyokalu_lista, name='tyokalu_lista'),
    path('tyokalu/<int:tyokalu_id>/', views.tyokalu_tiedot, name='tyokalu_tiedot'),
]