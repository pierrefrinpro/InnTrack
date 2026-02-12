document.addEventListener('DOMContentLoaded', function() {

    var deleteClientId = null;
    var deleteModal    = document.getElementById('deleteClientModal');
    var deleteBackdrop = document.getElementById('deleteClientBackdrop');
    var deleteNameEl   = document.getElementById('deleteClientName');
    var confirmBtn     = document.getElementById('confirmDeleteBtn');
    var cancelBtn      = document.getElementById('cancelDeleteBtn');
    var closeDeleteBtn = document.getElementById('closeDeleteModal');

    window.openDeleteClientModal = function(clientId, clientName) {
        deleteClientId = clientId;
        deleteNameEl.textContent = clientName;
        deleteModal.classList.add('active');
        deleteBackdrop.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    function closeDeleteModal() {
        deleteClientId = null;
        deleteModal.classList.remove('active');
        deleteBackdrop.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (closeDeleteBtn) closeDeleteBtn.addEventListener('click', closeDeleteModal);
    if (cancelBtn)      cancelBtn.addEventListener('click', closeDeleteModal);
    if (deleteBackdrop) deleteBackdrop.addEventListener('click', closeDeleteModal);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeDeleteModal();
    });

    if (confirmBtn) confirmBtn.addEventListener('click', function() {
        if (!deleteClientId) return;

        var csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');
        var csrfToken = '';
        if (csrfEl) {
            csrfToken = csrfEl.value;
        } else {
            var cookie = document.cookie.split(';')
                .map(function(c) { return c.trim(); })
                .find(function(c) { return c.startsWith('csrftoken='); });
            csrfToken = cookie ? cookie.split('=')[1] : '';
        }

        confirmBtn.disabled = true;
        confirmBtn.textContent = 'Suppression...';

        fetch('/api/client/' + deleteClientId + '/delete/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (data.success) {
                var row = document.querySelector('tr[data-client-id="' + deleteClientId + '"]');
                if (row) row.remove();

                // Fermer le panneau latéral
                if (typeof closePanel === 'function') closePanel();
                closeDeleteModal();

                // Mettre à jour le compteur
                var remaining = document.querySelectorAll('.client-row').length;
                var countEl = document.querySelector('.page-count');
                if (countEl) {
                    countEl.textContent = remaining + ' client' + (remaining > 1 ? 's' : '');
                }
            } else {
                alert(data.error || 'Erreur lors de la suppression');
            }

            confirmBtn.disabled = false;
            confirmBtn.textContent = 'Supprimer définitivement';
        })
        .catch(function(err) {
            console.error('Erreur:', err);
            alert('Erreur lors de la suppression');
            confirmBtn.disabled = false;
            confirmBtn.textContent = 'Supprimer définitivement';
        });
    });

});