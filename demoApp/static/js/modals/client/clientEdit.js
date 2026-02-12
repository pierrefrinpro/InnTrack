/* ═══════════════ MODAL MODIFIER CLIENT ═══════════════ */
function openEditClientModal(clientId) {
    fetch(`/api/client/${clientId}/`)
        .then(r => {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const form = document.getElementById('editClientForm');
            document.getElementById('editClientId').value = data.id;

            const fields = {
                'lastName': data.lastName || '',
                'firstName': data.firstName || '',
                'email': data.email || '',
                'phone': data.phone || '',
                'postal_address': data.postal_address || '',
                'type': data.type || '',
            };

            Object.entries(fields).forEach(([name, value]) => {
                // Chercher UNIQUEMENT dans le form edit
                const el =
                    form.querySelector(`[name="edit-${name}"]`) ||
                    form.querySelector(`[name="${name}"]`) ||
                    form.querySelector(`input[id*="${name}"]`) ||
                    form.querySelector(`select[id*="${name}"]`);

                if (el) {
                    el.value = value;
                    console.log(`✅ ${name} = "${value}" → ${el.id || el.name}`);
                } else {
                    console.warn(`⚠️ ${name}: INTROUVABLE dans editClientForm`);
                }
            });

            document.getElementById('editClientModal').classList.add('active');
            document.getElementById('editClientBackdrop').classList.add('active');
            document.body.style.overflow = 'hidden';
        })
        .catch(err => {
            console.error('Erreur:', err);
            alert('Erreur lors du chargement');
        });
}

function closeEditClientModal() {
    document.getElementById('editClientModal').classList.remove('active');
    document.getElementById('editClientBackdrop').classList.remove('active');
    document.body.style.overflow = '';
}

/* ═══════ Tout le reste attend que le DOM soit prêt ═══════ */
document.addEventListener('DOMContentLoaded', function() {

    // Fermer en cliquant sur le backdrop
    const backdrop = document.getElementById('editClientBackdrop');
    if (backdrop) {
        backdrop.addEventListener('click', closeEditClientModal);
    }

    // Soumission AJAX
    const form = document.getElementById('editClientForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const clientId = document.getElementById('editClientId').value;
            const formData = new FormData(this);

            // Nettoyer les erreurs précédentes
            this.querySelectorAll('.form-error').forEach(el => el.remove());
            this.querySelectorAll('.form-control').forEach(el => el.classList.remove('is-invalid'));

            fetch(`/api/client/${clientId}/update/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData,
            })
            .then(r => r.json().then(data => ({ ok: r.ok, data })))
            .then(({ ok, data }) => {
                if (ok && data.success) {
                    closeEditClientModal();
                    setTimeout(() => location.reload(), 300);
                } else {
                    // Afficher les erreurs par champ
                    if (data.errors) {
                        Object.entries(data.errors).forEach(([field, msgs]) => {
                            const input = document.getElementById(`edit-id_${field}`);
                            if (input) {
                                input.classList.add('is-invalid');
                                const errDiv = document.createElement('div');
                                errDiv.className = 'form-error';
                                errDiv.textContent = msgs.join(', ');
                                input.parentNode.appendChild(errDiv);
                            }
                        });
                    }
                    alert(data.message || 'Erreur lors de la sauvegarde');
                }
            })
            .catch(() => alert('Erreur réseau'));
        });
    }
});