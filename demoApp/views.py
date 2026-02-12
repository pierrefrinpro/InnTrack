from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

from .models import client as Client, demande as Demande, devis as Devis, travaux as Travaux, facture as Facture
from .forms import ClientForm, DemandeForm, DevisForm, TravauxForm, FactureForm
import json


# ═══════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════

def dashboard(request):
    devis_par_statut = (
        Devis.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
    )
    statut_labels = [item['status'] for item in devis_par_statut]
    statut_counts = [item['count'] for item in devis_par_statut]

    dates_visites = list(Demande.objects.values_list('excpectedVisitDate', flat=True))
    dates_visites_json = json.dumps(
        [d.strftime('%Y-%m-%d') for d in dates_visites if d],
        cls=DjangoJSONEncoder
    )
    date_devis = list(Devis.objects.values_list('excpectedSentDate', flat=True))
    date_devis_json = json.dumps(
        [d.strftime('%Y-%m-%d') for d in date_devis if d],
        cls=DjangoJSONEncoder
    )

    context = {
        'active_page': 'dashboard',
        'clients_count': Client.objects.count(),
        'demandes_count': Demande.objects.filter(realVisitDate__isnull=True).count(),
        'devis_count': Devis.objects.filter(sent=False).count(),
        'clients': Client.objects.all(),
        'demandes': Demande.objects.filter(realVisitDate__isnull=True),
        'devis': Devis.objects.filter(sent=False),
        'all_clients': Client.objects.all().order_by('lastName'),
        'client_form': ClientForm(),
        'demande_form': DemandeForm(),
        'devis_form': DevisForm(),
        'statut_labels': statut_labels,
        'statut_counts': statut_counts,
        'dates_visites_json': dates_visites_json,
        'dates_devis_json': date_devis_json,
        'edit_form': ClientForm(prefix='edit'),
        'edit_demande_form': DemandeForm(prefix='edit'),
        'edit_devis_form': DevisForm(prefix='edit'),
    }
    return render(request, 'dashboard/index.html', context)


# ═══════════════════════════════════════════════════════
#  CLIENTS
# ═══════════════════════════════════════════════════════

def clients_list(request):
    all_clients = Client.objects.all().order_by('-id')
    return render(request, 'client/clients.html', {        
        'active_page': 'clients',
        'clients': all_clients,
        'client_form': ClientForm(),
        'edit_form': ClientForm(prefix='edit'),
    })


def client_detail_api(request, pk):
    try:
        obj = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client introuvable'}, status=404)

    data = {
        'id': obj.id,
        'firstName': obj.firstName,
        'lastName': obj.lastName,
        'fullName': obj.full_name,
        'type': obj.type,
        'email': obj.email,
        'phone': obj.phone,
        'postal_address': obj.postal_address,
        'devis': [],
        'demandes': [],
    }

    try:
        for d in obj.devis_set.all():
            data['devis'].append({
                'id': d.id,
                'reference': getattr(d, 'reference', f'Devis #{d.id}'),
                'status': getattr(d, 'status', ''),
                'montant': float(d.montant) if getattr(d, 'montant', None) else None,
                'datePrevisionEnvoi': d.excpectedSentDate.strftime('%d/%m/%Y') if getattr(d, 'excpectedSentDate', None) else '',
            })
    except Exception as e:
        print(f"Erreur devis: {e}")

    try:
        for d in obj.demande_set.all():
            data['demandes'].append({
                'id': d.id,
                'reference': getattr(d, 'reference', f'Demande #{d.id}'),
                'type': getattr(d, 'type', ''),
                'description': getattr(d, 'description', ''),
                'excpectedVisitDate': d.excpectedVisitDate.strftime('%d/%m/%Y') if getattr(d, 'excpectedVisitDate', None) else '',
            })
    except Exception as e:
        print(f"Erreur demandes: {e}")

    return JsonResponse(data)


@require_POST
def client_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ClientForm(request.POST)
        if form.is_valid():
            new_client = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Client "{new_client}" créé avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def client_update(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            obj = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Client introuvable'}, status=404)

        form = ClientForm(request.POST, instance=obj)
        if form.is_valid():
            updated = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Client "{updated}" modifié avec succès !',
                'client': {
                    'id': updated.id,
                    'firstName': updated.firstName,
                    'lastName': updated.lastName,
                    'fullName': updated.full_name,
                    'type': updated.type,
                    'email': updated.email,
                    'phone': updated.phone,
                    'postal_address': updated.postal_address,
                },
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def api_client_delete(request, client_id):
    try:
        obj = Client.objects.get(id=client_id)
        client_name = f"{obj.firstName} {obj.lastName}"
        obj.delete()
        return JsonResponse({'success': True, 'message': f'Client "{client_name}" supprimé'})
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ═══════════════════════════════════════════════════════
#  DEMANDES
# ═══════════════════════════════════════════════════════

def demandes_list_view(request):
    qs = Demande.objects.select_related('client').all().order_by('-id')
    all_clients = Client.objects.all().order_by('lastName')

    # Filtres
    f_client = request.GET.get('client', '')
    f_type = request.GET.get('type', '')
    f_date_from = request.GET.get('date_from', '')
    f_date_to = request.GET.get('date_to', '')

    if f_client:
        qs = qs.filter(client_id=f_client)
    if f_type:
        qs = qs.filter(type=f_type)
    if f_date_from:
        qs = qs.filter(excpectedVisitDate__gte=f_date_from)
    if f_date_to:
        qs = qs.filter(excpectedVisitDate__lte=f_date_to)

    # Récupérer les choices du modèle
    type_choices = []
    try:
        type_choices = Demande._meta.get_field('type').choices or []
    except Exception:
        pass

    context = {
        'active_page': 'demandes',
        'demandes': qs,
        'clients': all_clients,
        'type_choices': type_choices,
        'demande_form': DemandeForm(),
        'edit_demande_form': DemandeForm(prefix='edit'),
        'current_filters': {
            'client': f_client,
            'type': f_type,
            'date_from': f_date_from,
            'date_to': f_date_to,
        },
    }
    return render(request, 'demande/demande_list.html', context)


def demande_detail_api(request, pk):
    """API unique pour le panel latéral ET le pré-remplissage edit."""
    try:
        obj = Demande.objects.select_related('client').get(pk=pk)
    except Demande.DoesNotExist:
        return JsonResponse({'error': 'Demande introuvable'}, status=404)

    # Devis liés
    devis_lies = []
    for dv in Devis.objects.filter(demande=obj):
        devis_lies.append({
            'id': dv.id,
            'status': dv.status,
            'excpectedSentDate': dv.excpectedSentDate.strftime('%d/%m/%Y') if dv.excpectedSentDate else '',
            'sent': dv.sent,
        })

    data = {
        'id': obj.id,
        # Pour pré-remplissage formulaire (valeurs brutes)
        'client': obj.client_id,
        'demandeDate': obj.demandeDate.strftime('%Y-%m-%d') if obj.demandeDate else '',
        'motif': obj.motif or '',
        'type': obj.type or '',
        'excpectedVisitDate': obj.excpectedVisitDate.strftime('%Y-%m-%d') if obj.excpectedVisitDate else '',
        'clientAvailibity': obj.clientAvailibity or '',
        'realVisitDate': obj.realVisitDate.strftime('%Y-%m-%d') if obj.realVisitDate else '',
        # Pour affichage panel (valeurs formatées)
        'client_name': str(obj.client) if obj.client else '',
        'client_phone': getattr(obj.client, 'phone', '') or '',
        'client_email': getattr(obj.client, 'email', '') or '',
        'type_display': obj.get_type_display() if hasattr(obj, 'get_type_display') else obj.type,
        'devis': devis_lies,
    }
    return JsonResponse(data)


@require_POST
def demande_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DemandeForm(request.POST)
        if form.is_valid():
            new_obj = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Demande "{new_obj}" créée avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def demande_update(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            obj = Demande.objects.get(pk=pk)
        except Demande.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Demande introuvable'}, status=404)

        form = DemandeForm(request.POST, instance=obj)
        if form.is_valid():
            updated = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Demande "{updated}" modifiée avec succès !',
                'demande': {
                    'id': updated.id,
                    'client': updated.client.full_name,
                    'client_id': updated.client.id,
                    'demandeDate': updated.demandeDate.strftime('%d/%m/%Y') if updated.demandeDate else None,
                    'motif': updated.motif,
                    'type': updated.type,
                    'excpectedVisitDate': updated.excpectedVisitDate.strftime('%d/%m/%Y') if updated.excpectedVisitDate else None,
                    'clientAvailibity': updated.clientAvailibity,
                    'realVisitDate': updated.realVisitDate.strftime('%d/%m/%Y') if updated.realVisitDate else None,
                },
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def demande_delete(request, pk):
    obj = get_object_or_404(Demande, pk=pk)
    obj.delete()
    # Si AJAX, retourner JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Demande supprimée'})
    messages.success(request, "Demande supprimée avec succès !")
    return redirect('dashboard')


# ═══════════════════════════════════════════════════════
#  DEVIS
# ═══════════════════════════════════════════════════════

def devis_list_view(request):
    qs = Devis.objects.select_related('client', 'demande').all().order_by('-id')
    all_clients = Client.objects.all().order_by('lastName')

    # Filtres
    f_client = request.GET.get('client', '')
    f_status = request.GET.get('status', '')
    f_sent = request.GET.get('sent', '')
    f_date_from = request.GET.get('date_from', '')
    f_date_to = request.GET.get('date_to', '')

    if f_client:
        qs = qs.filter(client_id=f_client)
    if f_status:
        qs = qs.filter(status=f_status)
    if f_sent == 'true':
        qs = qs.filter(sent=True)
    elif f_sent == 'false':
        qs = qs.filter(sent=False)
    if f_date_from:
        qs = qs.filter(excpectedSentDate__gte=f_date_from)
    if f_date_to:
        qs = qs.filter(excpectedSentDate__lte=f_date_to)

    # Récupérer les choices du modèle
    status_choices = []
    try:
        status_choices = Devis._meta.get_field('status').choices or []
    except Exception:
        pass

    context = {
        'active_page': 'devis',
        'devis_list': qs,  # ← "devis_list" et pas "devis" pour éviter conflit
        'clients': all_clients,
        'status_choices': status_choices,
        'devis_form': DevisForm(),
        'edit_devis_form': DevisForm(prefix='edit'),
        'current_filters': {
            'client': f_client,
            'status': f_status,
            'sent': f_sent,
            'date_from': f_date_from,
            'date_to': f_date_to,
        },
    }
    return render(request, 'devis/devis_list.html', context)


def devis_detail_api(request, pk):
    """API unique pour le panel latéral ET le pré-remplissage edit."""
    try:
        obj = Devis.objects.select_related('client', 'demande').get(pk=pk)
    except Devis.DoesNotExist:
        return JsonResponse({'error': 'Devis introuvable'}, status=404)

    data = {
        'id': obj.id,
        # Pour pré-remplissage formulaire (valeurs brutes)
        'client': obj.client_id,
        'demande': obj.demande_id if obj.demande_id else '',
        'status': obj.status or '',
        'excpectedSentDate': obj.excpectedSentDate.strftime('%Y-%m-%d') if obj.excpectedSentDate else '',
        'comment': obj.comment or '',
        'sent': obj.sent,
        'realSentDate': obj.realSentDate.strftime('%Y-%m-%d') if obj.realSentDate else '',
        # Pour affichage panel (valeurs formatées)
        'client_name': str(obj.client) if obj.client else '',
        'client_phone': getattr(obj.client, 'phone', '') or '',
        'client_email': getattr(obj.client, 'email', '') or '',
        'demande_name': str(obj.demande) if obj.demande else '',
        'status_display': obj.get_status_display() if hasattr(obj, 'get_status_display') else obj.status,
        'excpectedSentDate_display': obj.excpectedSentDate.strftime('%d/%m/%Y') if obj.excpectedSentDate else '',
        'realSentDate_display': obj.realSentDate.strftime('%d/%m/%Y') if obj.realSentDate else '',
    }
    return JsonResponse(data)


@require_POST
def devis_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DevisForm(request.POST)
        if form.is_valid():
            new_obj = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Devis "{new_obj}" créé avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)

@require_POST
def devis_update(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            obj = Devis.objects.get(pk=pk)
        except Devis.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Devis introuvable'}, status=404)

        # Retirer le prefix "edit-" des clés POST
        from django.http import QueryDict
        post_data = {}
        for key, value in request.POST.items():
            clean_key = key.replace('edit-', '')
            post_data[clean_key] = value

        if 'sent' not in post_data:
            post_data['sent'] = False

        cleaned_post = QueryDict(mutable=True)
        cleaned_post.update(post_data)

        form = DevisForm(cleaned_post, instance=obj)
        if form.is_valid():
            updated = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Devis "{updated}" modifié avec succès !',
                'devis': {
                    'id': updated.id,
                    'client': updated.client.full_name,
                    'client_id': updated.client.id,
                    'status': updated.status,
                    'excpectedSentDate': updated.excpectedSentDate.strftime('%d/%m/%Y') if updated.excpectedSentDate else '',
                    'sent': updated.sent,
                    'comment': updated.comment,
                    'realSentDate': updated.realSentDate.strftime('%d/%m/%Y') if updated.realSentDate else '',
                },
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def devis_delete(request, pk):
    obj = get_object_or_404(Devis, pk=pk)
    obj.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Devis supprimé'})
    messages.success(request, "Devis supprimé avec succès !")
    return redirect('dashboard')

# ═══════════════════════════════════════════════════════
#  TRAVAUX
# ═══════════════════════════════════════════════════════

def travaux_list_view(request):
    qs = Travaux.objects.select_related('client', 'demande', 'devis').all().order_by('-id')
    all_clients = Client.objects.all().order_by('lastName')

    # Filtres
    f_client = request.GET.get('client', '')
    f_demande = request.GET.get('demande', '')
    f_devis = request.GET.get('devis', '')
    f_terminated = request.GET.get('terminated', '')

    if f_client:
        qs = qs.filter(client_id=f_client)
    if f_demande:
        qs = qs.filter(demande=f_demande)
    if f_devis :
        qs = qs.filter(devis=f_devis)
    elif f_terminated :
        qs = qs.filter(terminated=f_terminated)

    context = {
        'active_page': 'travaux',
        'travaux_list': qs, 
        'clients': all_clients,
        'travaux_form': TravauxForm(),
        'edit_travaux_form': TravauxForm(prefix='edit'),
        'current_filters': {
            'client': f_client,
            'demande': f_demande,
            'devis': f_devis,
            'terminated': f_terminated,
        },
    }
    return render(request, 'travaux/travaux_list.html', context)


def travaux_detail_api(request, pk):
    """API unique pour le panel latéral ET le pré-remplissage edit."""
    try:
        obj = Travaux.objects.select_related('client', 'demande', 'devis').get(pk=pk)
    except Travaux.DoesNotExist:
        return JsonResponse({'error': 'Travaux introuvable'}, status=404)

    data = {
        'id': obj.id,
        # Pour pré-remplissage formulaire (valeurs brutes)
        'client': obj.client_id,
        'demande': obj.demande_id if obj.demande_id else '',
        'devis': obj.devis_id if obj.devis_id else '',
        'startdate': obj.startDate.strftime('%Y-%m-%d') if obj.startDate else None,
        'terminated': obj.terminated,
        'endDate': obj.endDate.strftime('%Y-%m-%d') if obj.endDate else None,
        # Pour affichage panel (valeurs formatées)
        'client_name': str(obj.client) if obj.client else '',
        'client_phone': getattr(obj.client, 'phone', '') or '',
        'client_email': getattr(obj.client, 'email', '') or '',
        'demande_name': str(obj.demande) if obj.demande else '',
        'devis_name': str(obj.devis) if obj.devis else '',
        'terminated': str(obj.terminated) if obj.terminated else '',
        'startdate_display': obj.startDate.strftime('%d/%m/%Y') if obj.startDate else None,
        'endDate_display': obj.endDate.strftime('%d/%m/%Y') if obj.endDate else None,
    }
    return JsonResponse(data)


@require_POST
def travaux_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = TravauxForm(request.POST)
        if form.is_valid():
            new_obj = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Travaux "{new_obj}" créé avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def travaux_update(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            obj = Travaux.objects.get(pk=pk)
        except Travaux.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Travaux introuvable'}, status=404)

        # Retirer le prefix "edit-" des clés POST
        from django.http import QueryDict
        post_data = {}
        for key, value in request.POST.items():
            clean_key = key.replace('edit-', '')
            post_data[clean_key] = value

        if 'sent' not in post_data:
            post_data['sent'] = False

        cleaned_post = QueryDict(mutable=True)
        cleaned_post.update(post_data)

        form = TravauxForm(cleaned_post, instance=obj)
        if form.is_valid():
            updated = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Travaux "{updated}" modifié avec succès !',
                'travaux': {
                    'id': updated.id,
                    'client': updated.client.full_name,
                    'client_id': updated.client.id,
                    'demande': updated.demande,
                    'devis': updated.devis,
                    'startdate': updated.startDate.strftime('%d/%m/%Y') if updated.startDate else None,
                    'terminated': updated.terminated,
                    'endDate': updated.ednDate.strftime('%d/%m/%Y') if updated.endDate else None,
                },
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def travaux_delete(request, pk):
    obj = get_object_or_404(Travaux, pk=pk)
    obj.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Travaux supprimé'})
    messages.success(request, "Travaux supprimé avec succès !")
    return redirect('dashboard')

# ═══════════════════════════════════════════════════════
#  FACTURES
# ═══════════════════════════════════════════════════════

def factures_list_view(request):
    ff = Facture.objects.all().order_by('id')

    # Filtres
    f_date_from = request.GET.get('date_from', '')
    f_date_to = request.GET.get('date_to', '')
    f_client = request.GET.get('client', '')
    f_type = request.GET.get('type', '')

    if f_client:
        ff = ff.filter(client=f_client)
    if f_type :
        ff = ff.filter(type=f_type)    
    if f_date_from:
        ff = ff.filter(date__gte=f_date_from)
    elif f_date_to:
        ff = ff.filter(date__lte=f_date_to)

    # Récupérer les choices du modèle
    type_choices = []
    try:
        type_choices = Facture._meta.get_field('type').choices or []
    except Exception:
        pass

    context = {
        'active_page': 'facture',
        'facture_list': ff, 
        'type_choices' : type_choices,
        'facture_form': FactureForm(),
        'edit_facture_form': FactureForm(prefix='edit'),
        'current_filters': {
            'client': f_client,
            'type': f_type,
            'date_from': f_date_from,
            'date_to': f_date_to,
        },
    }
    return render(request, 'facture/facture_list.html', context)


def facture_detail_api(request, pk):
    """API unique pour le panel latéral ET le pré-remplissage edit."""
    try:
        obj = Facture.objects.get(pk=pk)
    except Facture.DoesNotExist:
        return JsonResponse({'error': 'Facture introuvable'}, status=404)

    data = {
        'id': obj.id,
        # Pour pré-remplissage formulaire (valeurs brutes)
        'client': obj.client,
        'type': obj.type,
        'number': obj.number if obj.number else '',
        'date': obj.date.strftime('%Y-%m-%d') if obj.date else None,
        'prestation': obj.prestation,
        'taxe_exo': obj.taxe_exo,
        'amount_ht': obj.amount_ht,
        'tva': obj.tva,
        'amount_tva': obj.amount_tva,
        'amount_ttc' : obj.amount_ttc
    }
    return JsonResponse(data)


@require_POST
def facture_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = FactureForm(request.POST)
        if form.is_valid():
            new_obj = form.save()
            return JsonResponse({
                'success': True,
                #'message': f'Facture "{new_obj}" créé avec succès !',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def facture_update(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            obj = Facture.objects.get(pk=pk)
        except Facture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Facture introuvable'}, status=404)

        # Retirer le prefix "edit-" des clés POST
        from django.http import QueryDict
        post_data = {}
        for key, value in request.POST.items():
            clean_key = key.replace('edit-', '')
            post_data[clean_key] = value

        if 'sent' not in post_data:
            post_data['sent'] = False

        cleaned_post = QueryDict(mutable=True)
        cleaned_post.update(post_data)

        form = FactureForm(cleaned_post, instance=obj)
        if form.is_valid():
            if form.instance.amount_ht != 0 and form.instance.tva != 0 :
                form.instance.amount_tva = form.instance.amount_ht * (form.instance.tva/100)
                form.instance.amount_ttc = form.instance.amount_ht + form.instance.amount_tva
            updated = form.save()
            return JsonResponse({
                'success': True,
                'facture': {
                    'id': updated.id,
                    'client': updated.client,
                    'type': updated.type,
                    'number': updated.number if updated.number else '',
                    'date': updated.date.strftime('%Y-%m-%d') if updated.date else None,
                    'prestation': updated.prestation,
                    'taxe_exo': updated.taxe_exo,
                    'amount_ht': updated.amount_ht,
                    'tva': updated.tva,
                    'amount_tva': updated.amount_tva,
                    'amount_ttc' : updated.amount_ttc
                },
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)


@require_POST
def facture_delete(request, pk):
    obj = get_object_or_404(Facture, pk=pk)
    obj.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Facture supprimée'})
    #messages.success(request, "Facture supprimée avec succès !")
    return redirect('factures_list')


def planning_view(request):
    demandes = Demande.objects.select_related('client').all()
    devis = Devis.objects.select_related('client').all()
    travaux = Travaux.objects.select_related('client').all()

    # Construire les événements
    events = []

    for d in demandes:
        if d.excpectedVisitDate:
            events.append({
                'id': f'demande-{d.id}',
                'title': f'{d.client.firstName} {d.client.lastName} - {d.type}',
                'date': d.excpectedVisitDate.strftime('%Y-%m-%d'),
                'type': 'demande',
                'client': f'{d.client.firstName} {d.client.lastName}',
                'client_id': d.client.id,
                'type_demande': f'{d.type}',
            })

    for dv in devis:
        if dv.excpectedSentDate:
            events.append({
                'id': f'devis-{dv.id}',
                'title': f'{dv.client.firstName} {dv.client.lastName}- Devis #{dv.id}',
                'date': dv.excpectedSentDate.strftime('%Y-%m-%d'),
                'type': 'devis',
                'status': dv.status,
                'client': f'{dv.client.firstName} {dv.client.lastName}',
                'client_id': dv.client.id
            })

    for trav in travaux:
        if trav.startDate:
            events.append({
                'id': f'travaux-{trav.id}',
                'title': f'{trav.client.firstName} {trav.client.lastName}- Travaux #{trav.id}',
                'date': trav.startDate.strftime('%Y-%m-%d'),
                'type': 'travaux',
                'client': f'{trav.client.firstName} {trav.client.lastName}',
                'client_id': trav.client.id
            })

    # Listes pour filtres
    clients = Client.objects.all().order_by('lastName')
    type_devis = Devis.type_of_devis
    types_demande = Demande.type_of_demande

    import json
    context = {
        'active_page': 'planning',
        'events_json': json.dumps(events, default=str),
        'clients': clients,
        'type_devis': type_devis,
        'types_demande': types_demande,
    }
    return render(request, 'planning/planning.html', context)
