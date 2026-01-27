from django.db import models
from clients.models import Client

class Requete(models.Model):
    STATUT_CHOICES = [
        ('A_FAIRE', 'À faire'),
        ('EN_TEMPS', 'Faite en temps et en heure'),
        ('EN_RETARD', 'Faite mais en retard'),
        ('PAS_REALISEE', 'Pas encore réalisée'),
    ]
    
    nom = models.CharField("Nom", max_length=200)
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='requetes',
        verbose_name="Client"
    )
    
    mcpt = models.CharField("MC/PT", max_length=100, blank=True)
    type = models.CharField("Type", max_length=100, blank=True)
    
    date_commande = models.DateField("Date de commande", null=True, blank=True)
    date_visite_reelle = models.DateField("Date visite réelle", null=True, blank=True)
    disponibilite_client = models.CharField("Disponibilité client", max_length=200, blank=True)
    
    statut = models.CharField("Statut", max_length=20, choices=STATUT_CHOICES, default='A_FAIRE')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom} - {self.client}"
    
    class Meta:
        verbose_name = "Requête"
        verbose_name_plural = "Requêtes"
        ordering = ['-date_commande']
