/* ═══════════════ MODAL MODIFIER FACTURE ═══════════════ */
function openEditFactureModal(factureId) {
    fetch(`/api/facture/${factureId}/`)
        .then(r => {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Stocker l'ID
            document.getElementById('editFactureId').value = data.id;

            // Mapping : clé API → name du champ avec prefix "edit-"
            const fields = {
                'client': data.client,
                'type': data.type,
                'number': data.number,
                'date': data.date,
                'prestation': data.prestation,
                'taxe_exo': data.taxe_exo,
                'amount_ht': data.amount_ht,
                'tva': data.tva,
                'amount_tva': data.amount_tva,
                'amount_ttc' : data.amount_ttc
            };

            const form = document.getElementById('editFactureForm');

            Object.entries(fields).forEach(([name, value]) => {
                // Le prefix "edit" → les champs s'appellent "edit-client", "edit-motif", etc.
                const el = form.querySelector(`[name="edit-${name}"]`);
                if (el) {
                    el.value = value;
                    //console.log(`✅ edit-${name} = "${value}"`);
                } else {
                    //console.warn(`⚠️ edit-${name}: INTROUVABLE`);
                }
            });

            // Ouvrir la modal
            document.getElementById('editFactureModal').classList.add('active');
            document.getElementById('editFactureBackdrop').classList.add('active');
            document.body.style.overflow = 'hidden';
        })
        .catch(err => {
            console.error('Erreur:', err);
            alert('Erreur lors du chargement');
        });
}

function closeEditFactureModal() {
    document.getElementById('editFactureModal').classList.remove('active');
    document.getElementById('editFactureBackdrop').classList.remove('active');
    document.body.style.overflow = '';
}

document.addEventListener('DOMContentLoaded', function () {

    // Fermer en cliquant sur le backdrop
    const backdrop = document.getElementById('editFactureBackdrop');
    if (backdrop) {
        backdrop.addEventListener('click', closeEditFactureModal);
    }

    // Soumission AJAX
    const form = document.getElementById('editFactureForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const factureId = document.getElementById('editFactureId').value;
            const formData = new FormData(this);

            // ══ IMPORTANT : renommer les champs "edit-xxx" → "xxx" ══
            const cleanData = new FormData();
            for (let [key, value] of formData.entries()) {
                const cleanKey = key.startsWith('edit-') ? key.replace('edit-', '') : key;
                cleanData.append(cleanKey, value);
            }

            // Nettoyer les erreurs
            this.querySelectorAll('.form-error').forEach(el => el.remove());
            this.querySelectorAll('.form-control').forEach(el => el.classList.remove('is-invalid'));

            fetch(`/api/facture/${factureId}/update/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: cleanData
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        closeEditFactureModal();
                        // Toast de succès
                        //if (typeof showToast === 'function') {
                            //showToast(data.message, 'success');
                       // } else {
                            //alert(data.message);
                        //}
                        // Recharger la page pour voir les modifs
                        setTimeout(() => location.reload(), 800);
                    } else {
                        // Afficher les erreurs de validation
                        if (data.errors) {
                            Object.entries(data.errors).forEach(([field, msgs]) => {
                                const input = form.querySelector(`[name="edit-${field}"]`);
                                if (input) {
                                    input.classList.add('is-invalid');
                                    const errSpan = document.createElement('span');
                                    errSpan.className = 'form-error';
                                    errSpan.textContent = msgs[0];
                                    input.parentNode.appendChild(errSpan);
                                }
                            });
                        }
                        if (typeof showToast === 'function') {
                            showToast(data.message || 'Erreur', 'error');
                        }
                    }
                })
                .catch(err => {
                    console.error(err);
                    alert('Erreur réseau');
                });
        });
    }
});