from django.contrib import admin
from .models import Realisation

@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ['nom', 'client', 'date_realisation_prevue']
    search_fields = ['nom', 'client__nom', 'client__prenom']
    date_hierarchy = 'date_realisation_prevue'
