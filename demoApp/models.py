from datetime import date
from django.utils.translation import gettext as _
from django.db import models


PARTICULIER = "particulier"
PROFESSIONNEL = "professionnel"
INTERVENTION = "intervention"
CHANTIER = "chantier"
A_FAIRE = "A faire"
ATTENTE_CLIENT= "En attente client"
ACCEPTE = "Accepté"
REFUSE = "Refusé"

class client(models.Model):
    type_of_client = [
        (PARTICULIER, "particulier"),
        (PROFESSIONNEL, "professionnel")
    ]
    
    firstName = models.CharField(_("Prénom"),max_length=100)
    lastName = models.CharField(_("Nom"),max_length=100)
    type = models.CharField(
        choices=type_of_client,
        default=PARTICULIER,
        max_length=19
    )
    email = models.EmailField(max_length=254, default="example@example.com", blank=False)
    postal_address = models.CharField(_("Adresse postale"),max_length=255, blank=False)
    phone = models.CharField(_("Téléphone"),max_length=10, default="0600000000", blank=False)

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.firstName, self.lastName)
    full_name = property(_get_full_name)

    def __str__(self):
        return self.full_name
    

class demande(models.Model):
    type_of_demande = [
        (INTERVENTION, "intervention"),
        (CHANTIER, "chantier")
    ]

    client = models.ForeignKey(client, on_delete=models.CASCADE,blank=False)
    demandeDate = models.DateField(_("Date de la demande"),null=True, blank=True, default=date.today)
    motif = models.CharField(max_length=255)
    type = models.CharField(
        choices=type_of_demande,
        default=INTERVENTION,
        max_length=22
    )
    excpectedVisitDate = models.DateField(_("Date prévue de la visite"),null=True, blank=True, default=date.today)
    clientAvailibity = models.CharField(max_length=255)
    realVisitDate = models.DateField(_("Date réele de la visite"),null=True, blank=True, default=date.today)

    def __str__(self):
        return  "Demande - " + self.client.full_name
    
class devis(models.Model):
    type_of_devis = [
        (INTERVENTION, "intervention"),
        (CHANTIER, "chantier")
    ]

    status_of_devis = [
        (A_FAIRE, "A faire"),
        (ATTENTE_CLIENT, "En attente client"),
        (ACCEPTE, "Accepté"),
        (REFUSE, "Refusé")
    ]

    client = models.ForeignKey(client, on_delete=models.CASCADE,blank=False)
    demande = models.ForeignKey(demande, on_delete=models.CASCADE,null=True,blank=True)

    def _get_types(self):
        type_of_devis = [
            (INTERVENTION, "intervention"),
            (CHANTIER, "chantier")
        ]
        if demande != "" :
            return '%s' % (self.demande.type)
        else :
            return models.CharField(choices=type_of_devis,default=INTERVENTION,max_length=22)
    type = property(_get_types)
    
    status = models.CharField(
        choices=status_of_devis,
        default=A_FAIRE,
        max_length=25
    )
    excpectedSentDate = models.DateField(_("Date d'envoi prévue"),null=True, blank=True, default=date.today)
    comment = models.CharField(_("Note personnelle"),max_length=1000,null=True,blank=True)
    sent = models.BooleanField(_("Devis envoyé ?"), default=False)
    createdDate = models.DateField(_("Date de création"), auto_now=True)
    realSentDate = models.DateField(_("Date d'envoi réelle"),null=True, blank=True, default=date.today)

    def __str__(self):
        return "Devis - " + self.client.full_name
    
    class Meta :
        verbose_name_plural = "devis"

class travaux(models.Model):
    type_of_travaux = [
        (INTERVENTION, "intervention"),
        (CHANTIER, "chantier")
    ]

    client = models.ForeignKey(client, on_delete=models.CASCADE,blank=False)
    demande = models.ForeignKey(demande, on_delete=models.CASCADE,null=True)
    devis = models.ForeignKey(devis, on_delete=models.CASCADE,null=True)
    
    startDate = models.DateField(_("Date de début des travaux"),null=True, blank=True, default=date.today)
    type =  models.CharField(
        choices=type_of_travaux,
        default=INTERVENTION,
        max_length=24
    )
    terminated = models.BooleanField(_("Terminé ?"), default=False)
    endDate = models.DateField(_("Date de fin des travaux"),null=True, blank=True, default=date.today)

    def __str__(self):
        return "Travaux - " + self.client.full_name

    class Meta :
        verbose_name_plural = "travaux"
