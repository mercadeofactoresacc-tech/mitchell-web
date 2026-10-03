

// Índice para escalonar la entrada de las tarjetas
document.querySelectorAll('#grid .card').forEach(function(c,i){ c.style.setProperty('--i', i); });

// La cinta se duplica para que el bucle no tenga costura
(function(){
  var t = document.getElementById('track');
  if (!t) return;
  t.innerHTML += t.innerHTML;
})();

// Las cifras cuentan al entrar en pantalla. Una sola vez.
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nums = Array.prototype.slice.call(document.querySelectorAll('.stat b'));
  if (reduce || !('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if (!en.isIntersecting) return;
      io.unobserve(en.target);
      var el = en.target, full = el.textContent.trim();
      var m = full.match(/(\D*)(\d+)(.*)/);
      if (!m) return;
      var pre = m[1], target = parseInt(m[2], 10), post = m[3];
      var t0 = null, dur = 900;
      function tick(ts){
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var e = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + Math.round(target * e) + post;
        if (p < 1) requestAnimationFrame(tick);
      }
      el.textContent = pre + '0' + post;
      requestAnimationFrame(tick);
    });
  }, { threshold: .55 });
  nums.forEach(function(n){ io.observe(n); });
})();

(function(){
  var input = document.getElementById('q');
  var cards = Array.prototype.slice.call(document.querySelectorAll('#grid .card'));
  var count = document.getElementById('count');
  var empty = document.getElementById('empty');
  var tabs  = Array.prototype.slice.call(document.querySelectorAll('.nav2 a'));
  var term = '', cat = '';

  function norm(s){
    return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
  }
  function apply(){
    var t = norm(term), c = norm(cat), shown = 0;
    cards.forEach(function(card){
      var k = norm(card.dataset.k + ' ' + card.textContent);
      var ok = (!t || k.indexOf(t) !== -1) && (!c || k.indexOf(c) !== -1);
      card.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown + (shown === 1 ? ' línea' : ' líneas');
    empty.hidden = shown !== 0;
  }

  input.addEventListener('input', function(){ term = input.value; apply(); });

  document.querySelectorAll('.chip').forEach(function(chip){
    chip.addEventListener('click', function(){
      input.value = chip.dataset.s; term = chip.dataset.s; apply();
      document.getElementById('catalogo').scrollIntoView({behavior:'smooth', block:'start'});
    });
  });

  tabs.forEach(function(tab){
    tab.addEventListener('click', function(){
      tabs.forEach(function(t){ t.classList.remove('on'); });
      tab.classList.add('on');
      cat = tab.dataset.f || '';
      input.value = ''; term = '';
      apply();
    });
  });
})();

// ===== Visor de detalle: clic en la tarjeta abre la ficha, no WhatsApp =====
(function(){
  var dlg = document.getElementById('viewer');
  if (!dlg || !dlg.showModal) return;   // sin soporte, la tarjeta sigue yendo a WhatsApp
  var shot = document.getElementById('vshot');
  var img  = document.getElementById('vimg');
  var last = null;

  function open(card, e){
    e.preventDefault();
    last = card;
    var big = card.querySelector('.thumb img');
    img.src = big.currentSrc || big.src;
    img.alt = big.alt;
    document.getElementById('vtag').textContent   = card.querySelector('.tag').textContent;
    document.getElementById('vtitle').textContent = card.querySelector('h3').textContent;
    document.getElementById('vdesc').textContent  = card.querySelector('p').textContent;
    document.getElementById('vwa').href           = card.getAttribute('href');

    var dl = document.getElementById('vspecs');
    dl.innerHTML = '';
    (card.dataset.spec || '').split(';').filter(Boolean).forEach(function(row){
      var p = row.split('|');
      var d = document.createElement('div');
      d.innerHTML = '<dt></dt><dd></dd>';
      d.querySelector('dt').textContent = p[0];
      d.querySelector('dd').textContent = p[1] || '';
      dl.appendChild(d);
    });

    shot.classList.remove('on');
    img.style.transformOrigin = 'center';
    dlg.showModal();
  }

  document.querySelectorAll('#grid .card').forEach(function(card){
    card.addEventListener('click', function(e){
      if (e.metaKey || e.ctrlKey || e.button === 1) return;  // abrir en pestaña nueva sigue funcionando
      open(card, e);
    });
  });

  // Zoom macro: el origen sigue al cursor
  shot.addEventListener('click', function(){ shot.classList.toggle('on'); });
  shot.addEventListener('mousemove', function(e){
    if (!shot.classList.contains('on')) return;
    var r = shot.getBoundingClientRect();
    img.style.transformOrigin =
      ((e.clientX - r.left) / r.width * 100) + '% ' + ((e.clientY - r.top) / r.height * 100) + '%';
  });
  shot.addEventListener('touchmove', function(e){
    if (!shot.classList.contains('on') || !e.touches[0]) return;
    var r = shot.getBoundingClientRect(), t = e.touches[0];
    img.style.transformOrigin =
      ((t.clientX - r.left) / r.width * 100) + '% ' + ((t.clientY - r.top) / r.height * 100) + '%';
  }, {passive:true});

  document.getElementById('vclose').addEventListener('click', function(){ dlg.close(); });
  dlg.addEventListener('click', function(e){ if (e.target === dlg) dlg.close(); });
  dlg.addEventListener('close', function(){
    shot.classList.remove('on');
    if (last) last.focus();
  });
})();

// ===== Ventana al universo: deriva continua, parallax de cursor, vía láctea =====
(function(){
  var cv = document.getElementById('stars');
  if (!cv) return;
  var ctx = cv.getContext('2d', { alpha: true });
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W = 0, H = 0, stars = [], shots = [], sprites = [];
  var scrollY = 0, mx = 0, my = 0, tx = 0, ty = 0, raf = null, t = 0, nextShot = 9;

  // Tintes: casi todas frías, unas pocas cálidas. Un cielo real no es blanco.
  var TINTS = [
    [255,255,255], [214,228,255], [188,208,255],
    [164,192,255], [255,236,208], [255,206,190]
  ];

  // Cada estrella se dibuja de un sprite ya renderizado: mucho más barato que arc().
  function makeSprites(){
    sprites = TINTS.map(function(c){
      var S = 34, off = document.createElement('canvas');
      off.width = off.height = S;
      var o = off.getContext('2d');
      var g = o.createRadialGradient(S/2, S/2, 0, S/2, S/2, S/2);
      g.addColorStop(0,    'rgba('+c[0]+','+c[1]+','+c[2]+',1)');
      g.addColorStop(0.16, 'rgba('+c[0]+','+c[1]+','+c[2]+',.82)');
      g.addColorStop(0.36, 'rgba('+c[0]+','+c[1]+','+c[2]+',.20)');
      g.addColorStop(1,    'rgba('+c[0]+','+c[1]+','+c[2]+',0)');
      o.fillStyle = g; o.fillRect(0, 0, S, S);
      return off;
    });
  }

  // La banda de la galaxia: una diagonal donde la densidad se dispara.
  function inBand(x, y){
    var d = Math.abs((y - H * 0.34) - (x - W * 0.5) * 0.42);
    return Math.exp(-(d * d) / (2 * Math.pow(H * 0.20, 2)));
  }

  function build(){
    stars = [];
    var target = Math.min(Math.round(W * H * 0.00042), 900);
    var guard = 0;
    while (stars.length < target && guard < target * 14){
      guard++;
      var x = Math.random() * W, y = Math.random() * H;
      // Rechazo por densidad: la banda acepta casi siempre, el resto no.
      var band = inBand(x, y);
      if (Math.random() > 0.22 + band * 0.78) continue;
      var z = Math.pow(Math.random(), 1.9);            // muchas lejanas, pocas cercanas
      stars.push({
        x: x, y: y, z: z,
        size: 1.1 + z * 6.2,
        a: 0.20 + z * 0.62 + band * 0.12,
        sp: sprites[(Math.random() * sprites.length) | 0],
        vx: -(0.0045 + z * 0.030),                     // deriva: las cercanas corren más
        vy: -(0.0012 + z * 0.007),
        tw: 0.30 + Math.random() * 0.85,
        ph: Math.random() * 6.2832
      });
    }
  }

  function size(){
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    makeSprites(); build();
    if (reduce) draw(0);
  }

  function draw(dt){
    ctx.clearRect(0, 0, W, H);

    // Resplandor difuso de la banda
    var bg = ctx.createLinearGradient(0, H * 0.10, W, H * 0.58);
    bg.addColorStop(0,   'rgba(110,140,220,0)');
    bg.addColorStop(0.5, 'rgba(120,148,225,.055)');
    bg.addColorStop(1,   'rgba(110,140,220,0)');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);

    ctx.globalCompositeOperation = 'lighter';
    var px = tx, py = ty;

    for (var i = 0; i < stars.length; i++){
      var st = stars[i];
      if (!reduce){
        st.x += st.vx * dt;
        st.y += st.vy * dt;
        if (st.x < -40) { st.x = W + 40; st.y = Math.random() * H; }
        if (st.y < -40) { st.y = H + 40; st.x = Math.random() * W; }
      }
      // Parallax: cursor y scroll mueven cada capa a su propia velocidad
      var x = st.x + px * (0.10 + st.z * 0.95);
      var y = st.y + py * (0.10 + st.z * 0.95) - scrollY * (0.006 + st.z * 0.085);
      y = ((y % (H + 80)) + (H + 80)) % (H + 80) - 40;

      var a = reduce ? st.a : st.a * (0.62 + 0.38 * Math.sin(t * st.tw + st.ph));
      var s = st.size;
      ctx.globalAlpha = a < 0 ? 0 : (a > 1 ? 1 : a);
      ctx.drawImage(st.sp, x - s, y - s, s * 2, s * 2);
    }

    // Una fugaz de vez en cuando. Sutil, no de postal.
    if (!reduce){
      for (var j = shots.length - 1; j >= 0; j--){
        var sh = shots[j];
        sh.p += dt * 0.0016;
        if (sh.p >= 1){ shots.splice(j, 1); continue; }
        var fade = Math.sin(sh.p * Math.PI);
        var cx = sh.x + sh.dx * sh.p, cy = sh.y + sh.dy * sh.p;
        var g2 = ctx.createLinearGradient(cx, cy, cx - sh.dx * 0.10, cy - sh.dy * 0.10);
        g2.addColorStop(0, 'rgba(220,232,255,' + (0.68 * fade).toFixed(3) + ')');
        g2.addColorStop(1, 'rgba(220,232,255,0)');
        ctx.globalAlpha = 1; ctx.strokeStyle = g2; ctx.lineWidth = 1.5; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(cx, cy);
        ctx.lineTo(cx - sh.dx * 0.10, cy - sh.dy * 0.10); ctx.stroke();
      }
    }

    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'source-over';
  }

  var last = 0;
  function loop(ts){
    raf = requestAnimationFrame(loop);
    var dt = last ? Math.min(ts - last, 50) : 16;
    last = ts; t += dt * 0.0011;

    tx += (mx - tx) * 0.045;                 // el parallax persigue al cursor con inercia
    ty += (my - ty) * 0.045;

    nextShot -= dt / 1000;
    if (nextShot <= 0){
      nextShot = 14 + Math.random() * 20;
      var fromLeft = Math.random() < 0.5;
      shots.push({
        x: fromLeft ? -60 : W * (0.3 + Math.random() * 0.6),
        y: H * (0.02 + Math.random() * 0.34),
        dx: (fromLeft ? 1 : -1) * (W * (0.45 + Math.random() * 0.4)),
        dy: H * (0.18 + Math.random() * 0.22),
        p: 0
      });
    }
    draw(dt);
  }

  function start(){ if (!raf && !reduce) { last = 0; raf = requestAnimationFrame(loop); } }
  function stop(){ if (raf) { cancelAnimationFrame(raf); raf = null; } }

  // La ventana: el cielo responde a dónde estás mirando
  window.addEventListener('pointermove', function(e){
    if (e.pointerType === 'touch') return;
    mx = (e.clientX / window.innerWidth  - 0.5) * 46;
    my = (e.clientY / window.innerHeight - 0.5) * 30;
  }, { passive: true });
  window.addEventListener('deviceorientation', function(e){
    if (e.gamma == null) return;
    mx = Math.max(-1, Math.min(1, e.gamma / 34)) * 34;
    my = Math.max(-1, Math.min(1, ((e.beta || 45) - 45) / 34)) * 22;
  }, { passive: true });

  window.addEventListener('scroll', function(){ scrollY = window.scrollY || 0; }, { passive: true });
  window.addEventListener('resize', size, { passive: true });
  document.addEventListener('visibilitychange', function(){ document.hidden ? stop() : start(); });

  size(); start();
})();
