document.addEventListener('DOMContentLoaded', function () {

    const modal = document.getElementById('deleteTravauxModal');
    const backdrop = document.getElementById('deleteTravauxBackdrop');
    const form = document.getElementById('deleteTravauxForm');
    const clientName = document.getElementById('deleteTravauxClientName');

    if (!modal) return;

    window.openDeleteTravauxModal = function (id, name) {
        clientName.textContent = name;
        form.action = '/travaux/' + id + '/delete/';
        backdrop.classList.add('active');
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    window.closeDeleteTravaux = function () {
        backdrop.classList.remove('active');
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    backdrop.addEventListener('click', closeDeleteTravaux);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeDeleteTravaux();
    });

});