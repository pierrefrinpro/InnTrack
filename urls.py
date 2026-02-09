# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('client/<int:client_id>/', views.client_detail, name='client_detail'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clients/', views.clients_list, name='clients_list'),
    path('api/client/<int:pk>/', views.client_detail_api, name='client_detail_api'),
    path('clients/<int:pk>/data/', views.client_detail_api, name='client_detail_api'),    
    path('api/client/<int:pk>/update/', views.client_update, name='client_update'),
    path('api/client/<int:client_id>/delete/', views.api_client_delete, name='api_client_delete'),
    path('demandes/<int:pk>/delete/', views.demande_delete, name='demande_delete'), 
    path('api/demande/<int:pk>/', views.demande_detail_api, name='demande_detail_api'),
    path('api/demande/<int:pk>/update/', views.demande_update, name='demande_update'),

    path('api/devis/<int:pk>/', views.devis_detail_api, name='devis_detail_api'),
    path('api/devis/<int:pk>/update/', views.devis_update, name='devis_update'),
    path('devis/<int:pk>/delete/', views.devis_delete, name='devis_delete'),


    # Création AJAX (modales)
    path('clients/create/', views.client_create, name='client_create'),
    path('devis/create/', views.devis_create, name='devis_create'),
    path('demandes/create/', views.demande_create, name='demande_create'),

    # Pages (placeholder)
    path('clients/', views.dashboard, name='clients'),
    path('devis/', views.dashboard, name='devis'),
    path('demandes/', views.dashboard, name='demandes'),
    path('planning/', views.dashboard, name='planning'),
    path('documents/', views.dashboard, name='documents'),
    path('stats/', views.dashboard, name='stats'),
    path('settings/', views.dashboard, name='settings'),
]
