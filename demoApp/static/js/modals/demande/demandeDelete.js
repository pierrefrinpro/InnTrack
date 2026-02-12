document.addEventListener('DOMContentLoaded', function () {

    const modal = document.getElementById('deleteDemandeModal');
    const backdrop = document.getElementById('deleteDemandeBackdrop');
    const form = document.getElementById('deleteDemandeForm');
    const clientName = document.getElementById('deleteDemandeClientName');

    if (!modal) return;

    window.openDeleteDemande = function (id, name) {
        clientName.textContent = name;
        form.action = '/demandes/' + id + '/delete/';
        backdrop.classList.add('active');
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    window.closeDeleteDemande = function () {
        backdrop.classList.remove('active');
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    backdrop.addEventListener('click', closeDeleteDemande);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeDeleteDemande();
    });

});