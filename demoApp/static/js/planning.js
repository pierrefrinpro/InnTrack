/* static/js/planning.js */

document.addEventListener('DOMContentLoaded', function () {
    const EVENTS = window.PLANNING_EVENTS || [];
    const MONTHS_FR = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ];

    let currentDate = new Date();
    let selectedDate = null;

    // ===== DOM =====
    const calTitle = document.getElementById('calTitle');
    const calDays = document.getElementById('calDays');
    const calPrev = document.getElementById('calPrev');
    const calNext = document.getElementById('calNext');
    const calToday = document.getElementById('calToday');
    const dayEventsEl = document.getElementById('dayEvents');
    const selectedDayTitle = document.getElementById('selectedDayTitle');

    // Filtres
    const filterCbs = document.querySelectorAll('.filter-cb');
    const filterClient = document.getElementById('filterClient');
    const filterStatutDemande = document.getElementById('filterStatutDemande');
    const filterStatutDevis = document.getElementById('filterStatutDevis');
    const filterTypeDemande = document.getElementById('filterTypeDemande');
    const resetBtn = document.getElementById('resetFilters');

    // Vérification sécurité
    if (!calPrev || !calNext || !calDays) {
        console.warn('Planning: éléments DOM manquants');
        return;
    }

    // ===== FILTRAGE =====
    function getActiveFilters() {
        const types = [];
        filterCbs.forEach(cb => {
            if (cb.checked) types.push(cb.value);
        });

        return {
            types,
            clientId: filterClient ? filterClient.value : '',
            statutDemande: filterStatutDemande ? filterStatutDemande.value : '',
            statutDevis: filterStatutDevis ? filterStatutDevis.value : '',
            typeDemande: filterTypeDemande ? filterTypeDemande.value : '',
        };
    }

    function filterEvents(events) {
        const f = getActiveFilters();

        return events.filter(ev => {
            if (!f.types.includes(ev.type)) return false;
            if (f.clientId && String(ev.client_id) !== f.clientId) return false;
            if (ev.type === 'demande' && f.statutDemande && ev.status !== f.statutDemande) return false;
            if (ev.type === 'devis' && f.statutDevis && ev.status !== f.statutDevis) return false;
            if (ev.type === 'demande' && f.typeDemande && ev.type_demande !== f.typeDemande) return false;
            return true;
        });
    }

    // ===== CALENDRIER =====
    function renderCalendar() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        calTitle.textContent = `${MONTHS_FR[month]} ${year}`;

        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);

        let startDay = firstDay.getDay() - 1;
        if (startDay < 0) startDay = 6;

        const daysInMonth = lastDay.getDate();
        const prevMonthLast = new Date(year, month, 0).getDate();

        const filtered = filterEvents(EVENTS);

        const eventsByDate = {};
        filtered.forEach(ev => {
            if (!eventsByDate[ev.date]) eventsByDate[ev.date] = [];
            eventsByDate[ev.date].push(ev);
        });

        let html = '';
        const totalCells = Math.ceil((startDay + daysInMonth) / 7) * 7;

        const today = new Date();
        const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

        for (let i = 0; i < totalCells; i++) {
            let dayNum, dateStr, otherMonth = false;

            if (i < startDay) {
                dayNum = prevMonthLast - startDay + i + 1;
                const pm = month === 0 ? 12 : month;
                const py = month === 0 ? year - 1 : year;
                dateStr = `${py}-${String(pm).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;
                otherMonth = true;
            } else if (i >= startDay + daysInMonth) {
                dayNum = i - startDay - daysInMonth + 1;
                const nm = month + 2 > 12 ? 1 : month + 2;
                const ny = month + 2 > 12 ? year + 1 : year;
                dateStr = `${ny}-${String(nm).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;
                otherMonth = true;
            } else {
                dayNum = i - startDay + 1;
                dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;
            }

            const isToday = dateStr === todayStr;
            const isSelected = selectedDate === dateStr;
            const dayEvents = eventsByDate[dateStr] || [];

            let classes = 'cal-day';
            if (otherMonth) classes += ' cal-day--other-month';
            if (isToday) classes += ' cal-day--today';
            if (isSelected) classes += ' cal-day--selected';

            html += `<div class="${classes}" data-date="${dateStr}">`;
            html += `<div class="cal-day-number">${dayNum}</div>`;
            html += `<div class="cal-day-events">`;

            const maxShow = 5;
            dayEvents.slice(0, maxShow).forEach(ev => {
                html += `<div class="cal-event cal-event--${ev.type}" title="${ev.title}">${ev.title}</div>`;
            });

            if (dayEvents.length > maxShow) {
                html += `<div class="cal-event-more">+${dayEvents.length - maxShow} autres</div>`;
            }

            html += `</div></div>`;
        }

        calDays.innerHTML = html;

        calDays.querySelectorAll('.cal-day').forEach(dayEl => {
            dayEl.addEventListener('click', () => {
                selectedDate = dayEl.dataset.date;
                renderCalendar();
                renderDayEvents(dayEl.dataset.date);
            });
        });

        if (selectedDate) {
            renderDayEvents(selectedDate);
        }
    }

    // ===== EVENTS DU JOUR =====
    function renderDayEvents(dateStr) {
        const filtered = filterEvents(EVENTS).filter(ev => ev.date === dateStr);

        const parts = dateStr.split('-');
        const d = new Date(parts[0], parts[1] - 1, parts[2]);
        const options = { weekday: 'long', day: 'numeric', month: 'long' };
        selectedDayTitle.textContent = d.toLocaleDateString('fr-FR', options);

        if (filtered.length === 0) {
            dayEventsEl.innerHTML = '<p class="day-events-empty">Aucun événement ce jour</p>';
            return;
        }

        let html = '';
        filtered.forEach(ev => {
            html += `
                <div class="day-event-card day-event-card--${ev.type}">
                    <div class="day-event-type day-event-type--${ev.type}">
                        ${ev.type === 'demande' ? 'Demande' : ev.type === 'devis' ? 'Devis' : 'Travaux'}
                    </div>
                    <div class="day-event-title">${ev.client}</div>
                    <div class="day-event-sub">
                        ${ev.type === 'demande' ? ev.type_demande || '' : ''}
                        ${ev.type === 'devis' && ev.montant ? ev.montant + ' €' : ''}
                        ${ev.status ? ' • ' + ev.status : ''}
                    </div>
                </div>
            `;
        });

        dayEventsEl.innerHTML = html;
    }

    // ===== NAVIGATION =====
    calPrev.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    calNext.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    calToday.addEventListener('click', () => {
        currentDate = new Date();
        selectedDate = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`;
        renderCalendar();
        renderDayEvents(selectedDate);
    });

    // ===== FILTRES LISTENERS =====
    filterCbs.forEach(cb => cb.addEventListener('change', renderCalendar));
    if (filterClient) filterClient.addEventListener('change', renderCalendar);
    if (filterStatutDemande) filterStatutDemande.addEventListener('change', renderCalendar);
    if (filterStatutDevis) filterStatutDevis.addEventListener('change', renderCalendar);
    if (filterTypeDemande) filterTypeDemande.addEventListener('change', renderCalendar);

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            filterCbs.forEach(cb => { cb.checked = true; });
            if (filterClient) filterClient.value = '';
            if (filterStatutDemande) filterStatutDemande.value = '';
            if (filterStatutDevis) filterStatutDevis.value = '';
            if (filterTypeDemande) filterTypeDemande.value = '';
            renderCalendar();
        });
    }

    // ===== INIT =====
    renderCalendar();
    if (typeof lucide !== 'undefined') lucide.createIcons();
});
