/* ═══════════════ MODAL MODIFIER DEVIS ═══════════════ */

function openEditDevisModal(devisId) {
    fetch(`/api/devis/${devisId}/`)
        .then(r => {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const form = document.getElementById('editDevisForm');
            document.getElementById('editDevisId').value = data.id;

            const fields = {
                'client':           data.client || '',
                'demande':          data.demande || '',
                'status':           data.status || '',
                'excpectedSentDate': data.excpectedSentDate || '',
                'comment':          data.comment || '',
                'sent':             data.sent,
                'realSentDate':     data.realSentDate || '',
            };

            Object.entries(fields).forEach(([name, value]) => {
                const el =
                    form.querySelector(`[name="edit-${name}"]`) ||
                    form.querySelector(`[name="${name}"]`);

                if (el) {
                    if (el.type === 'checkbox') {
                        el.checked = !!value;
                    } else {
                        el.value = value;
                    }
                    console.log(`✅ devis ${name} = "${value}"`);
                } else {
                    console.warn(`⚠️ devis ${name}: INTROUVABLE`);
                }
            });

            document.getElementById('editDevisModal').classList.add('active');
        })
        .catch(err => {
            console.error(err);
            alert('Erreur lors du chargement du devis');
        });
}

function closeEditDevisModal() {
    document.getElementById('editDevisModal').classList.remove('active');
}

// Soumission du formulaire
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('editDevisForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const devisId = document.getElementById('editDevisId').value;
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

            fetch(`/api/devis/${devisId}/update/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: cleanData
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        closeEditDevisModal();
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
