from django.contrib import admin
from .models import client, devis, demande, travaux

admin.site.register(client)
admin.site.register(devis)
admin.site.register(demande)
admin.site.register(travaux)
