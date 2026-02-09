# core/forms.py
from django import forms
from .models import client, devis, demande


class ClientForm(forms.ModelForm):
    class Meta:
            model = client
            fields = "__all__"

class DevisForm(forms.ModelForm):
    class Meta:
            model = devis
            fields = "__all__"

class DemandeForm(forms.ModelForm):
    class Meta:
            model = demande
            fields = "__all__"
