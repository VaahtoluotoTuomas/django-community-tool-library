from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.tyokalu_lista, name='tyokalu_lista'),
    path('tyokalu/<int:tyokalu_id>/', views.tyokalu_tiedot, name='tyokalu_tiedot'),
    path('kirjaudu/', auth_views.LoginView.as_view(template_name='tyokalut/kirjaudu.html'), name='kirjaudu'),
    path('kirjaudu-ulos/', auth_views.LogoutView.as_view(), name='kirjaudu_ulos'),
    path('rekisteroidy/', views.rekisteroidy, name='rekisteroidy'),
    path('tyokalu/<int:tyokalu_id>/lainaa/', views.lainaa_tyokalu, name='lainaa_tyokalu'),
    path('omat-lainat/', views.omat_lainat, name='omat_lainat'),
    path('palauta/<int:laina_id>/', views.palauta_tyokalu, name='palauta_tyokalu'),
]