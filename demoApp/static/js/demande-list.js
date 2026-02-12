document.addEventListener('DOMContentLoaded', function () {

    const panel     = document.getElementById('demandeDetailPanel');
    const panelBody = document.getElementById('demandePanelBody');
    const panelTitle = document.getElementById('demandePanelTitle');
    let activeRow = null;

    window.openDemandePanel = function (id, event) {
        if (event && event.target.closest('.table-actions')) return;

        if (activeRow) activeRow.classList.remove('active');
        activeRow = document.querySelector(`tr[data-id="${id}"]`);
        if (activeRow) activeRow.classList.add('active');

        panelBody.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:200px;"><div class="spinner"></div></div>';
        panel.classList.add('open');

        fetch(`/api/demande/${id}/`)
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    panelBody.innerHTML = `<p style="color:var(--text-muted);">${data.error}</p>`;
                    return;
                }
                renderDemandePanel(data);
            })
            .catch(() => {
                panelBody.innerHTML = '<p style="color:#ef4444;">Erreur de chargement</p>';
            });
    };

    window.closeDemandePanel = function () {
        panel.classList.remove('open');
        if (activeRow) { activeRow.classList.remove('active'); activeRow = null; }
    };

    function renderDemandePanel(d) {
        panelTitle.textContent = `Demande #${d.id}`;

        let html = `
        <div class="panel-section">
            <div class="panel-section-title">Client</div>
            <div class="panel-field">
                <span class="panel-field-label">Nom</span>
                <span class="panel-field-value">${d.client_name || '—'}</span>
            </div>
            ${d.client_phone ? `<div class="panel-field"><span class="panel-field-label">Tél</span><span class="panel-field-value"><a href="tel:${d.client_phone}" style="color:var(--accent);">${d.client_phone}</a></span></div>` : ''}
            ${d.client_email ? `<div class="panel-field"><span class="panel-field-label">Email</span><span class="panel-field-value"><a href="mailto:${d.client_email}" style="color:var(--accent);">${d.client_email}</a></span></div>` : ''}
        </div>

        <div class="panel-section">
            <div class="panel-section-title">Demande</div>
            ${d.type_display || d.type ? `<div class="panel-field"><span class="panel-field-label">Type</span><span class="panel-field-value"><span class="type-badge">${d.type_display || d.type}</span></span></div>` : ''}
            <div class="panel-field">
                <span class="panel-field-label">Motif</span>
                <span class="panel-field-value">${d.motif || '—'}</span>
            </div>
            <div class="panel-field">
                <span class="panel-field-label">Date demande</span>
                <span class="panel-field-value">${d.demandeDate || '—'}</span>
            </div>
            <div class="panel-field">
                <span class="panel-field-label">Visite prévue</span>
                <span class="panel-field-value">${d.excpectedVisitDate || '—'}</span>
            </div>
            <div class="panel-field">
                <span class="panel-field-label">Visite réelle</span>
                <span class="panel-field-value">
                    ${d.realVisitDate ? '<span class="badge badge-success">' + d.realVisitDate + '</span>' : '<span class="badge badge-warning">Non effectuée</span>'}
                </span>
            </div>
            ${d.clientAvailibity ? `<div class="panel-field"><span class="panel-field-label">Disponibilité</span><span class="panel-field-value">${d.clientAvailibity}</span></div>` : ''}
        </div>`;

        // Devis liés
        if (d.devis && d.devis.length > 0) {
            html += `<div class="panel-section"><div class="panel-section-title">Devis liés (${d.devis.length})</div>`;
            d.devis.forEach(dv => {
                html += `
                <div class="panel-linked-item">
                    <div class="panel-linked-item-info">
                        <span class="panel-linked-item-title">Devis #${dv.id}</span>
                        <span class="panel-linked-item-sub">${dv.excpectedSentDate || 'Pas de date'} — ${dv.sent ? '✅ Envoyé' : '⏳ Non envoyé'}</span>
                    </div>
                    <span class="status-badge status-${(dv.status || '').toLowerCase()}">${dv.status}</span>
                </div>`;
            });
            html += `</div>`;
        }

        // Actions
        html += `
        <div class="panel-section" style="padding-top:16px;">
            <div style="display:flex;gap:8px;">
                <button class="btn btn-primary btn-sm" style="flex:1;" onclick="openEditDemandeModal(${d.id})">
                    <i data-lucide="pencil" style="width:14px;height:14px;"></i> Modifier
                </button>
                <button class="btn btn-danger btn-sm" style="flex:1;" onclick="openDeleteDemandeModal(${d.id}, '${d.client_name}')">
                    <i data-lucide="trash-2" style="width:14px;height:14px;"></i> Supprimer
                </button>
            </div>
        </div>`;

        panelBody.innerHTML = html;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDemandePanel(); });
    if (typeof lucide !== 'undefined') lucide.createIcons();
});
