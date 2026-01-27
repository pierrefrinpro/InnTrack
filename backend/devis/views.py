from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Devis
from .serializers import DevisSerializer

class DevisViewSet(viewsets.ModelViewSet):
    queryset = Devis.objects.all()
    serializer_class = DevisSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client', 'statut']
    search_fields = ['titre', 'description']
    ordering_fields = ['date_creation', 'montant']
    ordering = ['-date_creation']
