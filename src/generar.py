#!/usr/bin/env python3
"""
Generador del sitio de Manufacturas Mitchell.
Produce HTML estático: la home más una página por línea de producto.
Las direcciones son idénticas a las del sitio actual para no perder posicionamiento.
"""
import json, re, os, shutil, html

RAIZ   = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(RAIZ, "dist")
WA     = "https://wa.me/573123794395"
BASE   = os.environ.get("BASE", "")   # "" en el dominio propio, "/mitchell-web" en la prueba

# ── Orden y agrupación del catálogo ────────────────────────────────────────
CATALOGO = [
    ("marquillas-para-ropa",                    "Marquillas",      "Marquilla tejida y bordada"),
    ("marquillas-3d",                           "Marquillas",      "Marquilla 3D"),
    ("marquillas-lavables-nylon",               "Marquillas",      "Marquilla lavable en nylon"),
    ("marquillas-termicas-termoadhesivas",      "Marquillas",      "Marquilla térmica"),
    ("marquillas-en-razo-y-falla",              "Marquillas",      "Marquilla en razo y falla"),
    ("clises-en-fotograbado",                   "Clisés",          "Clisés en fotograbado"),
    ("repujes-en-sintetico",                    "Clisés",          "Repujes en sintético"),
    ("accesorios-pvc",                          "Apliques en PVC", "Apliques y accesorios en PVC"),
    ("marquillas-y-capelladas-pvc-para-calzado","Calzado",         "Marquillas y capelladas para calzado"),
    ("suela-para-babuchas-zapatos-bebe",        "Calzado",         "Suelas para babuchas y zapato de bebé"),
    ("herrajes-personalizados",                 "Herrajes",        "Herrajes personalizados"),
    ("llaveros-publicitarios",                  "Publicitario",    "Llaveros publicitarios"),
    ("manillas-publicitarias",                  "Publicitario",    "Manillas publicitarias"),
    ("stickers",                                "Publicitario",    "Stickers"),
    ("stickers-insumos",                        "Publicitario",    "Marquillas para ropa interior"),
]

# ── Ficha técnica por línea. Lo marcado con * está por confirmar. ──────────
FICHAS = {
 "marquillas-para-ropa": [("Material","Damasco, satén, taffeta"),("Colores","Hasta 8"),
   ("Acabado de borde","Corte caliente, doblez, centerfold"),("Resistencia","Lavado industrial"),
   ("Mínimo","500 unidades*"),("Muestra física","3 días*"),("Producción","8 días*")],
 "marquillas-3d": [("Material","PVC flexible"),("Relieve","Plano a redondo"),
   ("Molde","Pago único, queda a tu nombre"),("Mínimo","500 unidades*"),("Producción","Por confirmar*")],
 "marquillas-lavables-nylon": [("Material","Nylon"),("Técnica","Transferencia térmica"),
   ("Tacto","Suave, no raspa"),("Usos","Ropa interior e infantil"),("Mínimo","500 unidades*")],
 "marquillas-termicas-termoadhesivas": [("Material","Transferencia termoadhesiva"),
   ("Aplicación","Plancha de calor"),("Ventaja","Sin costura"),("Mínimo","500 unidades*")],
 "marquillas-en-razo-y-falla": [("Material","Razo y falla"),("Usos","Calzado y marroquinería"),
   ("Mínimo","500 unidades*"),("Producción","Por confirmar*")],
 "clises-en-fotograbado": [("Material","Magnesio y bronce"),("Espesores","1,5 mm · 3 mm · 7 mm"),
   ("Usos","Repujar, estampar, marcar"),("Molde","Por confirmar*"),("Elaboración","Por confirmar*")],
 "repujes-en-sintetico": [("Material","Sintético"),("Técnica","Repujado con clisé propio"),
   ("Mínimo","500 unidades*"),("Producción","Por confirmar*")],
 "accesorios-pvc": [("Material","Plastisol, PVC rígido y flexible"),("Técnica","Microinyección"),
   ("Usos","Chaquetas, morrales, accesorios"),("Mínimo","500 unidades*")],
 "marquillas-y-capelladas-pvc-para-calzado": [("Material","Plastisol"),
   ("Piezas","Marquillas y capelladas"),("Usos","Calzado deportivo y casual"),("Mínimo","500 unidades*")],
 "suela-para-babuchas-zapatos-bebe": [("Material","PVC flexible"),("Colores","A definir"),
   ("Usos","Babuchas y zapato de bebé"),("Mínimo","500 unidades*")],
 "herrajes-personalizados": [("Material","Zamac"),("Acabados","Níquel, dorado, envejecido"),
   ("Piezas","Hebillas, remaches, placas"),("Personalización","Logo en relieve"),("Mínimo","500 unidades*")],
 "llaveros-publicitarios": [("Material","Plastisol y PVC"),("Usos","Feria, activación, obsequio"),
   ("Molde","Puede reusar el de tu marquilla"),("Mínimo","500 unidades*")],
 "manillas-publicitarias": [("Material","Plastisol"),("Usos","Eventos y campañas"),("Mínimo","500 unidades*")],
 "stickers-insumos": [("Material","Silicona y satén"),("Usos","Ropa interior y deportiva"),("Tacto","Suave, sin costura"),("Mínimo","500 unidades*")],
 "stickers": [("Técnica","Impresión al calor"),("Tamaños","Varios"),("Usos","Señalización y marca"),
   ("Mínimo","500 unidades*")],
}

NAV2 = [("", "Todo"), ("marquillas","Marquillas"), ("clises","Clisés"),
        ("pvc","Apliques en PVC"), ("herrajes","Herrajes"),
        ("publicitario","Publicitario"), ("calzado","Calzado")]

def wa(msg):
    from urllib.parse import quote
    return f"{WA}?text={quote(msg)}"

def esc(s):
    return html.escape(s or "", quote=True)

def anchos_de(i, anchos):
    return [] if isinstance(i, dict) else anchos.get(i, [480])

def img_tag(slug, anchos, alt, clase="", lazy=True, sizes="100vw"):
    lz0 = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    if isinstance(slug, dict):          # viene del panel: {"chico":..., "grande":...}
        g_, c_ = slug.get("grande"), slug.get("chico")
        ss = f'srcset="{c_} 480w, {g_} 1000w" sizes="{sizes}"' if g_ and c_ else ""
        return f'<img src="{g_ or c_}" {ss} alt="{esc(alt)}" class="{clase}" {lz0}>'
    if 1000 in anchos:
        src = f"{BASE}/img/{slug}-1000.webp"
        srcset = f'srcset="{BASE}/img/{slug}-480.webp 480w, {BASE}/img/{slug}-1000.webp 1000w" sizes="{sizes}"'
    else:
        src = f"{BASE}/img/{slug}-480.webp"
        srcset = ""
    lz = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    return f'<img src="{src}" {srcset} alt="{esc(alt)}" class="{clase}" {lz}>'

# ── Cabecera y pie, compartidos ───────────────────────────────────────────
def cabecera(activo=""):
    tabs = "".join(
        f'<a href="{BASE}/#catalogo" data-f="{f}" class="{"on" if f==activo else ""}">{t}</a>'
        for f, t in NAV2)
    return f"""<div class="topbar">
  <nav class="wrap nav1" aria-label="Principal">
    <a href="{BASE}/" class="logo"><i>Marquillas y clisés</i><b>Mitchell</b></a>
    <div class="mid">
      <a href="{BASE}/#catalogo">Qué fabricamos</a>
      <a href="{BASE}/#proceso">Cómo trabajamos</a>
      <a href="{BASE}/#razones">La fábrica</a>
      <a href="{BASE}/#preguntas">Preguntas</a>
    </div>
    <div class="end">
      <a class="tel" href="tel:+576013660319">(601) 366 0319</a>
      <a class="btn btn-white" href="{wa('Hola, quiero cotizar.')}" target="_blank" rel="noopener">Cotizar</a>
      <button class="burger" aria-label="Abrir menú"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    </div>
  </nav>
  <div class="nav2"><div class="inner">{tabs}</div></div>
</div>"""

def pie():
    links = "".join(f'<li><a href="{BASE}/{s}/">{n}</a></li>' for s, _, n in CATALOGO[:7])
    return f"""<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <a href="{BASE}/" class="logo" style="margin-bottom:1.2rem"><i>Marquillas y clisés</i><b>Mitchell</b></a>
        <p class="legal" style="max-width:21rem">Fábrica de marquillas, clisés, apliques en PVC y herrajes para la industria de la confección y el calzado. Bogotá, Colombia.</p>
      </div>
      <div><h4>Qué fabricamos</h4><ul>{links}</ul></div>
      <div><h4>La empresa</h4><ul>
        <li><a href="{BASE}/#razones">La fábrica</a></li>
        <li><a href="{BASE}/#proceso">Cómo trabajamos</a></li>
        <li><a href="{BASE}/#preguntas">Preguntas frecuentes</a></li>
        <li><a href="{wa('Hola, quiero cotizar.')}" target="_blank" rel="noopener">Cotizar</a></li>
      </ul></div>
      <div><h4>Contacto</h4><p class="legal">
        <b class="q">Razón social por confirmar</b><br><span class="q">NIT por confirmar</span><br><br>
        Diagonal 16A # 24D-55 Sur<br>Barrio Restrepo, Bogotá D.C.<br><br>
        <a href="{WA}" target="_blank" rel="noopener">WhatsApp 312 379 4395</a><br>
        <a href="tel:+576013660319">(601) 366 0319</a><br>
        <a href="mailto:info@manufacturasmitchell.com">info@manufacturasmitchell.com</a><br><br>
        Lunes a viernes, 7:00 a.m. – 5:00 p.m.</p></div>
    </div>
    <div class="fbot">
      <span>© 2026 Manufacturas Mitchell</span>
      <a href="{BASE}/legal/datos/">Política de Tratamiento de Datos (Ley 1581 de 2012)</a>
    </div>
  </div>
</footer>
<a class="float" href="{wa('Hola, quiero cotizar un aplique.')}" target="_blank" rel="noopener" aria-label="Cotizar por WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.3 4.8 4.9-1.3A10 10 0 1 0 12 2Zm5.6 14.2c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.5-2.6-1.1-4.3-3.7-4.4-3.9-.1-.2-1-1.4-1-2.6 0-1.2.6-1.8.9-2.1.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2 0 .4-.1.5l-.3.4-.3.3c-.1.1-.2.3-.1.5.1.2.6 1 1.3 1.6.9.8 1.6 1 1.8 1.1.2.1.4.1.5-.1l.7-.8c.2-.2.3-.2.5-.1l1.8.9c.2.1.4.2.4.3.1.1.1.5-.1 1Z"/></svg>
  <span>Cotizar</span>
</a>"""

NOINDEX = os.environ.get("NOINDEX", "1") == "1"
FUENTE  = os.environ.get("FUENTE", "local")   # "local" o "panel"
_PANEL  = None
if FUENTE == "panel":
    _PANEL = json.load(open(os.path.join(RAIZ, "contenido/del-panel.json"), encoding="utf-8"))
    CATALOGO = [tuple(x) for x in _PANEL["catalogo"]]
    FICHAS   = {s: [tuple(f) for f in _PANEL["productos"][s]["ficha"]] for s,_,_ in CATALOGO}

def documento(titulo, desc, cuerpo, canonical, extra_head=""):
    robots = '<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://manufacturasmitchell.com{canonical}">
<meta name="theme-color" content="#09090B">
{robots}
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{BASE}/css/site.css">
{extra_head}
</head>
<body class="interna">
{cuerpo}
<script src="{BASE}/js/site.js" defer></script>
</body>
</html>"""

# ── Página de producto ────────────────────────────────────────────────────
def pagina_producto(slug, grupo, nombre, datos):
    p = datos[slug]
    texto = p["texto"]
    imgs  = p.get("cdn") or p.get("imgs", []); anchos = p.get("anchos", {})
    ficha = FICHAS.get(slug, [])

    hero_img = ""
    if imgs:
        hero_img = f'<div class="p-hero-img">{img_tag(imgs[0], anchos_de(imgs[0], anchos), nombre, lazy=False, sizes="(max-width:900px) 92vw, 46vw")}</div>'

    galeria = ""
    if len(imgs) > 1:
        celdas = "".join(
            f'<figure>{img_tag(i, anchos_de(i, anchos), f"{nombre} fabricada por Mitchell", sizes="(max-width:620px) 46vw, 23vw")}</figure>'
            for i in imgs[1:13])
        galeria = f"""<section class="p-gal"><div class="wrap">
  <div class="head"><span class="mono">Producción real</span>
  <h2 style="margin-top:.8rem">Piezas que han salido de la planta</h2></div>
  <div class="gal">{celdas}</div></div></section>"""

    filas = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in ficha)
    tabla = f'<dl class="vspecs">{filas}</dl>' if filas else ""

    otras = "".join(
        f'<a class="rel" href="{BASE}/{s}/"><span>{n}</span>'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h13M13 6l6 6-6 6"/></svg></a>'
        for s, g, n in CATALOGO if g == grupo and s != slug)
    relacionadas = f"""<section class="p-rel"><div class="wrap">
  <span class="mono">También en {esc(grupo.lower())}</span>
  <div class="rels">{otras}</div></div></section>""" if otras else ""

    cuerpo = f"""<div class="sky" aria-hidden="true">
  <div class="neb"></div>
  <div class="neb2"></div>
  <canvas id="stars"></canvas>
</div>
{cabecera(grupo.lower().split()[0] if grupo else "")}
<section class="p-hero">
  <div class="wrap p-grid">
    <div>
      <nav class="miga" aria-label="Ruta"><a href="{BASE}/">Inicio</a> <span>›</span> <a href="{BASE}/#catalogo">{esc(grupo)}</a></nav>
      <h1>{esc(nombre)}</h1>
      <p class="lead">{esc(texto)}</p>
      <div class="p-cta">
        <a class="btn btn-wa btn-lg" href="{wa(f'Hola, quiero cotizar {nombre.upper()}.')}" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.3 4.8 4.9-1.3A10 10 0 1 0 12 2Zm5.6 14.2c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.5-2.6-1.1-4.3-3.7-4.4-3.9-.1-.2-1-1.4-1-2.6 0-1.2.6-1.8.9-2.1.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2 0 .4-.1.5l-.3.4-.3.3c-.1.1-.2.3-.1.5.1.2.6 1 1.3 1.6.9.8 1.6 1 1.8 1.1.2.1.4.1.5-.1l.7-.8c.2-.2.3-.2.5-.1l1.8.9c.2.1.4.2.4.3.1.1.1.5-.1 1Z"/></svg>
          Cotizar por WhatsApp</a>
        <a class="btn btn-line" href="{BASE}/#catalogo">Ver todo el catálogo</a>
      </div>
      {tabla}
      <p class="nota-q">Los datos marcados con * están por confirmar.</p>
    </div>
    {hero_img}
  </div>
</section>
{galeria}
{relacionadas}
<section class="cta">
  <div class="wrap">
    <h2>¿Necesitas {esc(nombre.lower())}?</h2>
    <p class="lead">Mándanos el arte y te cotizamos en 24 horas. Precio por unidad para tres cantidades.</p>
    <a class="btn btn-white btn-lg" href="{wa(f'Hola, quiero cotizar {nombre.upper()}. Mi marca es:')}" target="_blank" rel="noopener">Escribir a 312 379 4395</a>
    <p class="note">Lunes a viernes, 7:00 a.m. a 5:00 p.m. · También al (601) 366 0319</p>
  </div>
</section>
{pie()}"""

    desc = p["seo_desc"] or f"{nombre} fabricadas en Bogotá por Manufacturas Mitchell. {texto[:110]}"
    return documento(f"{nombre} | Mitchell · Fábrica en Bogotá", desc, cuerpo, f"/{slug}/")



# ── Páginas de contenido ──────────────────────────────────────────────────
def pagina_texto(slug, titulo, texto, datos, extra_html=""):
    p = datos.get(slug, {})
    imgs = p.get("imgs", []); anchos = p.get("anchos", {})
    gal = ""
    if imgs:
        celdas = "".join(f'<figure>{img_tag(i, anchos_de(i, anchos), titulo, sizes="(max-width:620px) 46vw, 23vw")}</figure>'
                         for i in imgs[:12])
        gal = f'<section class="p-gal"><div class="wrap"><div class="gal">{celdas}</div></div></section>'
    parrafos = "".join(f"<p>{esc(t.strip())}</p>" for t in re.split(r'(?<=\.)\s+(?=[A-ZÁÉÍÓÚÑ])', texto) if t.strip())
    cuerpo = f"""<div class="sky" aria-hidden="true"><div class="neb"></div><div class="neb2"></div><canvas id="stars"></canvas></div>
{cabecera()}
<section class="p-hero"><div class="wrap" style="max-width:52rem">
  <nav class="miga"><a href="{BASE}/">Inicio</a> <span>›</span> <span>{esc(titulo)}</span></nav>
  <h1>{esc(titulo)}</h1>
  <div class="prosa">{parrafos}</div>
  {extra_html}
</div></section>
{gal}
<section class="cta"><div class="wrap">
  <h2>¿Hablamos?</h2>
  <p class="lead">Mándanos el arte y te cotizamos en 24 horas.</p>
  <a class="btn btn-white btn-lg" href="{wa('Hola, quiero cotizar.')}" target="_blank" rel="noopener">Escribir a 312 379 4395</a>
  <p class="note">Lunes a viernes, 7:00 a.m. a 5:00 p.m. · También al (601) 366 0319</p>
</div></section>
{pie()}"""
    desc = p.get("seo_desc") or f"{titulo} · Manufacturas Mitchell, fábrica de marquillas y clisés en Bogotá."
    return documento(f"{titulo} | Mitchell · Fábrica en Bogotá", desc, cuerpo, f"/{slug}/")

def pagina_indice(datos):
    filas = ""
    grupo_actual = None
    for slug, grupo, nombre in CATALOGO:
        if grupo != grupo_actual:
            if grupo_actual: filas += "</div>"
            filas += f'<h2 class="g-tit">{esc(grupo)}</h2><div class="rels">'
            grupo_actual = grupo
        filas += (f'<a class="rel" href="{BASE}/{slug}/"><span>{esc(nombre)}</span>'
                  f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h13M13 6l6 6-6 6"/></svg></a>')
    filas += "</div>"
    cuerpo = f"""<div class="sky" aria-hidden="true"><div class="neb"></div><div class="neb2"></div><canvas id="stars"></canvas></div>
{cabecera()}
<section class="p-hero"><div class="wrap" style="max-width:56rem">
  <nav class="miga"><a href="{BASE}/">Inicio</a> <span>›</span> <span>Productos</span></nav>
  <h1>Todo lo que fabricamos</h1>
  <p class="lead">Quince líneas de producción, todas en nuestra planta del Restrepo en Bogotá. Toca cualquiera para ver su ficha técnica.</p>
  <div class="indice">{filas}</div>
</div></section>
{pie()}"""
    return documento("Productos | Mitchell · Fábrica en Bogotá",
                     "Catálogo completo: marquillas tejidas, impresas, 3D, clisés, apliques en PVC, herrajes y llaveros. Fabricados en Bogotá.",
                     cuerpo, "/productos/")

def redireccion(slug, destino, titulo):
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<title>{esc(titulo)}</title>
<link rel="canonical" href="https://manufacturasmitchell.com{destino}">
<meta http-equiv="refresh" content="0; url={BASE}{destino}">
<meta name="robots" content="noindex, follow">
</head><body><p>Esta página se movió. <a href="{BASE}{destino}">Continuar</a></p></body></html>"""

# ── Main ──────────────────────────────────────────────────────────────────
def main():
    datos = json.load(open(os.path.join(RAIZ, "contenido/paginas-final.json"), encoding="utf-8"))
    if os.path.isdir(SALIDA): shutil.rmtree(SALIDA)
    os.makedirs(SALIDA)
    shutil.copytree(os.path.join(RAIZ, "public/img"), os.path.join(SALIDA, "img"))

    n = 0
    for slug, grupo, nombre in CATALOGO:
        if slug not in datos:
            print("  falta contenido:", slug); continue
        d = os.path.join(SALIDA, slug); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            pagina_producto(slug, grupo, nombre, datos))
        n += 1
    print(f"paginas de producto generadas: {n}")
    return n

if __name__ == "__main__":
    main()
