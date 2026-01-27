from rest_framework import serializers
from .models import Realisation

class RealisationSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    client_prenom = serializers.CharField(source='client.prenom', read_only=True)
    
    class Meta:
        model = Realisation
        fields = '__all__'
