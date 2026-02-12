// core/static/js/modal.js

class ModalManager {
    constructor() {
        this.overlay = document.getElementById('modalOverlay');
        this.activeModal = null;
        this.init();
    }

    init() {
        // Ouvrir
        document.querySelectorAll('[data-modal-target]').forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.getAttribute('data-modal-target');
                this.open(document.querySelector(target));
            });
        });

        // Fermer
        document.querySelectorAll('[data-modal-close]').forEach(btn => {
            btn.addEventListener('click', () => this.close());
        });

        // Fermer via overlay
        this.overlay.addEventListener('click', () => this.close());

        // Échap
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.activeModal) this.close();
        });

        // Submit AJAX
        document.querySelectorAll('[data-modal-form]').forEach(form => {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        });
    }

    open(modal) {
        if (!modal) return;
        this.activeModal = modal;
        this.overlay.classList.add('active');
        modal.classList.add('active');

        // Focus premier input
        setTimeout(() => {
            const firstInput = modal.querySelector('input, select, textarea');
            if (firstInput) firstInput.focus();
        }, 300);

        // Re-render icônes Lucide dans la modale
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    close() {
        if (!this.activeModal) return;
        this.activeModal.classList.remove('active');
        this.overlay.classList.remove('active');

        // Reset du formulaire
        const form = this.activeModal.querySelector('form');
        if (form) {
            form.reset();
            form.querySelectorAll('.has-error').forEach(el => {
                el.classList.remove('has-error');
            });
            form.querySelectorAll('.form-error').forEach(el => {
                el.textContent = '';
            });
        }

        this.activeModal = null;
    }

    async handleSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const submitBtn = form.querySelector('[type="submit"]');
        const originalText = submitBtn.innerHTML;

        // Loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Envoi...';

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });

            const data = await response.json();

            if (data.success) {
                this.close();
                this.showToast(data.message, 'success');

                // Recharger la page pour voir le nouveau contenu
                setTimeout(() => location.reload(), 800);
            } else {
                // Afficher les erreurs sur les champs
                if (data.errors) {
                    this.displayErrors(form, data.errors);
                }
                this.showToast(data.message || 'Erreur de validation', 'error');
            }
        } catch (err) {
            console.error(err);
            this.showToast('Erreur de connexion au serveur', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    }

    displayErrors(form, errors) {
        // Reset erreurs précédentes
        form.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));
        form.querySelectorAll('.form-error').forEach(el => el.textContent = '');

        for (const [field, messages] of Object.entries(errors)) {
            const input = form.querySelector(`[name="${field}"]`);
            if (input) {
                const group = input.closest('.form-group');
                if (group) {
                    group.classList.add('has-error');
                    let errorEl = group.querySelector('.form-error');
                    if (!errorEl) {
                        errorEl = document.createElement('span');
                        errorEl.className = 'form-error';
                        group.appendChild(errorEl);
                    }
                    errorEl.textContent = messages[0];
                }
            }
        }
    }

    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i data-lucide="${type === 'success' ? 'check-circle' : 'alert-circle'}" 
               style="width:18px;height:18px;"></i>
            <span>${message}</span>
        `;
        document.body.appendChild(toast);

        if (typeof lucide !== 'undefined') lucide.createIcons();

        requestAnimationFrame(() => toast.classList.add('show'));

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    window.modalManager = new ModalManager();
});