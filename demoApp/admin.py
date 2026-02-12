from django.contrib import admin
from .models import client, devis, demande, travaux, facture

admin.site.register(client)
admin.site.register(devis)
admin.site.register(demande)
admin.site.register(travaux)
admin.site.register(facture)
