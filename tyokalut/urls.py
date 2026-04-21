from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.TyokaluListView.as_view(), name='tyokalu_lista'),
    path('tyokalu/<int:tyokalu_id>/', views.TyokaluDetailView.as_view(), name='tyokalu_tiedot'),
    path('kirjaudu/', auth_views.LoginView.as_view(template_name='tyokalut/kirjaudu.html'), name='kirjaudu'),
    path('kirjaudu-ulos/', auth_views.LogoutView.as_view(), name='kirjaudu_ulos'),
    path('rekisteroidy/', views.rekisteroidy, name='rekisteroidy'),
    path('tyokalu/<int:tyokalu_id>/lainaa/', views.lainaa_tyokalu, name='lainaa_tyokalu'),
    path('omat-lainat/', views.OmatLainatView.as_view(), name='omat_lainat'),
    path('palauta/<int:laina_id>/', views.palauta_tyokalu, name='palauta_tyokalu'),
] + debug_toolbar_urls()