document.addEventListener('DOMContentLoaded', function () {

    const panel     = document.getElementById('devisDetailPanel');
    const panelBody = document.getElementById('devisPanelBody');
    const panelTitle = document.getElementById('devisPanelTitle');
    let activeRow = null;

    // ─── Ouvrir le panel ───
    window.openDevisPanel = function (id, event) {
        if (event && event.target.closest('.table-actions')) return;

        if (activeRow) activeRow.classList.remove('active');
        activeRow = document.querySelector(`tr[data-id="${id}"]`);
        if (activeRow) activeRow.classList.add('active');

        panelBody.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:200px;"><div class="spinner"></div></div>';
        panel.classList.add('open');

        fetch(`/api/devis/${id}/`)
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    panelBody.innerHTML = `<p style="color:var(--text-muted);">${data.error}</p>`;
                    return;
                }
                renderDevisPanel(data);
            })
            .catch(() => {
                panelBody.innerHTML = '<p style="color:#ef4444;">Erreur de chargement</p>';
            });
    };

    window.closeDevisPanel = function () {
        panel.classList.remove('open');
        if (activeRow) { activeRow.classList.remove('active'); activeRow = null; }
    };

    function renderDevisPanel(d) {
        panelTitle.textContent = `Devis #${d.id}`;

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
            <div class="panel-section-title">Devis</div>
            <div class="panel-field">
                <span class="panel-field-label">Statut</span>
                <span class="panel-field-value">
                    <span class="status-badge status-${(d.status || '').toLowerCase()}">${d.status_display || d.status || '—'}</span>
                </span>
            </div>
            <div class="panel-field">
                <span class="panel-field-label">Date prév. envoi</span>
                <span class="panel-field-value">${d.excpectedSentDate_display || '—'}</span>
            </div>
            <div class="panel-field">
                <span class="panel-field-label">Envoyé</span>
                <span class="panel-field-value">
                    ${d.sent ? '<span class="badge badge-success">Oui</span>' : '<span class="badge badge-warning">Non</span>'}
                </span>
            </div>
            ${d.sent && d.realSentDate_display ? `<div class="panel-field"><span class="panel-field-label">Date réelle</span><span class="panel-field-value">${d.realSentDate_display}</span></div>` : ''}
            ${d.demande_name ? `<div class="panel-field"><span class="panel-field-label">Demande</span><span class="panel-field-value"><span class="link-badge">${d.demande_name}</span></span></div>` : ''}
        </div>

        ${d.comment ? `<div class="panel-section"><div class="panel-section-title">Commentaire</div><div class="panel-comment">${d.comment}</div></div>` : ''}

        <div class="panel-section" style="padding-top:16px;">
            <div style="display:flex;gap:8px;">
                <button class="btn btn-primary btn-sm" style="flex:1;" onclick="openEditDevisModal(${d.id})">
                    <i data-lucide="pencil" style="width:14px;height:14px;"></i> Modifier
                </button>
                <button class="btn btn-danger btn-sm" style="flex:1;" onclick="openDeleteDevisModal(${d.id}, '${d.client_name}')">
                    <i data-lucide="trash-2" style="width:14px;height:14px;"></i> Supprimer
                </button>
            </div>
        </div>`;

        panelBody.innerHTML = html;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDevisPanel(); });
    if (typeof lucide !== 'undefined') lucide.createIcons();
});
