from django.shortcuts import render, redirect, get_object_or_404
from .models import client, demande, devis
from .forms import ClientForm, DemandeForm, DevisForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def clients_list(request):
    clients = client.objects.all().order_by('-id')
    client_form = ClientForm()
    edit_form = ClientForm(prefix='edit')  # ← préfixe pour éviter les conflits d'id

    return render(request, 'client/clients.html', {
        'clients': clients,
        'client_form': client_form,
        'edit_form': edit_form,
    })


def client_detail_api(request, pk):
    try:
        obj = client.objects.get(pk=pk)
    except client.DoesNotExist:
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
                'reference': getattr(d, 'reference', f'Delande #{d.id}'),
                'type': getattr(d, 'type', ''),
                'description': getattr(d, 'description', ''),
                'excpectedVisitDate': d.excpectedVisitDate.strftime('%d/%m/%Y') if getattr(d, 'excpectedVisitDate', None) else '',
            })
    except Exception as e:
        print(f"Erreur demandes: {e}")

    return JsonResponse(data)


def dashboard(request):
    devis_par_statut = (
        devis.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
    )
    statut_labels = [item['status'] for item in devis_par_statut]
    statut_counts = [item['count'] for item in devis_par_statut]
    dates_visites = list(demande.objects.values_list('excpectedVisitDate', flat=True))
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
        'client_form': ClientForm(),
        'demande_form': DemandeForm(),
        'devis_form': DevisForm(),
        'statut_labels': statut_labels,
        'statut_counts': statut_counts,
        'dates_visites_json': dates_visites_json,
        'dates_devis_json': date_devis_json,        
        'edit_form':ClientForm(prefix='edit'),
        'edit_demande_form': DemandeForm(prefix='edit'),
        'edit_devis_form': DevisForm(prefix='edit'),
    }
    return render(request, 'dashboard/index.html', context)


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
def devis_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DevisForm(request.POST)
        if form.is_valid():
            new_devis = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Devis "{new_devis}" créé avec succès !',
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
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DemandeForm(request.POST)
        if form.is_valid():
            new_demande = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Demande "{new_demande}" créée avec succès !',
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
            obj = client.objects.get(pk=pk)
        except client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Client introuvable'}, status=404)

        form = ClientForm(request.POST, instance=obj)
        if form.is_valid():
            updated_client = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Client "{updated_client}" modifié avec succès !',
                'client': {
                    'id': updated_client.id,
                    'firstName': updated_client.firstName,
                    'lastName': updated_client.lastName,
                    'fullName': updated_client.full_name,
                    'type': updated_client.type,
                    'email': updated_client.email,
                    'phone': updated_client.phone,
                    'postal_address': updated_client.postal_address,
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
        obj = client.objects.get(id=client_id)
        client_name = f"{obj.firstName} {obj.lastName}"
        obj.delete()
        return JsonResponse({'success': True, 'message': f'Client "{client_name}" supprimé'})
    except obj.DoesNotExist:
        return JsonResponse({'error': 'Client introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST   
def demande_delete(request, pk):
    obj = get_object_or_404(demande, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Demande supprimée avec succès !")
    return redirect('dashboard')

def demande_detail_api(request, pk):
    try:
        obj = demande.objects.get(pk=pk)
    except demande.DoesNotExist:
        return JsonResponse({'error': 'Demande introuvable'}, status=404)

    data = {
        'id': obj.id,
        'client': obj.client.id,          # ← l'ID, pas l'objet !
        'demandeDate': obj.demandeDate.strftime('%Y-%m-%d') if obj.demandeDate else '',
        'motif': obj.motif or '',
        'type': obj.type or '',
        'excpectedVisitDate': obj.excpectedVisitDate.strftime('%Y-%m-%d') if obj.excpectedVisitDate else '',
        'clientAvailibity': obj.clientAvailibity or '',
        'realVisitDate': obj.realVisitDate.strftime('%Y-%m-%d') if obj.realVisitDate else '',
    }
    return JsonResponse(data)

@require_POST
def demande_update(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            obj = demande.objects.get(pk=pk)
        except demande.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Demande introuvable'}, status=404)

        form = DemandeForm(request.POST, instance=obj)
        if form.is_valid():
            updated = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Demande "{updated}" modifiée avec succès !',
                'demande': {
                    'id': updated.id,
                    'client': updated.client.full_name,        # ← string pour affichage
                    'client_id': updated.client.id,
                    'demandeDate': updated.demandeDate.strftime('%d/%m/%Y') if updated.demandeDate else '',
                    'motif': updated.motif,
                    'type': updated.type,
                    'excpectedVisitDate': updated.excpectedVisitDate.strftime('%d/%m/%Y') if updated.excpectedVisitDate else '',
                    'clientAvailibity': updated.clientAvailibity,
                    'realVisitDate': updated.realVisitDate.strftime('%d/%m/%Y') if updated.realVisitDate else '',
                },
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erreur de validation',
                'errors': form.errors,
            }, status=400)

    return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)

def devis_detail_api(request, pk):
    try:
        obj = devis.objects.get(pk=pk)
    except devis.DoesNotExist:
        return JsonResponse({'error': 'Devis introuvable'}, status=404)

    data = {
        'id': obj.id,
        'client': obj.client.id,
        'demande': obj.demande.id if obj.demande else '',
        'status': obj.status or '',
        'excpectedSentDate': obj.excpectedSentDate.strftime('%Y-%m-%d') if obj.excpectedSentDate else '',
        'comment': obj.comment or '',
        'sent': obj.sent,
        'realSentDate': obj.realSentDate.strftime('%Y-%m-%d') if obj.realSentDate else '',
    }
    return JsonResponse(data)


@require_POST
def devis_update(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            obj = devis.objects.get(pk=pk)
        except devis.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Devis introuvable'}, status=404)

        # Retirer le prefix "edit-" des clés POST
        post_data = {}
        for key, value in request.POST.items():
            clean_key = key.replace('edit-', '')
            post_data[clean_key] = value

        # Gérer le checkbox "sent" (absent du POST si non coché)
        if 'sent' not in post_data:
            post_data['sent'] = False

        from django.http import QueryDict
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
    obj = get_object_or_404(devis, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Devis supprimé avec succès !")
    return redirect('dashboard')

