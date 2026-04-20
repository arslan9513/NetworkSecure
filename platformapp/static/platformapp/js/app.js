document.addEventListener('DOMContentLoaded', () => {
  const html = document.documentElement;
  const toggle = document.getElementById('themeToggle');

  const setTheme = (theme) => {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  };

  setTheme(localStorage.getItem('theme') || 'dark');

  if (toggle) {
    toggle.addEventListener('click', () => {
      const theme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      setTheme(theme);
    });
  }

  const commonChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: getComputedStyle(document.body).getPropertyValue('--text') } } },
    scales: {
      x: { ticks: { color: getComputedStyle(document.body).getPropertyValue('--muted') }, grid: { color: 'rgba(148,163,184,0.2)' } },
      y: { ticks: { color: getComputedStyle(document.body).getPropertyValue('--muted') }, grid: { color: 'rgba(148,163,184,0.2)' } }
    }
  };

  const trafficCanvas = document.getElementById('trafficChart');
  if (trafficCanvas) {
    trafficCanvas.style.minHeight = '280px';
    const ctx = trafficCanvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 240);
    gradient.addColorStop(0, 'rgba(139,92,246,0.55)');
    gradient.addColorStop(1, 'rgba(6,182,212,0.05)');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        datasets: [{
          label: 'Trafik akymy',
          data: [12, 19, 9, 23, 15, 28],
          fill: true,
          backgroundColor: gradient,
          borderColor: '#8b5cf6',
          tension: 0.35,
          pointRadius: 4,
        }]
      },
      options: commonChartOptions
    });
  }

  const threatCanvas = document.getElementById('threatChart');
  if (threatCanvas) {
    threatCanvas.style.minHeight = '280px';
    let levels = [];
    try { levels = JSON.parse(threatCanvas.dataset.levels || '[]'); } catch (e) { levels = []; }

    new Chart(threatCanvas, {
      type: 'bar',
      data: {
        labels: levels.map(v => `Dereje ${v.severity}`),
        datasets: [{
          label: 'Howp sany',
          data: levels.map(v => v.total),
          borderRadius: 8,
          backgroundColor: ['#8b5cf6', '#06b6d4', '#f43f5e', '#f59e0b', '#22c55e']
        }]
      },
      options: commonChartOptions
    });
  }

  const liveAlerts = document.getElementById('liveAlerts');
  if (liveAlerts) {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/duydurys/`);
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const div = document.createElement('div');
      div.className = 'feed-item';
      div.textContent = `⚠ ${data.habar || 'Täze duýduryş'}`;
      liveAlerts.prepend(div);
    };
  }
});
