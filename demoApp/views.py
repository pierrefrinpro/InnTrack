from django.shortcuts import render, get_object_or_404
from .models import client, demande, devis
from .forms import ClientForm, DemandeForm, DevisForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder

def client_detail(request, client_id):
    cl = client.objects.get(id=client_id)
    return render(request, 'client/client_detail.html', {'client': cl})


def dashboard(request):
    devis_par_statut = (
        devis.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
    )
    statut_labels = [item['status'] for item in devis_par_statut]
    statut_counts = [item['count'] for item in devis_par_statut]
    dates_visites = list(demande.objects.values_list('excpectedVisitDate',flat=True))
    dates_visites_json = json.dumps(
        [d.strftime('%Y-%m-%d') for d in dates_visites if d],
        cls=DjangoJSONEncoder
    )
    date_devis = list(devis.objects.values_list('excpectedSentDate', flat=True))
    date_devis_json = json.dumps(
        [d.strftime('%Y-%m-%d') for d in date_devis if d],
        cls=DjangoJSONEncoder
    )

    context = {
        'active_page': 'dashboard',
        'clients_count': client.objects.count(),
        'demandes_count': demande.objects.count(),
        'devis_count': devis.objects.count(),
        'clients': client.objects.all(),
        'demandes': demande.objects.all(),
        'devis': devis.objects.all(),
        'all_clients': client.objects.all().order_by('lastName'),
        'all_clients': [],
        'client_form': ClientForm(),
        'demande_form': DemandeForm(),
        'devis_form': DevisForm(),
        'statut_labels': statut_labels,
        'statut_counts': statut_counts,
        'dates_visites_json': dates_visites_json,
        'dates_devis_json': date_devis_json,
    }
    return render(request, 'dashboard/index.html', context)


@require_POST
def client_create(request):
    """Création client via AJAX."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Client "{client}" créé avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)

    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def devis_create(request):
    """Création demande via AJAX."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DevisForm(request.POST)
        if form.is_valid():
            devis = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Devis "{devis}" créé avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)

    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)

@require_POST
def demande_create(request):
    """Création demande via AJAX."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DemandeForm(request.POST)
        if form.is_valid():
            demande = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Demande "{demande}" créée avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)

    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)

def client_detail_api(request, pk):
    """Retourne les devis et visites d'un client en JSON."""
    client = get_object_or_404(client, pk=pk)
    
    devis = devis.objects.filter(client=client)
    demandes = demande.objects.filter(client=client)
    
    return JsonResponse({
        'success': True,
        'client': {
            'id': client.pk,
            'firstName': client.firstName,
            'lastName': client.lastName,
            'type': client.type,
            'email': client.email,
            'phone': client.phone,
        },
        'devis': list(devis.values(
            'id', 'status', 'datePrevisionEnvoi', 'envoyee'
        )),
        'demandes': list(demandes.values(
            'id', 'type', 'dateVisite'
        )),
    })