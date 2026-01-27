from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Requete
from .serializers import RequeteSerializer

class RequeteViewSet(viewsets.ModelViewSet):
    queryset = Requete.objects.all()
    serializer_class = RequeteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client', 'statut', 'priorite']
    search_fields = ['objet', 'description']
    ordering_fields = ['date_creation', 'priorite']
    ordering = ['-date_creation']
