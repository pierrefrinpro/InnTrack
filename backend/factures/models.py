from django.db import models
from clients.models import Client

class Facture(models.Model):
    TYPE_CHOICES = [
        ('CLIENT', 'Client'),
        ('FOURNISSEUR', 'Fournisseur'),
    ]
    
    type = models.CharField("Type", max_length=20, choices=TYPE_CHOICES)
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='factures',
        verbose_name="Client",
        null=True,
        blank=True
    )
    
    prestation = models.CharField("Prestation", max_length=200)
    date_facturation = models.DateField("Date facturation")
    
    montant_ht = models.DecimalField("Montant HT", max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField("Taux TVA (%)", max_digits=5, decimal_places=2, default=20)
    montant_tva = models.DecimalField("Montant TVA", max_digits=10, decimal_places=2, editable=False)
    montant_ttc = models.DecimalField("Montant TTC", max_digits=10, decimal_places=2, editable=False)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.montant_tva = self.montant_ht * (self.taux_tva / 100)
        self.montant_ttc = self.montant_ht + self.montant_tva
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.prestation} - {self.montant_ttc}€"
    
    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-date_facturation']
