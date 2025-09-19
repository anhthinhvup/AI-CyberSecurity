// Matrix effect for left and right canvas
function startMatrix(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width = 120;
  const h = canvas.height = window.innerHeight;
  const fontSize = 18;
  const columns = Math.floor(w / fontSize);
  const drops = Array(columns).fill(1);
  const chars = 'アカサタナハマヤラワガザダバパイキシチニヒミリヰギジヂビピウクスツヌフムユルグズヅブプエケセテネヘメレヱゲゼデベペオコソトノホモヨロヲゴゾドボポヴッンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.split('');

  function draw() {
    ctx.fillStyle = 'rgba(24,24,26,0.18)';
    ctx.fillRect(0, 0, w, h);
    ctx.font = fontSize + "px 'Share Tech Mono', monospace";
    for (let i = 0; i < drops.length; i++) {
      const text = chars[Math.floor(Math.random() * chars.length)];
      ctx.fillStyle = '#39ff14';
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      if (Math.random() > 0.975) drops[i] = 0;
      drops[i]++;
      if (drops[i] * fontSize > h) drops[i] = 0;
    }
  }
  setInterval(draw, 50);
}

window.addEventListener('DOMContentLoaded', () => {
  startMatrix('matrix-left');
  startMatrix('matrix-right');
}); 