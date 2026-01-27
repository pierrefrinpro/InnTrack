from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from clients.views import ClientViewSet
from devis.views import DevisViewSet
from requetes.views import RequeteViewSet
from realisations.views import RealisationViewSet
from factures.views import FactureViewSet

# Création du router pour l'API
router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'devis', DevisViewSet)
router.register(r'requetes', RequeteViewSet)
router.register(r'realisations', RealisationViewSet)
router.register(r'factures', FactureViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
