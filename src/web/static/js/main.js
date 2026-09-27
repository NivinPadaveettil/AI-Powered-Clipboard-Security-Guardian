document.addEventListener('DOMContentLoaded', () => {

    let rawHistory = [];

    // Navigation Tab Switching
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            navButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            if (targetTab === 'dashboard-tab') loadDashboardStats();
            if (targetTab === 'history-tab') loadHistoryData();
            if (targetTab === 'settings-tab') loadSettingsData();
        });
    });

    // ----------------------------------------------------
    // Load Dashboard Stats
    // ----------------------------------------------------
    async function loadDashboardStats() {
        try {
            const res = await fetch('/api/stats');
            const data = await res.json();

            if (data.success) {
                document.getElementById('stat-total').textContent = data.total;
                document.getElementById('stat-critical').textContent = data.critical;
                document.getElementById('stat-high').textContent = data.high;
                document.getElementById('stat-medium').textContent = data.medium;
                document.getElementById('stat-safe').textContent = data.safe;
                document.getElementById('val-avg-confidence').textContent = data.avg_confidence + '%';
                document.getElementById('val-avg-risk').textContent = data.avg_risk_score + ' / 100';
            }

            // Also load settings for status indicators
            const setRes = await fetch('/api/settings');
            const setData = await setRes.json();
            if (setData.success) {
                const s = setData.settings;
                document.getElementById('val-monitoring').textContent = s.monitoring_enabled ? 'ACTIVE' : 'PAUSED';
                document.getElementById('val-autoclear').textContent = s.auto_clear_enabled ? `ENABLED (${s.clear_timeout}s)` : 'DISABLED';
                document.getElementById('val-notifications').textContent = s.notifications_enabled ? 'ENABLED' : 'DISABLED';

                document.getElementById('val-db-path').textContent = setData.database.path;
                const bytes = setData.database.size_bytes;
                const sizeStr = bytes >= 1024 * 1024 ? (bytes / (1024 * 1024)).toFixed(2) + ' MB' : (bytes / 1024).toFixed(2) + ' KB';
                document.getElementById('val-db-size').textContent = sizeStr;
            }
        } catch (err) {
            console.error('Error loading dashboard stats:', err);
        }
    }

    // ----------------------------------------------------
    // Live AI Security Scanner
    // ----------------------------------------------------
    const btnScan = document.getElementById('btn-run-scan');
    const scannerInput = document.getElementById('scanner-input');
    const scannerResult = document.getElementById('scanner-result');

    btnScan.addEventListener('click', async () => {
        const text = scannerInput.value.trim();
        if (!text) return alert('Please enter or paste text to scan.');

        btnScan.disabled = true;
        btnScan.textContent = 'Scanning...';

        try {
            const res = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            const data = await res.json();

            if (data.success) {
                document.getElementById('res-category').textContent = data.category.toUpperCase();
                document.getElementById('res-confidence').textContent = data.confidence + '%';

                const riskTag = document.getElementById('res-risk-level');
                riskTag.textContent = data.risk_level;
                riskTag.className = `res-value risk-tag ${data.risk_level}`;

                document.getElementById('res-risk-score').textContent = data.risk_score + ' / 100';
                document.getElementById('res-explanation').textContent = data.explanation;
                document.getElementById('res-action').textContent = data.action;

                scannerResult.classList.remove('hidden');
            } else {
                alert('Scan failed: ' + data.error);
            }
        } catch (err) {
            alert('Scan error: ' + err);
        } finally {
            btnScan.disabled = false;
            btnScan.innerHTML = '<span>⚡</span> Run AI Classification';
        }
    });

    // ----------------------------------------------------
    // History Table & Filtering
    // ----------------------------------------------------
    const historyBody = document.getElementById('history-table-body');
    const searchInput = document.getElementById('history-search');
    const categorySelect = document.getElementById('filter-category');
    const riskSelect = document.getElementById('filter-risk');

    async function loadHistoryData() {
        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            if (data.success) {
                rawHistory = data.history;
                renderHistoryTable();
            }
        } catch (err) {
            console.error('Error loading history:', err);
        }
    }

    function renderHistoryTable() {
        const query = searchInput.value.toLowerCase().trim();
        const selCat = categorySelect.value;
        const selRisk = riskSelect.value;

        historyBody.innerHTML = '';

        const filtered = rawHistory.filter(item => {
            if (selCat !== 'ALL' && item.category !== selCat) return false;
            if (selRisk !== 'ALL' && item.risk_level !== selRisk) return false;
            if (query) {
                const combined = `${item.id} ${item.timestamp} ${item.category} ${item.risk_level} ${item.action}`.toLowerCase();
                if (!combined.includes(query)) return false;
            }
            return true;
        });

        if (filtered.length === 0) {
            historyBody.innerHTML = '<tr><td colspan="8" style="text-align:center; color:#94a3b8;">No records found</td></tr>';
            return;
        }

        filtered.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${item.id}</td>
                <td>${item.timestamp}</td>
                <td><strong>${item.category.toUpperCase()}</strong></td>
                <td>${item.confidence}%</td>
                <td>${item.risk_score}</td>
                <td><span class="risk-tag ${item.risk_level}">${item.risk_level}</span></td>
                <td>${item.action}</td>
                <td><button class="btn btn-secondary btn-sm btn-view-details" data-id="${item.id}">View</button></td>
            `;
            historyBody.appendChild(tr);
        });

        // Add view detail modal event handlers
        document.querySelectorAll('.btn-view-details').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.getAttribute('data-id'));
                const rec = rawHistory.find(r => r.id === id);
                if (rec) openModal(rec);
            });
        });
    }

    searchInput.addEventListener('input', renderHistoryTable);
    categorySelect.addEventListener('change', renderHistoryTable);
    riskSelect.addEventListener('change', renderHistoryTable);

    document.getElementById('btn-refresh-history').addEventListener('click', loadHistoryData);

    document.getElementById('btn-clear-history').addEventListener('click', async () => {
        if (!confirm('Are you sure you want to clear all detection history?')) return;
        try {
            const res = await fetch('/api/clear-history', { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                loadHistoryData();
                loadDashboardStats();
            }
        } catch (err) {
            alert('Failed to clear history');
        }
    });

    // ----------------------------------------------------
    // Details Modal Logic
    // ----------------------------------------------------
    const detailsModal = document.getElementById('details-modal');
    const btnCloseModal = document.getElementById('btn-close-modal');

    function openModal(rec) {
        document.getElementById('m-id').textContent = '#' + rec.id;
        document.getElementById('m-timestamp').textContent = rec.timestamp;
        document.getElementById('m-category').textContent = rec.category.toUpperCase();
        document.getElementById('m-confidence').textContent = rec.confidence + '%';
        document.getElementById('m-risk-score').textContent = rec.risk_score + ' / 100';

        const tag = document.getElementById('m-risk-level');
        tag.textContent = rec.risk_level;
        tag.className = `risk-tag ${rec.risk_level}`;

        document.getElementById('m-action').textContent = rec.action;
        document.getElementById('m-explanation').textContent = rec.explanation;

        detailsModal.classList.remove('hidden');
    }

    btnCloseModal.addEventListener('click', () => detailsModal.classList.add('hidden'));

    // ----------------------------------------------------
    // Settings Logic
    // ----------------------------------------------------
    const settingsForm = document.getElementById('settings-form');
    const saveStatus = document.getElementById('save-status');

    async function loadSettingsData() {
        try {
            const res = await fetch('/api/settings');
            const data = await res.json();
            if (data.success) {
                const s = data.settings;
                document.getElementById('set-monitoring').checked = s.monitoring_enabled;
                document.getElementById('set-autostart').checked = s.start_monitoring_automatically;
                document.getElementById('set-notifications').checked = s.notifications_enabled;
                document.getElementById('set-autoclear').checked = s.auto_clear_enabled;
                document.getElementById('set-timeout').value = s.clear_timeout;
            }
        } catch (err) {
            console.error('Error loading settings:', err);
        }
    }

    settingsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const newSettings = {
            monitoring_enabled: document.getElementById('set-monitoring').checked,
            start_monitoring_automatically: document.getElementById('set-autostart').checked,
            notifications_enabled: document.getElementById('set-notifications').checked,
            auto_clear_enabled: document.getElementById('set-autoclear').checked,
            clear_timeout: parseInt(document.getElementById('set-timeout').value)
        };

        try {
            const res = await fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newSettings)
            });
            const data = await res.json();
            if (data.success) {
                saveStatus.classList.remove('hidden');
                setTimeout(() => saveStatus.classList.add('hidden'), 3000);
            }
        } catch (err) {
            alert('Failed to save settings: ' + err);
        }
    });

    // Initial Load & Auto-Refresh Timer
    loadDashboardStats();
    setInterval(loadDashboardStats, 5000);
});
