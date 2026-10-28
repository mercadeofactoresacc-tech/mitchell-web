#!/usr/bin/env python3
"""
Genera el sitio leyendo el contenido del panel (Sanity).
Lo que el cliente publica en el panel sale aquí.

Las imágenes se sirven desde el CDN de Sanity, que las entrega
ya convertidas a WebP y al tamaño que se le pida.

Uso:
    BASE="/mitchell-web" NOINDEX="1" python3 generar-desde-panel.py
    BASE=""              NOINDEX="0" python3 generar-desde-panel.py
"""
import json, os, re, sys, urllib.request, urllib.parse

PROJECT = "5202v4k4"
DATASET = "production"
RAIZ    = os.path.dirname(os.path.abspath(__file__))

def consultar(groq):
    url = (f"https://{PROJECT}.api.sanity.io/v2021-10-21/data/query/{DATASET}"
           f"?query={urllib.parse.quote(groq)}")
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())["result"]

def cdn(ref, ancho):
    """Convierte la referencia de Sanity en una URL del CDN, ya en WebP."""
    if not ref: return None
    m = re.match(r'image-([a-f0-9]+)-(\d+x\d+)-(\w+)$', ref)
    if not m: return None
    ident, dims, ext = m.groups()
    return (f"https://cdn.sanity.io/images/{PROJECT}/{DATASET}/"
            f"{ident}-{dims}.{ext}?w={ancho}&fm=webp&q=76&fit=max")

def traer():
    productos = consultar(
        '*[_type=="producto"]|order(orden asc){nombre,"slug":slug.current,grupo,orden,'
        'descripcion,minimo,entrega,ficha[]{campo,valor},"fotos":fotos[].asset._ref}')
    empresa   = consultar('*[_id=="empresa"][0]') or {}
    inicio    = consultar('*[_id=="inicio"][0]{titular,subtitulo,cifras[]{numero,texto},'
                          '"hero":imagenHero.asset._ref}') or {}
    preguntas = consultar('*[_type=="pregunta"]|order(orden asc){pregunta,respuesta}')
    return productos, empresa, inicio, preguntas

def main():
    productos, empresa, inicio, preguntas = traer()
    print(f"Del panel: {len(productos)} productos · {len(preguntas)} preguntas")
    # Si un producto nuevo no trae direccion web, se arma sola con el nombre.
    # Asi el cliente nunca tiene que ver ni entender ese campo tecnico.
    import unicodedata
    def direccion_desde(nombre):
        s = unicodedata.normalize("NFD", nombre or "")
        s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        return s[:60] or "producto"

    usadas = {p["slug"] for p in productos if p.get("slug")}
    for p in productos:
        if p.get("slug"):
            continue
        base = direccion_desde(p.get("nombre"))
        s, n = base, 2
        while s in usadas:               # dos productos con el mismo nombre
            s, n = f"{base}-{n}", n + 1
        p["slug"] = s
        usadas.add(s)
        print(f"  direccion web generada sola: {p['nombre']} -> /{s}/")

    datos = {}
    for p in productos:
        fotos = [f for f in (p.get("fotos") or []) if f]
        datos[p["slug"]] = {
            "slug": p["slug"],
            "nombre": p["nombre"],
            "seo_title": f'{p["nombre"]} - Mitchell',
            "seo_desc": (p.get("descripcion") or "")[:155],
            "texto": p.get("descripcion") or "",
            "grupo": p.get("grupo") or "",
            "orden": p.get("orden") or 99,
            "ficha": [(f["campo"], f["valor"]) for f in (p.get("ficha") or []) if f.get("campo")],
            "minimo": p.get("minimo") or "",
            "entrega": p.get("entrega") or "",
            "cdn": [{"chico": cdn(f, 480), "grande": cdn(f, 1000), "xl": cdn(f, 1500)} for f in fotos],
        }

    salida = {
        "productos": datos,
        "empresa": empresa,
        "inicio": {**inicio, "heroUrl": cdn(inicio.get("hero"), 1400) if inicio.get("hero") else None},
        "preguntas": preguntas,
        "catalogo": [(p["slug"], p.get("grupo") or "", p["nombre"]) for p in productos],
    }
    destino = os.path.join(RAIZ, "contenido/del-panel.json")
    json.dump(salida, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"  guardado en {os.path.relpath(destino, RAIZ)}")
    con_foto = sum(1 for d in datos.values() if d["cdn"])
    print(f"  productos con foto: {con_foto}/{len(datos)}")
    print(f"  empresa: {'sí' if empresa else 'NO'} · inicio: {'sí' if inicio.get('titular') else 'NO'}")
    return salida

if __name__ == "__main__":
    main()
