/* WEBSTER Dashboard - Spidey Web Interface */
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadStats();
    startPolling();
});

function initNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            const page = item.dataset.page;
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            const target = document.getElementById(`page-${page}`);
            if (target) target.classList.add('active');
            document.getElementById('page-title').textContent = item.querySelector('span:last-child').textContent;
        });
    });
}

async function loadStats() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        document.getElementById('stat-messages').textContent = data.conversations || '0';
        document.getElementById('stat-memory').textContent = data.memory_items || '0';
        document.getElementById('stat-study').textContent = data.study_items || '0';
        document.getElementById('stat-automation').textContent = data.automations || '0';
        const prov = document.getElementById('provider-status');
        if (prov) prov.textContent = data.provider || 'Spidey';
    } catch (e) {
        console.log('Dashboard: Waiting for connection...');
    }
}

function startPolling() {
    setInterval(loadStats, 5000);
}

async function sendCmd(cmd) {
    try {
        const res = await fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: cmd })
        });
        const data = await res.json();
        console.log('Command sent:', data);
    } catch (e) {
        console.error('Command failed:', e);
    }
}

function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
}
