# core/forms.py
from django import forms
from .models import client, devis, demande, travaux, facture


class ClientForm(forms.ModelForm):
    class Meta:
            model = client
            fields = "__all__"

class DevisForm(forms.ModelForm):
    class Meta:
            model = devis
            fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Si c'est un champ date → widget DateInput avec type="date"
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(
                    attrs={
                        'class': 'form-input',
                        'type': 'date'
                    }
                )
            else:
                field.widget.attrs['class'] = 'form-input'

class DemandeForm(forms.ModelForm):
    class Meta:
            model = demande
            fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Si c'est un champ date → widget DateInput avec type="date"
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(
                    attrs={
                        'class': 'form-input',
                        'type': 'date'
                    }
                )
            else:
                field.widget.attrs['class'] = 'form-input'

class TravauxForm(forms.ModelForm):
    class Meta:
            model = travaux
            fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Si c'est un champ date → widget DateInput avec type="date"
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(
                    attrs={
                        'class': 'form-input',
                        'type': 'date'
                    }
                )
            else:
                field.widget.attrs['class'] = 'form-input'
            
class FactureForm(forms.ModelForm):
    class Meta:
            model = facture
            fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Si c'est un champ date → widget DateInput avec type="date"
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(
                    attrs={
                        'class': 'form-input',
                        'type': 'date'
                    }
                )
            else:
                field.widget.attrs['class'] = 'form-input'