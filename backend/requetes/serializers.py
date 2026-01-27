from rest_framework import serializers
from .models import Requete

class RequeteSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    client_prenom = serializers.CharField(source='client.prenom', read_only=True)
    
    class Meta:
        model = Requete
        fields = '__all__'
