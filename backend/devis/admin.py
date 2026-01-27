from django.contrib import admin
from .models import Devis

@admin.register(Devis)
class DevisAdmin(admin.ModelAdmin):
    list_display = ['nom', 'client', 'montant_ht', 'statut', 'date_envoi', 'date_validite']
    list_filter = ['statut', 'date_envoi']
    search_fields = ['nom', 'client__nom', 'client__prenom']
    date_hierarchy = 'date_envoi'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'client', 'statut')
        }),
        ('Dates', {
            'fields': ('date_envoi', 'date_validite', 'date_derniere_relance')
        }),
        ('Montants', {
            'fields': ('montant_ht',)
        }),
    )
