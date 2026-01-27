from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Realisation
from .serializers import RealisationSerializer

class RealisationViewSet(viewsets.ModelViewSet):
    queryset = Realisation.objects.all()
    serializer_class = RealisationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['devis', 'statut']
    search_fields = ['titre', 'description']
    ordering_fields = ['date_debut', 'date_fin']
    ordering = ['-date_debut']
