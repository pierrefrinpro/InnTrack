from django.db import models
from clients.models import Client

class Devis(models.Model):
    STATUT_CHOICES = [
        ('ENVOYE', 'Envoyé'),
        ('ATTENTE', 'En attente client'),
        ('ACCEPTE', 'Accepté'),
        ('REFUSE', 'Refusé'),
    ]
    
    nom = models.CharField("Nom", max_length=200)
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='devis',
        verbose_name="Client"
    )
    
    date_envoi = models.DateField("Date d'envoi", null=True, blank=True)
    date_validite = models.DateField("Date de validité", null=True, blank=True)
    date_derniere_relance = models.DateField("Dernière relance", null=True, blank=True)
    
    montant_ht = models.DecimalField("Montant HT", max_digits=10, decimal_places=2, default=0)
    statut = models.CharField("Statut", max_length=20, choices=STATUT_CHOICES, default='ENVOYE')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom} - {self.client}"
    
    class Meta:
        verbose_name = "Devis"
        verbose_name_plural = "Devis"
        ordering = ['-date_envoi']
