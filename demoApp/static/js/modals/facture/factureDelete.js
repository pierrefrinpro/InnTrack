document.addEventListener('DOMContentLoaded', function () {

    const modal = document.getElementById('deleteFactureModal');
    const backdrop = document.getElementById('deleteFactureBackdrop');
    const form = document.getElementById('deleteFactureForm');
    const clientName = document.getElementById('deleteFactureClientName');

    if (!modal) return;

    window.openDeleteFacture = function (id, name) {
        clientName.textContent = name;
        form.action = '/factures/' + id + '/delete/';
        backdrop.classList.add('active');
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    window.closeDeleteFacture = function () {
        backdrop.classList.remove('active');
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    backdrop.addEventListener('click', closeDeleteFacture);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeDeleteFacture();
    });

});