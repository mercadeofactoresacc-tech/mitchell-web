#!/usr/bin/env python3
"""
Construye el sitio completo leyendo el contenido del panel.
Es lo que corre el automatismo cada vez que el cliente publica un cambio.

    BASE="/mitchell-web" NOINDEX="1" python3 construir.py    # prueba
    BASE=""              NOINDEX="0" python3 construir.py    # producción
"""
import os, json, re, shutil, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("FUENTE", "panel")
BASE    = os.environ.get("BASE", "")
NOINDEX = os.environ.get("NOINDEX", "1") == "1"

# 1. Traer el contenido del panel
sys.path.insert(0, RAIZ)
import importlib.util
spec = importlib.util.spec_from_file_location("panel", os.path.join(RAIZ, "generar-desde-panel.py"))
panelmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(panelmod)
PANEL = panelmod.main()

# 2. Cargar el generador con ese contenido
G = open(os.path.join(RAIZ, "generar.py"), encoding="utf-8").read().split("if __name__")[0]
ns = {"__name__": "generador", "__file__": os.path.join(RAIZ, "generar.py")}
exec(compile(G, "generar.py", "exec"), ns)
for k in ("SALIDA","CATALOGO","FICHAS","wa","esc","img_tag","anchos_de","cabecera","pie",
          "documento","pagina_producto","pagina_texto","pagina_indice","redireccion"):
    globals()[k] = ns[k]

datos     = PANEL["productos"]
empresa   = PANEL["empresa"]
inicio    = PANEL["inicio"]
preguntas = PANEL["preguntas"]

def construir():
    if os.path.isdir(SALIDA): shutil.rmtree(SALIDA)
    os.makedirs(SALIDA)

    # ── Páginas de producto ──
    for slug, grupo, nombre in CATALOGO:
        d = os.path.join(SALIDA, slug); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            pagina_producto(slug, grupo, nombre, datos))

    # ── Páginas de contenido ──
    contacto_html = f"""<dl class="datos">
  <div><dt>WhatsApp</dt><dd><a href="{wa('Hola, quiero cotizar.')}" target="_blank" rel="noopener">{esc(empresa.get('whatsapp','')[2:] if empresa.get('whatsapp','').startswith('57') else empresa.get('whatsapp',''))}</a></dd></div>
  <div><dt>Teléfono</dt><dd>{esc(empresa.get('telefono',''))}</dd></div>
  <div><dt>Correo</dt><dd><a href="mailto:{esc(empresa.get('correo',''))}">{esc(empresa.get('correo',''))}</a></dd></div>
  <div><dt>Dirección</dt><dd>{esc(empresa.get('direccion','')).replace(chr(10),'<br>')}</dd></div>
  <div><dt>Horario</dt><dd>{esc(empresa.get('horario',''))}</dd></div>
</dl>"""
    textos = [
        ("quienes-somos", "Quiénes somos",
         f"Manufacturas Mitchell lleva {empresa.get('anios','')} años fabricando marquillas, clisés y apliques en su planta del barrio Restrepo, en Bogotá. Producimos para marcas de ropa y calzado de todo el país. Antes de arrancar cualquier lote, el cliente recibe una muestra física para aprobar.", ""),
        ("contacto", "Contacto",
         "Escríbenos por WhatsApp y te respondemos el mismo día. Si prefieres llamar, el fijo de la planta está abajo.", contacto_html),
        ("productos-terminados", "Productos terminados",
         "Algunas de las piezas que han salido de nuestra planta para marcas de ropa y calzado.", ""),
    ]
    for slug, tit, txt, extra in textos:
        d = os.path.join(SALIDA, slug); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            pagina_texto(slug, tit, txt, datos, extra))

    os.makedirs(os.path.join(SALIDA, "productos"), exist_ok=True)
    open(os.path.join(SALIDA, "productos/index.html"), "w", encoding="utf-8").write(
        pagina_indice(datos))

    for slug, dest, tit in [("nosotros", "/quienes-somos/", "Nosotros"),
                            ("servicios", "/productos/", "Servicios")]:
        d = os.path.join(SALIDA, slug); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            redireccion(slug, dest, tit))

    # ── Home, con el contenido del panel ──
    home = open(os.path.join(RAIZ, "home-plantilla.html"), encoding="utf-8").read()

    if inicio.get("titular"):
        home = re.sub(r'(<h1[^>]*>).*?(</h1>)', lambda m: m.group(1) + esc(inicio["titular"]) + m.group(2),
                      home, count=1, flags=re.S)
    if inicio.get("subtitulo"):
        home = re.sub(r'(<p class="lead">).*?(</p>)', lambda m: m.group(1) + esc(inicio["subtitulo"]) + m.group(2),
                      home, count=1, flags=re.S)
    if inicio.get("cifras"):
        bloque = "".join(f'<div class="stat"><b>{esc(c.get("numero",""))}</b>'
                         f'<span>{esc(c.get("texto",""))}</span></div>' for c in inicio["cifras"])
        home = re.sub(r'(<div class="stats">\s*<div class="wrap">).*?(</div>\s*</div>)',
                      lambda m: m.group(1) + bloque + m.group(2), home, count=1, flags=re.S)

    # Tarjetas del catálogo
    GF = {"Marquillas":"marquillas","Clisés":"clises","Apliques en PVC":"pvc",
          "Calzado":"calzado","Herrajes":"herrajes","Publicitario":"publicitario"}
    tarjetas = []
    for slug, grupo, nombre in CATALOGO:
        p = datos[slug]
        foto = p["cdn"][0] if p.get("cdn") else None
        thumb = img_tag(foto, [], nombre, sizes="(max-width:620px) 92vw, (max-width:980px) 46vw, 30vw") if foto else ""
        resumen = " ".join((p.get("texto") or "").split()[:22])
        k = f'{GF.get(grupo,"")} {nombre} {grupo} {p.get("texto","")[:80]}'.lower()
        spec = ";".join(f"{a}|{b}" for a, b in p.get("ficha", []))
        primero = p["ficha"][0][1] if p.get("ficha") else ""
        tarjetas.append(f"""      <a class="card" data-k="{esc(k)}" data-spec="{esc(spec)}"
         data-wa="{wa('Hola, quiero cotizar ' + nombre.upper() + '.')}" href="{BASE}/{slug}/">
        <div class="thumb"><span class="tag">{esc(grupo)}</span>{thumb}</div>
        <div class="card-body">
          <h3>{esc(nombre)}</h3>
          <p>{esc(resumen)}…</p>
          <p class="spec">{esc(primero)}{' · ' + esc(p.get('minimo','')) if p.get('minimo') else ''}</p>
          <span class="go">Ver ficha <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h13M13 6l6 6-6 6"/></svg></span>
        </div>
      </a>""")
    home = re.sub(r'<div class="grid" id="grid">.*?\n    </div>',
                  '<div class="grid" id="grid">\n\n' + "\n\n".join(tarjetas) + "\n\n    </div>",
                  home, flags=re.S)
    home = re.sub(r'<span class="count" id="count">[^<]*</span>',
                  f'<span class="count" id="count">{len(tarjetas)} líneas</span>', home)

    # ── Cinta "Salido de la planta" ──
    # Antes apuntaba a archivos de la maqueta que nunca existieron (/img/tejida-480.webp
    # y 7 mas), asi que las 8 fotos salian rotas. Ahora sale del panel, igual que el resto.
    CINTA = [
        ("marquillas-para-ropa",                     "Tejida · damasco y satén"),
        ("marquillas-3d",                            "3D · PVC flexible"),
        ("clises-en-fotograbado",                    "Clisé · magnesio y bronce"),
        ("herrajes-personalizados",                  "Herraje · zamac"),
        ("accesorios-pvc",                           "Aplique · plastisol"),
        ("llaveros-publicitarios",                   "Llavero · PVC"),
        ("marquillas-y-capelladas-pvc-para-calzado", "Capellada · plastisol"),
        ("repujes-en-sintetico",                     "Repuje · sintético"),
    ]
    figs = []
    for slug, pie_txt in CINTA:
        p = datos.get(slug) or {}
        fotos = p.get("cdn") or []
        if not fotos:
            continue                      # sin foto en el panel, no se pinta un hueco
        # la segunda foto, para que la cinta no repita la miniatura del catalogo
        ref = fotos[1] if len(fotos) > 1 else fotos[0]
        url = (ref.get("chico") or "").replace("w=480&", "w=640&h=480&fit=crop&")
        if "h=480" not in url:
            url = (ref.get("chico") or "") + "&h=480&fit=crop"
        figs.append(
            f'<figure><a href="{BASE}/{slug}/">'
            f'<img src="{esc(url)}" alt="{esc(p.get("nombre",""))}" width="640" height="480" '
            f'loading="lazy" decoding="async">'
            f'<figcaption>{esc(pie_txt)}</figcaption></a></figure>')
    if figs:
        home = re.sub(r'<div class="track" id="track">.*?</div>',
                      '<div class="track" id="track">\n' + "\n".join(figs) + '\n  </div>',
                      home, count=1, flags=re.S)

    # Preguntas frecuentes
    if preguntas:
        bloque = "".join(
            f'<details{" open" if i == 0 else ""}><summary>{esc(q["pregunta"])}</summary>'
            f'<div class="a">{esc(q.get("respuesta",""))}</div></details>'
            for i, q in enumerate(preguntas))
        # Reemplazar desde el primer <details> hasta el ultimo cierre
        ini = home.find('<div class="faq">')
        fin = home.rfind('</details>')
        if ini != -1 and fin != -1 and fin > ini:
            home = home[:ini + len('<div class="faq">')] + bloque + home[fin + len('</details>'):]

    # Logo, telefono y horario: lo que el cliente puso en el panel
    def _d(c, r):
        v = empresa.get(c)
        return (v.strip() if isinstance(v, str) else v) or r
    l1, l2 = _d("logoLinea1","Marquillas y clisés"), _d("logoLinea2","Mitchell")
    tel     = _d("telefono","(601) 366 0319")
    tel_url = "tel:+57" + "".join(c for c in tel if c.isdigit())
    horario = _d("horario","Lunes a viernes, 7:00 a.m. a 5:00 p.m.")
    logo = (f'<img src="{BASE}/marca/logo.png" '
            f'srcset="{BASE}/marca/logo.png 197w, {BASE}/marca/logo@2x.png 394w, {BASE}/marca/logo@3x.png 591w" '
            f'sizes="197px" width="197" height="44" alt="{esc(l1 + " " + l2)}">')
    home = home.replace("<i>Marquillas y clisés</i><b>Mitchell</b>", logo)
    home = home.replace("</head>",
        f'<link rel="icon" type="image/png" sizes="32x32" href="{BASE}/marca/favicon-32.png">\n'
        f'<link rel="icon" type="image/png" sizes="16x16" href="{BASE}/marca/favicon-16.png">\n'
        f'<link rel="apple-touch-icon" href="{BASE}/marca/apple-touch-icon.png">\n</head>', 1)
    # El fijo del encabezado se reemplaza por WhatsApp, que es por donde cotizan
    wa_num = "".join(c for c in (empresa.get("whatsapp") or "573123794395") if c.isdigit())
    wa_num = wa_num[2:] if wa_num.startswith("57") and len(wa_num) > 10 else wa_num
    wa_leg = f"{wa_num[:3]} {wa_num[3:6]} {wa_num[6:]}" if len(wa_num) == 10 else wa_num
    ICONO_WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15l-1.3 4.8 4.9-1.3A10 10 0 1 0 12 2Zm5.6 14.2c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.5-2.6-1.1-4.3-3.7-4.4-3.9-.1-.2-1-1.4-1-2.6 0-1.2.6-1.8.9-2.1.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2 0 .4-.1.5l-.3.4-.3.3c-.1.1-.2.3-.1.5.1.2.6 1 1.3 1.6.9.8 1.6 1 1.8 1.1.2.1.4.1.5-.1l.7-.8c.2-.2.3-.2.5-.1l1.8.9c.2.1.4.2.4.3.1.1.1.5-.1 1Z"/></svg>')
    home = home.replace('<a class="tel" href="tel:+576013660319">(601) 366 0319</a>',
        f'<a class="tel tel-wa" href="{wa("Hola, quiero cotizar.")}" target="_blank" rel="noopener">{ICONO_WA}<span>{esc(wa_leg)}</span></a>')

    # Redes sociales en el pie, tomadas del panel
    ICO = {
     "facebook":'<path d="M17 2h-3a5 5 0 0 0-5 5v3H6v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
     "instagram":'<rect x="2.6" y="2.6" width="18.8" height="18.8" rx="5.2" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="12" cy="12" r="4.1" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="17.4" cy="6.6" r="1.25"/>',
     "tiktok":'<path d="M16.6 2h-3.1v13.2a2.9 2.9 0 1 1-2.4-2.85V9.2a6 6 0 1 0 5.5 5.98V8.6a7 7 0 0 0 4 1.26V6.73a4 4 0 0 1-4-4.02z"/>',
    }
    enlaces = "".join(
      f'<a href="{esc(empresa.get(r) or "")}" target="_blank" rel="noopener me" aria-label="{n}" title="{n}">'
      f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{ICO[r]}</svg></a>'
      for r, n in (("facebook","Facebook"),("instagram","Instagram"),("tiktok","TikTok"))
      if empresa.get(r))
    if enlaces:
        legal_pie = 'para la industria de la confección y el calzado.</p>'
        home = home.replace(legal_pie, legal_pie + f'<div class="redes">{enlaces}</div>', 1)
    home = home.replace('<a href="tel:+576013660319">(601) 366 0319</a>',
                        f'<a href="{tel_url}">{esc(tel)}</a>')
    home = home.replace("Lunes a viernes, 7:00 a.m. a 5:00 p.m. · También al (601) 366 0319",
                        f"{esc(horario)} · También al {esc(tel)}")

    home = home.replace('href="/css/site.css"', f'href="{BASE}/css/site.css"')
    home = home.replace('src="/js/site.js"', f'src="{BASE}/js/site.js"')
    import re as _re
    home = _re.sub(r'<meta name="robots"[^>]*>\s*', '', home)      # limpiar el que venga
    if NOINDEX:
        home = home.replace("</head>", '<meta name="robots" content="noindex, nofollow">\n</head>')
    open(os.path.join(SALIDA, "index.html"), "w", encoding="utf-8").write(home)

    # ── Archivos de apoyo ──
    shutil.copytree(os.path.join(RAIZ, "public/css"), os.path.join(SALIDA, "css"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(RAIZ, "public/js"),  os.path.join(SALIDA, "js"),  dirs_exist_ok=True)
    shutil.copytree(os.path.join(RAIZ, "public/marca"), os.path.join(SALIDA, "marca"), dirs_exist_ok=True)
    shutil.copy(os.path.join(RAIZ, "public/404.html"), os.path.join(SALIDA, "404.html"))
    open(os.path.join(SALIDA, ".nojekyll"), "w").write("")
    if not BASE:                      # solo en produccion, con dominio propio
        open(os.path.join(SALIDA, "CNAME"), "w").write("manufacturasmitchell.com\n")
    open(os.path.join(SALIDA, "robots.txt"), "w").write(
        "User-agent: *\nDisallow: /\n" if NOINDEX else
        "User-agent: *\nAllow: /\nSitemap: https://manufacturasmitchell.com/sitemap.xml\n")

    urls = ["/"] + [f"/{s}/" for s, _, _ in CATALOGO] + \
           ["/productos/", "/quienes-somos/", "/contacto/", "/productos-terminados/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>https://manufacturasmitchell.com{u}</loc></url>\n"
    open(os.path.join(SALIDA, "sitemap.xml"), "w").write(sm + "</urlset>\n")

    paginas = sum(1 for r, _, fs in os.walk(SALIDA) for f in fs if f == "index.html")
    peso = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(SALIDA) for f in fs)
    print(f"\nSitio construido: {paginas} páginas · {peso/1024:.0f} KB")
    print(f"  base: '{BASE or '(dominio propio)'}' · buscadores: {'bloqueados' if NOINDEX else 'permitidos'}")

if __name__ == "__main__":
    construir()
