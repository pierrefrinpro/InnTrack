from django.contrib import admin
from .models import Facture

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['prestation', 'client', 'type', 'date_facturation', 'montant_ht', 'montant_tva', 'montant_ttc']
    list_filter = ['type', 'date_facturation']
    search_fields = ['prestation', 'client__nom', 'client__prenom']
    date_hierarchy = 'date_facturation'
    
    readonly_fields = ['montant_tva', 'montant_ttc']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('type', 'client', 'prestation', 'date_facturation')
        }),
        ('Montants', {
            'fields': ('montant_ht', 'taux_tva', 'montant_tva', 'montant_ttc')
        }),
    )
