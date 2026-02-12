from django.urls import path
from . import views

urlpatterns = [
    # ─── Dashboard ───
    path('', views.dashboard, name='dashboard'),

    # ─── Clients ───
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('api/client/<int:pk>/', views.client_detail_api, name='client_detail_api'),
    path('api/client/<int:pk>/update/', views.client_update, name='client_update'),
    path('api/client/<int:client_id>/delete/', views.api_client_delete, name='api_client_delete'),

    # ─── Demandes ───
    path('demandes/', views.demandes_list_view, name='demandes_list'),
    path('demandes/create/', views.demande_create, name='demande_create'),
    path('demandes/<int:pk>/delete/', views.demande_delete, name='demande_delete'),
    path('api/demande/<int:pk>/', views.demande_detail_api, name='demande_detail_api'),
    path('api/demande/<int:pk>/update/', views.demande_update, name='demande_update'),

    # ─── Devis ───
    path('devis/', views.devis_list_view, name='devis_list'),
    path('devis/create/', views.devis_create, name='devis_create'),
    path('devis/<int:pk>/delete/', views.devis_delete, name='devis_delete'),
    path('api/devis/<int:pk>/', views.devis_detail_api, name='devis_detail_api'),
    path('api/devis/<int:pk>/update/', views.devis_update, name='devis_update'),

    # ─── Travaux ───
    path('travaux/', views.travaux_list_view, name='travaux_list'),
    path('travaux/create/', views.travaux_create, name='travaux_create'),
    path('travaux/<int:pk>/delete/', views.travaux_delete, name='travaux_delete'),
    path('api/travaux/<int:pk>/', views.travaux_detail_api, name='travaux_detail_api'),
    path('api/travaux/<int:pk>/update/', views.travaux_update, name='travaux_update'),

    # ─── Factures ───
    path('factures/', views.factures_list_view, name='factures_list'),
    path('factures/create/', views.facture_create, name='facture_create'),
    path('factures/<int:pk>/delete/', views.facture_delete, name='facture_delete'),
    path('api/facture/<int:pk>/', views.facture_detail_api, name='facture_detail_api'),
    path('api/facture/<int:pk>/update/', views.facture_update, name='facture_update'),

    # ─── Pages placeholder ───
    path('planning/', views.planning_view, name='planning'),
    path('documents/', views.dashboard, name='documents'),
    path('stats/', views.dashboard, name='stats'),
    path('settings/', views.dashboard, name='settings'),
]
