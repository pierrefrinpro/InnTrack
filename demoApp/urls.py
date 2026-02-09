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
    path('clients/<int:pk>/data/', views.client_detail_api, name='client_detail_api'),

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
