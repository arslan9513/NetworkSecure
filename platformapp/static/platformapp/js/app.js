document.addEventListener('DOMContentLoaded', () => {
  const html = document.documentElement;
  const toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const theme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
    });
    html.setAttribute('data-theme', localStorage.getItem('theme') || 'light');
  }

  const trafficCanvas = document.getElementById('trafficChart');
  if (trafficCanvas) {
    new Chart(trafficCanvas, {
      type: 'line',
      data: { labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'], datasets: [{ label: 'Trafik', data: [12, 19, 9, 23, 15, 28], borderColor: '#3b82f6' }] }
    });
  }

  const threatCanvas = document.getElementById('threatChart');
  if (threatCanvas) {
    let levels = [];
    try { levels = JSON.parse(threatCanvas.dataset.levels || '[]'); } catch (e) { levels = []; }
    new Chart(threatCanvas, {
      type: 'bar',
      data: { labels: levels.map(v => `Dereje ${v.severity}`), datasets: [{ label: 'Howp sany', data: levels.map(v => v.total), backgroundColor: '#ef4444' }] }
    });
  }

  const liveAlerts = document.getElementById('liveAlerts');
  if (liveAlerts) {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/duydurys/`);
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const div = document.createElement('div');
      div.textContent = `⚠ ${data.habar || 'Täze duýduryş'}`;
      liveAlerts.prepend(div);
    };
  }
});
