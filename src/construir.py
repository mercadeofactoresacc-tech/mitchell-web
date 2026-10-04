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

    # Preguntas frecuentes
    if preguntas:
        bloque = "".join(
            f'<details{" open" if i == 0 else ""}><summary>{esc(q["pregunta"])}</summary>'
            f'<div class="a">{esc(q.get("respuesta",""))}</div></details>'
            for i, q in enumerate(preguntas))
        home = re.sub(r'(<div class="faq">).*?(</div>\s*</div>\s*</section>)',
                      lambda m: m.group(1) + bloque + m.group(2), home, count=1, flags=re.S)

    home = home.replace('href="/css/site.css"', f'href="{BASE}/css/site.css"')
    home = home.replace('src="/js/site.js"', f'src="{BASE}/js/site.js"')
    if NOINDEX and 'name="robots"' not in home:
        home = home.replace("</head>", '<meta name="robots" content="noindex, nofollow">\n</head>')
    open(os.path.join(SALIDA, "index.html"), "w", encoding="utf-8").write(home)

    # ── Archivos de apoyo ──
    shutil.copytree(os.path.join(RAIZ, "public/css"), os.path.join(SALIDA, "css"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(RAIZ, "public/js"),  os.path.join(SALIDA, "js"),  dirs_exist_ok=True)
    open(os.path.join(SALIDA, ".nojekyll"), "w").write("")
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
