from datetime import date, timedelta
from django.utils.translation import gettext as _
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
            
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

PARTICULIER = "particulier"
PROFESSIONNEL = "professionnel"
INTERVENTION = "intervention"
CHANTIER = "chantier"
A_FAIRE = "A faire"
ATTENTE_CLIENT= "En attente client"
ACCEPTE = "Accepté"
REFUSE = "Refusé"
FOURNISSEUR = "Fournisseur"
CLIENT = "Client"

##Calcul des jours ouvrés
def workday(start_date, days):
    """Ajoute N jours ouvrés (lundi-vendredi) à une date."""
    if not start_date:
        return None
    current = start_date
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # 0=lundi ... 4=vendredi
            added += 1
    return current

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
    clientAvailibity = models.CharField(_("Disponibilités client"),max_length=255)
    realVisitDate = models.DateField(_("Date réele de la visite"),null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculer excpectedVisitDate
        if self.demandeDate :
            self.excpectedVisitDate = workday(self.demandeDate, 5)

        # Vérifier que la demande est terminée (visite réalisée) et créer un devis lié automatiquement
        is_new_visit = False
        if self.pk:
            old = demande.objects.filter(pk=self.pk).values('realVisitDate').first()
            if old and not old['realVisitDate'] and self.realVisitDate:
                is_new_visit = True
        elif self.realVisitDate:
            is_new_visit = True

        super().save(*args, **kwargs)

        # Créer automatiquement un devis si visite réelle vient d'être renseignée
        if is_new_visit:
            devis.objects.create(
                demande=self,
                client=self.client,
                status=A_FAIRE,
                excpectedSentDate=workday(self.realVisitDate, 10)
            )

    def __str__(self):
        return  "Demande - " + self.client.full_name
    
    @property
    def color_code(self):
        """
        Retourne un code couleur basé sur les règles métier :
        - 'green'  : visite réelle effectuée et dépassée
        - 'red'    : 5+ jours ouvrés sans devis lié
        - 'orange' : 3-5 jours ouvrés sans devis lié
        - None     : pas de couleur spéciale
        """
        today = date.today()

         # 🟢 Vert : visite réelle renseignée ET today > date visite réelle
        if self.realVisitDate and today > self.realVisitDate:
            return 'green'

        # Pas de devis lié ?
        has_devis = self.devis_set.exists()

        if self.excpectedVisitDate and not self.realVisitDate:
            deadline_5 = workday(self.excpectedVisitDate, 5)
            deadline_3 = workday(self.excpectedVisitDate, 3)

            # 🟠 Orange : 3-5 jours ouvrés sans devis
            if deadline_3 and today >= deadline_3 and today < deadline_5 :
                return 'orange'

            # 🔴 Rouge : 5+ jours ouvrés sans devis
            if deadline_5 and today >= deadline_5:
                return 'red'

        return None
    
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

    excpectedSentDate = models.DateField(_("Date d'envoi prévue"),null=True, blank=True)
    comment = models.CharField(_("Note personnelle"),max_length=1000,null=True,blank=True)
    sent = models.BooleanField(_("Devis envoyé ?"), default=False)
    createdDate = models.DateField(_("Date de création"), auto_now=True)
    realSentDate = models.DateField(_("Date d'envoi réelle"),null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculer excpectedSentDate si la demande a une date de visite réelle
        if self.demande and self.demande.realVisitDate:
            self.excpectedSentDate = workday(self.demande.realVisitDate, 10)
        super().save(*args, **kwargs)

    def __str__(self):
        return "Devis - " + self.client.full_name
    
    class Meta :
        verbose_name_plural = "devis"

    @property
    def color_code(self):
        """
        Retourne un code couleur basé sur les règles métier :
        - 'green'  : envoyé et accepté
        - 'orange' : 6+ jours ouvrés sans avoir envoyé
        - 'red'    : 12+ jours ouvrés sans avoir envoyé
        - 'violet' : 13+ jours ouvrés sans avoir envoyé
        """
        today = date.today()

        if self.sent and self.status == ACCEPTE:
            return 'green'

        if self.excpectedSentDate and not self.sent:
            deadline_13 = workday(self.excpectedSentDate, 13)
            deadline_12 = workday(self.excpectedSentDate, 12)
            deadline_6 = workday(self.excpectedSentDate, 6)

            if deadline_6 and today >= deadline_6 and today < deadline_12 :
                return 'orange'

            if deadline_12 and today >= deadline_12 and today < deadline_13 :
                return 'red'
            
            if deadline_13 and today >= deadline_13  :
                return 'violet'

        return None

class travaux(models.Model):
    type_of_travaux = [
        (INTERVENTION, "intervention"),
        (CHANTIER, "chantier")
    ]

    client = models.ForeignKey(client, on_delete=models.CASCADE,blank=False)
    demande = models.ForeignKey(demande, on_delete=models.CASCADE,null=True)
    devis = models.ForeignKey(devis, on_delete=models.CASCADE,null=True)
    
    startDate = models.DateField(_("Date de début des travaux"),null=True, blank=True)
    type =  models.CharField(
        choices=type_of_travaux,
        default=INTERVENTION,
        max_length=24
    )
    terminated = models.BooleanField(_("Terminé ?"), default=False)
    endDate = models.DateField(_("Date de fin des travaux"),null=True, blank=True)

    def __str__(self):
        return "Travaux - " + self.client.full_name

    class Meta :
        verbose_name_plural = "travaux"


class facture(models.Model):
    type_of_facture = [
        (FOURNISSEUR, "Fournisseur"),
        (CLIENT, "Client")
    ]

    type =  models.CharField(
        choices=type_of_facture,
        default=FOURNISSEUR,
        max_length=24
    )
    client = models.CharField(_("Client"),max_length=100,null=True,blank=True)
    number = models.CharField(_("Numéro"),max_length=100,null=True,blank=True)
    date = models.DateField(_("Date de facture"),null=True,blank=True)
    prestation = models.CharField(_("Prestation"),max_length=100,null=True,blank=True)
    taxe_exo = models.BooleanField(_("Exonération de taxe"),default=False)
    amount_ht = models.DecimalField(_("Montant H.T"),max_digits=6,decimal_places=0,max_length=10,null=True,blank=True,default=0)
    tva = models.DecimalField(_("TVA applicable"),null=True,blank=True,max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR)
    amount_tva = models.DecimalField(_("Montant T.V.A"),max_digits=6,decimal_places=0,max_length=10,null=True,blank=True,default=0)
    amount_ttc = models.DecimalField(_("Montant T.T.C"),max_digits=6,decimal_places=0,max_length=10,null=True,blank=True,default=0)

    def __str__(self):
        if self.number :
            return "Facture - " + self.number + " - " + self.date.strftime('%Y-%m-%d')
        else :
            return "Facture - " + self.client + " - " + self.date.strftime('%Y-%m-%d')