document.addEventListener('DOMContentLoaded', function () {

    const modal = document.getElementById('deleteDevisModal');
    const backdrop = document.getElementById('deleteDevisBackdrop');
    const form = document.getElementById('deleteDevisForm');
    const clientName = document.getElementById('deleteDevisClientName');

    if (!modal) return;

    window.openDeleteDevisModal = function (id, name) {
        clientName.textContent = name;
        form.action = '/devis/' + id + '/delete/';
        backdrop.classList.add('active');
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    window.closeDeleteDevis = function () {
        backdrop.classList.remove('active');
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    backdrop.addEventListener('click', closeDeleteDevis);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeDeleteDevis();
    });

});