# Sitio de Manufacturas Mitchell

Sitio estático. El contenido se edita desde el panel y el sitio se reconstruye solo.

- **Sitio:** https://mercadeofactoresacc-tech.github.io/mitchell-web/
- **Panel de edición:** /admin/

## Cómo funciona

1. El cliente edita y publica en el panel (Sanity)
2. El panel avisa a este repositorio
3. El automatismo lee el contenido, arma las 22 páginas y las publica

## Construir a mano

```bash
cd src
BASE="/mitchell-web" NOINDEX="1" python3 construir.py   # prueba
BASE=""              NOINDEX="0" python3 construir.py   # producción
```
