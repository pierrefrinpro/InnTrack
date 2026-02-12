document.addEventListener('DOMContentLoaded', function () {

    const panel     = document.getElementById('factureDetailPanel');
    const panelBody = document.getElementById('facturePanelBody');
    const panelTitle = document.getElementById('facturePanelTitle');
    let activeRow = null;

    window.openFacturePanel = function (id, event) {
        if (event && event.target.closest('.table-actions')) return;

        if (activeRow) activeRow.classList.remove('active');
        activeRow = document.querySelector(`tr[data-id="${id}"]`);
        if (activeRow) activeRow.classList.add('active');

        panelBody.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:200px;"><div class="spinner"></div></div>';
        panel.classList.add('open');

        fetch(`/api/facture/${id}/`)
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    panelBody.innerHTML = `<p style="color:var(--text-muted);">${data.error}</p>`;
                    return;
                }
                renderFacturePanel(data);
            })
            .catch(() => {
                panelBody.innerHTML = '<p style="color:#ef4444;">Erreur de chargement</p>';
            });
    };

    window.closeFacturePanel = function () {
        panel.classList.remove('open');
        if (activeRow) { activeRow.classList.remove('active'); activeRow = null; }
    };

    function renderFacturePanel(d) {
        panelTitle.textContent = `Facture #${d.id}`;

        let html = `
        <div class="panel-section">
            <div class="panel-section-title">Client</div>
            <div class="panel-field">
                <span class="panel-field-label">Nom</span>
                <span class="panel-field-value">${d.client}</span>
            </div>
        </div>

        <div class="panel-section">
            <div class="panel-section-title">Facture</div>
            ${d.type ? `<div class="panel-field"><span class="panel-field-label">Type</span><span class="panel-field-value"><span class="type-badge">${d.type_display || d.type}</span></span></div>` : ''}
            <div class="panel-field">
                <span class="panel-field-label">Date facture</span>
                <span class="panel-field-value">${d.date || '—'}</span>
            </div>
        </div>`;

        panelBody.innerHTML = html;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeFacturePanel(); });
    if (typeof lucide !== 'undefined') lucide.createIcons();
});
