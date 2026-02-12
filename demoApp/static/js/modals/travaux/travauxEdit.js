/* ═══════════════ MODAL MODIFIER TRAVAUX ═══════════════ */

function openEditTravauxModal(travauxId) {
    fetch(`/api/travaux/${travauxId}/`)
        .then(r => {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .then(data => {
            if (data.error) { alert(data.error); return; }

            document.getElementById('editTravauxId').value = data.id;

            const fields = {
                'client': data.client,
                'demande': data.demande,
                'status': data.status,
                'excpectedSentDate': data.excpectedSentDate,
                'note': data.note,
                'sentDate': data.sentDate
            };

            const form = document.getElementById('editTravauxForm');
            Object.entries(fields).forEach(([name, value]) => {
                const el = form.querySelector(`[name="edit-${name}"]`) ||
                           form.querySelector(`[name="${name}"]`);
                if (el) {
                    if (el.type === 'checkbox') {
                        el.checked = !!value;
                    } else {
                        el.value = value;
                    }
                } else {
                    console.warn(`⚠️ travaux ${name}: INTROUVABLE`);
                }
            });

            // Checkbox sent
            const sentCb = form.querySelector('[name="edit-sent"]') ||
                           form.querySelector('[name="sent"]');
            if (sentCb) sentCb.checked = !!data.sent;

            // ═══ OUVRIR : overlay + modal ═══
            document.getElementById('editTravauxOverlay').classList.add('active');
            document.getElementById('editTravauxModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        })
        .catch(err => {
            console.error(err);
            alert('Erreur lors du chargement du travaux');
        });
}

function closeEditTravauxModal() {
    document.getElementById('editTravauxModal').classList.remove('active');
    document.getElementById('editTravauxOverlay').classList.remove('active');
    document.body.style.overflow = '';
}


// Soumission du formulaire
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('editTravauxForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const travauxId = document.getElementById('editTravauxId').value;
            const formData = new FormData(form);

            // Retirer le prefix "edit-" pour Django
            const cleanData = new FormData();
            for (const [key, value] of formData.entries()) {
                const cleanKey = key.replace('edit-', '');
                cleanData.append(cleanKey, value);
            }

            // Gérer le checkbox "sent" (non envoyé si non coché)
            const sentCheckbox = form.querySelector('[name="edit-sent"]');
            if (sentCheckbox && !sentCheckbox.checked) {
                cleanData.set('sent', 'false');
            }

            // Ajouter le CSRF token
            const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;
            cleanData.set('csrfmiddlewaretoken', csrfToken);

            // Retirer erreurs précédentes
            form.querySelectorAll('.form-error').forEach(el => el.remove());
            form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

            fetch(`/api/travaux/${travauxId}/update/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: cleanData
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        closeEditTravauxModal();
                        if (typeof showToast === 'function') {
                            showToast(data.message, 'success');
                        } else {
                            alert(data.message);
                        }
                        setTimeout(() => location.reload(), 800);
                    } else {
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