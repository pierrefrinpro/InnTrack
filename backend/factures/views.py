from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Facture
from .serializers import FactureSerializer

class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client', 'statut']
    search_fields = ['numero_facture']
    ordering_fields = ['date_emission', 'montant_total']
    ordering = ['-date_emission']
