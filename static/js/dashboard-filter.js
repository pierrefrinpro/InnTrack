// static/js/dashboard-filter.js

document.addEventListener('DOMContentLoaded', () => {

    let activeClientId = null;

    // ===== Récupère les tableaux visites et devis =====
    // On cible les tbodies des cards AUTRES que clients
    const allCards = document.querySelectorAll('.dash-card');
    let visitesBody = null;
    let devisBody = null;
    let visitesHeader = null;
    let devisHeader = null;

    allCards.forEach(card => {
        const title = card.querySelector('.card-header h3');
        if (!title) return;
        const text = title.textContent.toLowerCase();
        if (text.includes('visite')) {
            visitesBody = card.querySelector('tbody');
            visitesHeader = title;
        }
        if (text.includes('devis') && !text.includes('calendrier') && !text.includes('avancement')) {
            devisBody = card.querySelector('tbody');
            devisHeader = title;
        }
    });

    // ===== Clic sur un client =====
    document.querySelectorAll('.client-row').forEach(row => {
        row.addEventListener('click', () => {
            const clientId = row.dataset.clientId;
            const clientName = row.dataset.clientName;

            // Toggle : re-clic = désactive
            if (activeClientId === clientId) {
                clearFilter();
                return;
            }

            activeClientId = clientId;

            // Highlight ligne active
            document.querySelectorAll('.client-row').forEach(r => r.classList.remove('active'));
            row.classList.add('active');

            // Filtre les lignes
            filterRows(visitesBody, clientId);
            filterRows(devisBody, clientId);

            // Met à jour les headers avec badge
            updateHeaderBadge(visitesHeader, clientName);
            updateHeaderBadge(devisHeader, clientName);
        });
    });

    // ===== Filtre les <tr> d'un tbody =====
    function filterRows(tbody, clientId) {
        if (!tbody) return;

        // Retire ancien message vide
        const oldMsg = tbody.querySelector('.empty-filter-msg');
        if (oldMsg) oldMsg.remove();

        const rows = tbody.querySelectorAll('tr:not(.empty-filter-msg)');
        let visible = 0;

        rows.forEach(tr => {
            const trClientId = tr.dataset.clientId;
            if (!trClientId) return; // header ou ligne vide

            if (trClientId === clientId) {
                tr.classList.remove('filtered-out');
                visible++;
            } else {
                tr.classList.add('filtered-out');
            }
        });

        // Si aucun résultat
        if (visible === 0) {
            const colCount = tbody.closest('table').querySelector('thead tr')?.children.length || 3;
            const emptyTr = document.createElement('tr');
            emptyTr.className = 'empty-filter-msg';
            emptyTr.innerHTML = `<td colspan="${colCount}">Aucun résultat pour ce client</td>`;
            tbody.appendChild(emptyTr);
        }
    }

    // ===== Badge filtre dans le header =====
    function updateHeaderBadge(headerEl, clientName) {
        if (!headerEl) return;

        // Retire l'ancien badge
        const oldBadge = headerEl.parentElement.querySelector('.filter-badge');
        if (oldBadge) oldBadge.remove();

        const badge = document.createElement('span');
        badge.className = 'filter-badge';
        badge.innerHTML = `🔍 ${clientName} <span style="margin-left:4px;">✕</span>`;
        badge.title = 'Cliquer pour retirer le filtre';
        badge.addEventListener('click', (e) => {
            e.stopPropagation();
            clearFilter();
        });

        headerEl.parentElement.appendChild(badge);
    }

    // ===== Clear tout =====
    function clearFilter() {
        activeClientId = null;

        // Retire highlight
        document.querySelectorAll('.client-row').forEach(r => r.classList.remove('active'));

        // Montre tout
        document.querySelectorAll('.filtered-out').forEach(r => r.classList.remove('filtered-out'));

        // Retire les messages vides
        document.querySelectorAll('.empty-filter-msg').forEach(r => r.remove());

        // Retire les badges
        document.querySelectorAll('.filter-badge').forEach(b => b.remove());
    }
});
