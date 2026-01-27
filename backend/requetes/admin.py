from django.contrib import admin
from .models import Requete

@admin.register(Requete)
class RequeteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'client', 'statut', 'date_creation']
    list_filter = ['statut']
    search_fields = ['nom', 'client__nom', 'client__prenom', 'description']
    date_hierarchy = 'date_creation'
