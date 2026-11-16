/* Level Up · ayudas compartidas para los motion graphics (HyperFrames).
   Cárgalo al final del <body>, ANTES del script de la composición. */
window.LU = (function () {
  const root = document.documentElement;

  // 1) Variables: defaults declarados → HyperFrames (render/Studio) → ?query (galería)
  function defaults() {
    try {
      return Object.fromEntries(JSON.parse(root.dataset.compositionVariables || '[]').map((v) => [v.id, v.default]));
    } catch (e) { return {}; }
  }
  let v = defaults();
  try {
    const hv = window.__hyperframes && window.__hyperframes.getVariables && window.__hyperframes.getVariables();
    if (hv) v = Object.assign(v, hv);
  } catch (e) {}
  try { new URLSearchParams(location.search).forEach((val, k) => { v[k] = val; }); } catch (e) {}

  // 2) Colores → variables CSS
  ['papel', 'papel2', 'tinta', 'tinta2', 'acento', 'acento2', 'blanco'].forEach((k) => {
    if (v[k]) root.style.setProperty('--' + k, v[k]);
  });
  if (v.fondo === 'transparente') root.classList.add('sin-fondo');
  // posición y tamaño: se aplican directo a .capa (HyperFrames reinicia los estilos de <html> al renderizar)
  const ox = +v.x || 0, oy = +v.y || 0, esc = +v.escala || 1;
  if (ox || oy || esc !== 1) document.querySelectorAll('.capa').forEach((c) => { c.style.translate = ox + 'px ' + oy + 'px'; c.style.scale = String(esc); });

  // 3) Rellena textos: <span data-lu="titulo"></span>
  document.querySelectorAll('[data-lu]').forEach((el) => {
    const k = el.getAttribute('data-lu');
    if (v[k] !== undefined) el.textContent = v[k];
  });

  // 4) Parte un elemento en palabras o letras (para animarlas una por una)
  function split(el, mode) {
    const txt = el.textContent;
    el.textContent = '';
    const parts = mode === 'letras' ? Array.from(txt) : txt.split(/(\s+)/);
    const out = [];
    parts.forEach((p) => {
      if (/^\s+$/.test(p) || p === ' ') { el.appendChild(document.createTextNode(p)); return; }
      const s = document.createElement('span');
      s.className = mode === 'letras' ? 'letra' : 'palabra';
      s.textContent = p;
      el.appendChild(s); out.push(s);
    });
    return out;
  }

  // 5) Aleatorio con semilla (render = vista previa)
  function rand(seed) {
    let s = (seed % 2147483647) || 1;
    return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  }

  // 6) Registra la línea de tiempo con el id de la composición
  function register(tl) {
    const id = document.querySelector('[data-composition-id]').getAttribute('data-composition-id');
    window.__timelines = window.__timelines || {};
    window.__timelines[id] = tl;
    return tl;
  }

  // 7) ZONA SEGURA (1080x1920) — reglas de Level Up:
  //    arriba 0–320 nada (solo título-gancho) · cara 320–920 libre · subtítulos 920–1070
  //    elementos 1080–1500 con x 96–870 (derecha libre por los botones de Instagram) · abajo de 1510 nada
  const ZONAS = {
    elementos: [120, 1080, 960, 1500],   // centrado (x 120–960): ni pegado a la izquierda ni debajo de los botones
    titulo: [120, 150, 960, 330],
    pantalla: [90, 330, 990, 1490],
    panel: [70, 330, 1010, 905],          // tutorial: mitad de arriba, sin tocar la franja de arriba ni los subtítulos
  };
  function ajustarZona() {
    const zona = v.zona || root.dataset.zona || 'libre';
    const capa = document.querySelector('.capa');
    if (!capa) return;
    let tx = 0, ty = 0, s = 1;
    const Z = ZONAS[zona];
    if (Z) {
      const id = document.querySelector('[data-composition-id]').getAttribute('data-composition-id');
      const tl = window.__timelines && window.__timelines[id];
      // mide el motion en su momento "lleno" (antes de salir)
      if (tl) tl.seek(Math.min(tl.duration() * 0.62, Math.max(0, tl.duration() - 0.6)), false);
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      capa.querySelectorAll('*').forEach((el) => {
        const tag = el.tagName.toLowerCase();
        if (el.closest('svg') && tag !== 'svg') return;
        const cs0 = getComputedStyle(el);
        const caja = cs0.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs0.backgroundImage !== 'none' || cs0.boxShadow !== 'none' || parseFloat(cs0.borderTopWidth) > 0;
        const hoja = tag === 'svg' || tag === 'img' || el.children.length === 0;
        if (!hoja && !caja) return;                                   // contenedor invisible: se miden sus hijos
        if (hoja && tag !== 'svg' && tag !== 'img' && !caja && !el.textContent.trim()) return;   // vacío sin dibujo
        let a = el, vis = true;
        while (a && a !== capa) { const cs = getComputedStyle(a); if (cs.display === 'none' || +cs.opacity < 0.05) { vis = false; break; } a = a.parentElement; }
        if (!vis) return;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2 || (r.width > 1000 && r.height > 1700)) return;
        const L = Math.max(0, r.left), T = Math.max(0, r.top), R = Math.min(1080, r.right), B = Math.min(1920, r.bottom);
        if (R - L < 2 || B - T < 2) return;                          // lo que está fuera del cuadro no cuenta
        x0 = Math.min(x0, L); y0 = Math.min(y0, T); x1 = Math.max(x1, R); y1 = Math.max(y1, B);
      });
      if (tl) tl.seek(0, false);
      if (x1 > x0 && y1 > y0) {
        const w = x1 - x0, h = y1 - y0, zw = Z[2] - Z[0], zh = Z[3] - Z[1];
        s = Math.min(1, zw / w, zh / h);
        tx = (Z[0] + Z[2]) / 2 - s * (x0 + x1) / 2;
        ty = (Z[1] + Z[3]) / 2 - s * (y0 + y1) / 2;
      }
    }
    capa.style.transformOrigin = '0 0';
    capa.style.translate = (tx + ox) + 'px ' + (ty + oy) + 'px';
    capa.style.scale = String(s * esc);
  }

  return { vars: v, split, rand, register, ajustarZona, ZONAS };
})();
