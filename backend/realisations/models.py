from django.db import models
from clients.models import Client
from devis.models import Devis

class Realisation(models.Model):
    STATUT_CHOICES = [
        ('NON_PREVUE', 'Non prévue'),
        ('PROGRAMMEE', 'Programmée'),
        ('EN_COURS', 'En cours'),
        ('PASSEE', 'Passée'),
    ]
    
    nom = models.CharField("Nom", max_length=200)
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='realisations',
        verbose_name="Client"
    )
    devis = models.ForeignKey(
        Devis, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='realisations',
        verbose_name="Devis"
    )
    
    date_realisation_prevue = models.DateField("Date prévue", null=True, blank=True)
    statut = models.CharField("Statut", max_length=20, choices=STATUT_CHOICES, default='NON_PREVUE')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom} - {self.client}"
    
    class Meta:
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"
        ordering = ['-date_realisation_prevue']
