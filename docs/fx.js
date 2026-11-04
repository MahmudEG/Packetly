// Visual effects layer over the views app.js renders: the 3D network in the
// hero, card tilt and glare, headline and count-up motion, reveal-on-scroll,
// ripples and a reading-progress bar. Purely decorative; it re-applies itself
// whenever app.js re-renders #main and stands down under reduced motion.
// Hand-authored; build.py does not generate this file.
(() => {
  const main = document.getElementById('main');
  if (!main) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Theme colours, re-read whenever app.js toggles body.light.
  const pal = {};
  const readPalette = () => {
    const hex = getComputedStyle(document.body).getPropertyValue('--lime').trim() || '#c3ed7a';
    const n = parseInt(hex.slice(1), 16);
    pal.rgb = [n >> 16 & 255, n >> 8 & 255, n & 255].join(',');
    pal.hub = document.body.classList.contains('light') ? 'rgba(244,247,238,.94)' : 'rgba(26,34,22,.94)';
  };
  readPalette();
  new MutationObserver(readPalette).observe(document.body, { attributes: true, attributeFilter: ['class'] });
  const tint = a => 'rgba(' + pal.rgb + ',' + a.toFixed(3) + ')';

  const layer = cls => {
    const el = document.createElement('div');
    el.className = cls;
    el.setAttribute('aria-hidden', 'true');
    document.body.append(el);
    return el;
  };
  layer('fx-aurora');
  const progress = layer('fx-progress');
  const glow = fine && !reduce ? layer('fx-glow') : null;

  // ---- 3D network: points on a sphere, linked to their neighbours, with
  // packets hopping edge to edge and lighting the hub they arrive at. ------
  function mountNetwork(box) {
    if (box.querySelector('.fx-net')) return;
    const canvas = document.createElement('canvas');
    canvas.className = 'fx-net';
    canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', 'A rotating 3D map of a connected network, with packets moving between devices');
    box.prepend(canvas);
    box.classList.add('fx-3d');
    const ctx = canvas.getContext('2d');

    const N = 120, nodes = [], golden = Math.PI * (3 - Math.sqrt(5));
    for (let i = 0; i < N; i++) {
      const y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), a = golden * i, j = 1 + (Math.random() - 0.5) * 0.14;
      nodes.push([Math.cos(a) * r * j, y * j, Math.sin(a) * r * j]);
    }
    const edges = [], adj = nodes.map(() => []), seen = new Set();
    nodes.forEach((a, i) => {
      nodes.map((b, k) => [k, (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2])
        .filter(([k]) => k !== i).sort((p, q) => p[1] - q[1]).slice(0, 3)
        .forEach(([k]) => {
          const id = Math.min(i, k) + '-' + Math.max(i, k);
          if (seen.has(id)) return;
          seen.add(id);
          adj[i].push(edges.length);
          adj[k].push(edges.length);
          edges.push([i, k]);
        });
    });
    const hubs = ['>_', '≋', '▦', '☁', '⌘', '◇', '⊞', '△']
      .map((g, n) => ({ i: Math.floor((n + 0.5) * N / 8), g, pulse: 0 }));
    const hubAt = new Map(hubs.map(h => [h.i, h]));
    const hop = (p, from) => {
      const e = adj[from][Math.random() * adj[from].length | 0];
      p.e = e; p.fwd = edges[e][0] === from; p.t = 0; p.v = 0.45 + Math.random() * 0.6;
    };
    const packets = Array.from({ length: 18 }, () => {
      const p = { trail: [] };
      hop(p, Math.random() * N | 0);
      p.t = Math.random();
      return p;
    });
    const rings = [[1.34, 0.42, [2, 6]], [1.55, -0.62, [1, 9]]];
    const P = nodes.map(() => ({ x: 0, y: 0, d: 0 })), tmp = { x: 0, y: 0, d: 0 };

    let W = 0, H = 0;
    const size = () => {
      const dpr = Math.min(2, devicePixelRatio || 1);
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (reduce) draw(0);
    };

    let yaw = 0.7, vYaw = 0.16, px = 0, py = 0, tx = 0, ty = 0, drag = null, clock = 0;
    function draw(dt) {
      clock += dt;
      if (!drag) { yaw += vYaw * dt; vYaw += (0.16 - vYaw) * Math.min(1, dt * 0.8) }
      px += (tx - px) * Math.min(1, dt * 3);
      py += (ty - py) * Math.min(1, dt * 3);
      const Y = yaw + px, X = -0.38 + py, cY = Math.cos(Y), sY = Math.sin(Y), cX = Math.cos(X), sX = Math.sin(X);
      const R = Math.min(W, H) * 0.37, cx = W / 2, cy = H / 2 - 6, f = 2.8;
      const proj = (x, y, z, o) => {
        const x1 = x * cY - z * sY, z1 = x * sY + z * cY, y1 = y * cX - z1 * sX, z2 = y * sX + z1 * cX, s = f / (f + z2);
        o.x = cx + x1 * R * s; o.y = cy + y1 * R * s; o.d = (1 - z2) / 2;
        return o;
      };
      nodes.forEach((n, i) => proj(n[0], n[1], n[2], P[i]));
      ctx.clearRect(0, 0, W, H);

      ctx.lineWidth = 1;
      for (const [rad, tilt, dash] of rings) {
        ctx.setLineDash(dash);
        ctx.beginPath();
        for (let k = 0; k <= 80; k++) {
          const a = k / 80 * Math.PI * 2, z = Math.sin(a) * rad;
          proj(Math.cos(a) * rad, z * Math.sin(tilt), z * Math.cos(tilt), tmp);
          k ? ctx.lineTo(tmp.x, tmp.y) : ctx.moveTo(tmp.x, tmp.y);
        }
        ctx.strokeStyle = tint(0.22);
        ctx.stroke();
      }
      ctx.setLineDash([]);
      const sat = clock * 0.7, sz = Math.sin(sat) * rings[0][0];
      proj(Math.cos(sat) * rings[0][0], sz * Math.sin(rings[0][1]), sz * Math.cos(rings[0][1]), tmp);
      ctx.fillStyle = tint(0.5 + tmp.d * 0.5);
      ctx.beginPath(); ctx.arc(tmp.x, tmp.y, 2 + tmp.d * 1.6, 0, 7); ctx.fill();

      ctx.lineWidth = 0.8;
      for (const [a, b] of edges) {
        const A = P[a], B = P[b], d = (A.d + B.d) / 2;
        ctx.strokeStyle = tint(0.04 + d * d * 0.42);
        ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.stroke();
      }
      for (const n of P) {
        ctx.fillStyle = tint(0.16 + n.d * 0.8);
        ctx.beginPath(); ctx.arc(n.x, n.y, 0.7 + n.d * 1.9, 0, 7); ctx.fill();
      }

      for (const p of packets) {
        p.t += p.v * dt;
        if (p.t >= 1) {
          const end = edges[p.e][p.fwd ? 1 : 0];
          if (hubAt.has(end)) hubAt.get(end).pulse = 1;
          hop(p, end);
        }
        const [a, b] = edges[p.e], A = P[p.fwd ? a : b], B = P[p.fwd ? b : a];
        const x = A.x + (B.x - A.x) * p.t, y = A.y + (B.y - A.y) * p.t, d = A.d + (B.d - A.d) * p.t;
        p.trail.push(x, y);
        if (p.trail.length > 16) p.trail.splice(0, 2);
        ctx.strokeStyle = tint(0.32 * d);
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        for (let k = 0; k < p.trail.length; k += 2) k ? ctx.lineTo(p.trail[k], p.trail[k + 1]) : ctx.moveTo(p.trail[k], p.trail[k + 1]);
        ctx.stroke();
        ctx.shadowColor = tint(1);
        ctx.shadowBlur = 12;
        ctx.fillStyle = tint(0.55 + 0.45 * d);
        ctx.beginPath(); ctx.arc(x, y, 1.3 + 1.7 * d, 0, 7); ctx.fill();
        ctx.shadowBlur = 0;
      }

      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      for (const h of [...hubs].sort((u, v) => P[u.i].d - P[v.i].d)) {
        const p = P[h.i], k = 0.55 + p.d * 0.65, w = 26 * k;
        ctx.globalAlpha = 0.3 + p.d * 0.7;
        if (h.pulse > 0) {
          ctx.strokeStyle = tint(h.pulse * 0.7);
          ctx.lineWidth = 1.5;
          ctx.beginPath(); ctx.arc(p.x, p.y, w * (0.7 + (1 - h.pulse) * 1.3), 0, 7); ctx.stroke();
          h.pulse = Math.max(0, h.pulse - dt * 1.4);
        }
        ctx.fillStyle = pal.hub;
        ctx.strokeStyle = tint(0.85);
        ctx.lineWidth = 1;
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(p.x - w / 2, p.y - w / 2, w, w, 6 * k); else ctx.rect(p.x - w / 2, p.y - w / 2, w, w);
        ctx.fill(); ctx.stroke();
        ctx.fillStyle = tint(1);
        ctx.font = '600 ' + Math.round(13 * k) + 'px ui-monospace, Consolas, monospace';
        ctx.fillText(h.g, p.x, p.y + 0.5);
        ctx.globalAlpha = 1;
      }
    }

    box.addEventListener('pointermove', e => {
      const r = box.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width - 0.5) * 0.7;
      ty = ((e.clientY - r.top) / r.height - 0.5) * 0.5;
      if (drag) {
        yaw = drag.yaw + (e.clientX - drag.x) * 0.008;
        vYaw = (e.clientX - drag.lx) * 0.5;
        drag.lx = e.clientX;
      }
    });
    box.addEventListener('pointerleave', () => { tx = ty = 0 });
    canvas.addEventListener('pointerdown', e => {
      drag = { x: e.clientX, lx: e.clientX, yaw };
      canvas.setPointerCapture(e.pointerId);
      canvas.classList.add('grabbing');
    });
    const release = () => {
      if (!drag) return;
      drag = null;
      vYaw = Math.max(-2.5, Math.min(2.5, vYaw));
      canvas.classList.remove('grabbing');
    };
    canvas.addEventListener('pointerup', release);
    canvas.addEventListener('pointercancel', release);

    let raf = 0, last = 0, onScreen = true;
    const loop = ts => {
      if (!box.isConnected) return stop();
      draw(Math.min(0.05, (ts - last) / 1000));
      last = ts;
      raf = requestAnimationFrame(loop);
    };
    const start = () => { if (!raf && !reduce && onScreen && !document.hidden) { last = performance.now(); raf = requestAnimationFrame(loop) } };
    const stop = () => { cancelAnimationFrame(raf); raf = 0 };
    new ResizeObserver(size).observe(canvas);
    new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; onScreen ? start() : stop() }).observe(box);
    document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
    size();
    start();
  }

  // ---- headline: each word flips up in turn; the <em> moves as one -------
  function split(h) {
    if (!h || h.querySelector('.fx-w')) return;
    let i = 0;
    const walk = node => {
      for (const ch of [...node.childNodes]) {
        if (ch.nodeType === 3) {
          const frag = document.createDocumentFragment();
          for (const part of ch.textContent.split(/(\s+)/)) {
            if (!part) continue;
            if (/^\s+$/.test(part)) { frag.append(part); continue }
            const w = document.createElement('span');
            w.className = 'fx-w';
            w.style.setProperty('--i', i++);
            w.textContent = part;
            frag.append(w);
          }
          ch.replaceWith(frag);
        } else if (ch.nodeName === 'EM') {
          ch.classList.add('fx-w');
          ch.style.setProperty('--i', i++);
        } else if (ch.nodeType === 1 && ch.nodeName !== 'BR') walk(ch);
      }
    };
    walk(h);
  }

  function countUp(b) {
    if (b.dataset.fxc) return;
    b.dataset.fxc = '1';
    const m = b.textContent.match(/^(\d+)(.*)$/);
    if (!m || reduce) return;
    const to = +m[1], suffix = m[2], t0 = performance.now();
    const step = t => {
      const k = Math.min(1, (t - t0) / 1100);
      b.textContent = Math.round(to * (1 - (1 - k) ** 3)) + suffix;
      if (k < 1) requestAnimationFrame(step);
    };
    b.textContent = '0' + suffix;
    requestAnimationFrame(step);
  }

  // ---- reveal on scroll, staggered within each batch ---------------------
  const REVEAL = '.card, .step, .bottom-callout, .section-top, .filters, .searchbox, .quick, '
    + '#cheat tbody tr, .sources, .detail .note, .tabs, .actions, .related h2, .case-finding';
  const io = reduce ? null : new IntersectionObserver(entries => {
    let n = 0;
    for (const en of entries) {
      if (!en.isIntersecting) continue;
      const el = en.target;
      io.unobserve(el);
      el.style.setProperty('--d', Math.min(n++, 10) * 45 + 'ms');
      el.classList.remove('fx-pending');
      el.classList.add('fx-in');
    }
  }, { rootMargin: '0px 0px -6% 0px' });

  let queued = false;
  function enhance() {
    queued = false;
    const net = main.querySelector('.network');
    if (net) mountNetwork(net);
    split(main.querySelector('.hero h1, .detail h1'));
    main.querySelectorAll('.stats b').forEach(countUp);
    if (io) {
      for (const el of main.querySelectorAll(REVEAL)) {
        if (el.dataset.fxr) continue;
        el.dataset.fxr = '1';
        el.classList.add('fx-pending');
        io.observe(el);
      }
    }
    progress.hidden = !main.querySelector('.detail:not(.prose)');
    onScroll();
  }
  new MutationObserver(() => { if (!queued) { queued = true; requestAnimationFrame(enhance) } })
    .observe(main, { childList: true, subtree: true });

  function onScroll() {
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, scrollY / max) : 0) + ')';
  }
  addEventListener('scroll', onScroll, { passive: true });

  // ---- pointer: card tilt with glare, and a soft light under the cursor ---
  if (fine && !reduce) {
    let current = null, ev = null, frame = 0;
    const settle = c => {
      c.classList.remove('fx-tilt');
      c.style.transition = 'transform .7s cubic-bezier(.2,1.3,.35,1), border-color .2s, box-shadow .3s';
      c.style.transform = '';
    };
    const track = () => {
      frame = 0;
      glow.style.transform = 'translate3d(' + ev.clientX + 'px,' + ev.clientY + 'px,0)';
      glow.classList.add('on');
      const c = ev.target.closest ? ev.target.closest('.card, .bottom-callout') : null;
      if (current && current !== c) settle(current);
      current = c;
      if (!c) return;
      const r = c.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width, y = (ev.clientY - r.top) / r.height;
      const max = c.classList.contains('card') ? 9 : 3;
      c.classList.add('fx-tilt');
      c.style.transition = 'transform .12s ease-out, border-color .2s, box-shadow .3s';
      c.style.transform = 'perspective(900px) rotateX(' + ((0.5 - y) * max).toFixed(2) + 'deg) rotateY('
        + ((x - 0.5) * max).toFixed(2) + 'deg) translateY(-4px)';
      c.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
      c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    };
    document.addEventListener('pointermove', e => { ev = e; if (!frame) frame = requestAnimationFrame(track) }, { passive: true });
    document.addEventListener('pointerout', e => {
      if (e.relatedTarget) return;
      glow.classList.remove('on');
      if (current) { settle(current); current = null }
    });
  }

  // ---- press feedback: ripples on buttons, a pop on copy and bookmark -----
  if (!reduce) {
    document.addEventListener('pointerdown', e => {
      const b = e.target.closest('.primary, .secondary, .filter, .quick button, .bottom-callout a');
      if (!b) return;
      const r = b.getBoundingClientRect(), dot = document.createElement('span');
      dot.className = 'fx-ripple';
      dot.style.left = e.clientX - r.left + 'px';
      dot.style.top = e.clientY - r.top + 'px';
      b.append(dot);
      setTimeout(() => dot.remove(), 650);
    });
    document.addEventListener('click', e => {
      const b = e.target.closest('[data-copy], [data-save]');
      if (!b) return;
      b.classList.remove('fx-pop');
      void b.offsetWidth;
      b.classList.add('fx-pop');
    });
  }

  enhance();
})();
