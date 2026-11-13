# Sitio de Manufacturas Mitchell — instrucciones para Claude Code

Lee esto completo antes de tocar cualquier archivo. Cada regla de aquí salió de un
error que ya se cometió una vez.

---

## ⚠️ ANTES QUE NADA: quién te está escribiendo

**El dueño de la fábrica. No es programador.** No sabe qué es un commit, ni una rama,
ni un archivo HTML, y no tiene por qué saberlo. Va a escribirte cosas como
*"cámbiame la foto de la portada"* o *"quiero que diga otra cosa aquí"*.

Cómo trabajar con él:

1. **Hazlo tú.** No le pidas que abra una terminal, que corra un comando ni que edite
   un archivo. Si hace falta un comando, lo corres tú y le cuentas el resultado.
2. **Responde en español, sin tecnicismos.** Nada de "actualicé el template" — di
   "cambié el texto de la portada".
3. **Pregunta antes de publicar algo que se vea raro.** Publicar tarda 45 segundos y
   lo ve todo el mundo. Si no estás seguro de lo que pidió, pregúntale primero.
4. **Después de publicar, compruébalo en vivo** y dile que ya quedó. No le digas
   "listo" solo porque el código cambió — eso ya falló antes (regla 6).
5. **Si pide algo que rompe una regla de abajo, díselo y propón la alternativa.**
   No lo hagas callado, y tampoco te niegues sin dar salida.

### Lo que él va a pedir, y dónde se hace

| Lo que te pide | Dónde se resuelve |
|---|---|
| Cambiar un texto de un producto, una foto, un precio, una pregunta frecuente | **En el panel**, no en el código. Guíalo: `manufacturasmitchell.com/admin`. Si prefiere que lo hagas tú, se puede por código del panel, pero el camino normal es el panel |
| Agregar un producto nuevo | En el panel. Botón **Crear**. La dirección web se genera sola |
| Cambiar el logo, el teléfono, el WhatsApp, las redes | En el panel, sección **Empresa** |
| Cambiar los textos de "Cómo trabajamos" o "Nosotros" | **En el código** — hoy están ahí (ver pendientes al final) |
| Cambiar colores, tipografía, cómo se ve algo, mover secciones | **En el código**: `src/public/` y `src/home-plantilla.html` |
| "No se ve el cambio" | Casi siempre es el navegador. `Ctrl+Shift+R`. Ver la tabla del final |

---
## Qué es este proyecto

El sitio `https://manufacturasmitchell.com`. No es WordPress ni un constructor visual:
son **22 páginas HTML que se generan con Python** a partir del contenido que vive en
un panel (Sanity). Se publica solo en GitHub Pages.

```
  Panel (Sanity)  ──►  src/construir.py  ──►  src/dist/  ──►  GitHub Pages
   el contenido          arma el HTML         22 páginas      el sitio en vivo
```

| Carpeta | Qué es |
|---|---|
| `src/` | El generador del sitio. Python puro, sin dependencias que instalar |
| `src/public/` | CSS, JavaScript, el logo y el favicon |
| `src/home-plantilla.html` | La portada. Las demás páginas las arma `generar.py` |
| `studio/` | El código del panel de edición |
| `admin/` | El panel **ya compilado**. Se genera desde `studio/`, no se edita a mano |

---

## Cómo se trabaja

### Ver el sitio en el computador antes de publicar

```bash
cd src
BASE="" NOINDEX="0" python3 construir.py
cd dist && python3 -m http.server 8000
```
Y abrir `http://localhost:8000`. En Windows con PowerShell:
`$env:BASE=""; $env:NOINDEX="0"; python construir.py`

### Publicar

Basta con `git push` a `main`. Un automatismo reconstruye y publica en ~45 segundos.
**No hay nada más que hacer.** No hay FTP ni servidor que tocar.

### Cambiar el panel

```bash
cd studio
npm install            # solo la primera vez
npx sanity build dist
```
Después hay que arreglar las rutas y copiarlo a `admin/` — ver "El panel" abajo.

---

## REGLAS QUE NO SE ROMPEN

### 1. La dirección web de un producto no se cambia
Cada producto vive en una dirección (`/marquillas-3d/`). Google las tiene indexadas.
Cambiar una **borra esa página de Google** y se pierde el posicionamiento ganado.
Por eso el campo está bloqueado en el panel. En un producto nuevo se genera sola a
partir del título, al construir.

### 2. El contenido se edita en el panel, no en el código
Los textos, las fotos, los productos y las preguntas viven en el panel
(`manufacturasmitchell.com/admin`). Si se escriben a mano en el HTML, **la siguiente
publicación los borra**, porque el HTML se regenera desde el panel cada vez.

Lo que sí vive en el código: la estructura de la portada, el diseño, los textos de
las secciones fijas (Cómo trabajamos, Nosotros) y el pie de página.

### 3. No leer el contenido por el CDN
`generar-desde-panel.py` consulta `api.sanity.io`, **no** `apicdn.sanity.io`. El CDN
guarda copia **por consulta exacta** y devuelve contenido viejo sin dar ningún error:
el sitio se reconstruye "con éxito" y publica lo de antes. Ya pasó una vez.

### 4. Las claves nunca van en el repositorio
El token de Sanity y el de GitHub viven en archivos sueltos **fuera** del proyecto,
en la carpeta personal del usuario. El `.gitignore` los bloquea. Si alguna vez se
sube una por accidente: **hay que revocarla**, no basta con borrarla del repositorio.

### 5. Reescribir archivos completos, no parchearlos a ciegas
Los archivos de este proyecto se rompieron dos veces buscando y reemplazando texto
con anclas imprecisas (un `replace` con cadena vacía insertó código entre cada
carácter de `generar.py`). Si un cambio toca varias partes de un archivo, **reescribir
el archivo entero** y comprobar que el Python sigue siendo válido antes de publicar.

### 6. Comprobar en vivo, no en el código
Que una cadena aparezca en el HTML no significa que se vea. Hay que abrir la página.
Dos casos reales: fotos presentes en el HTML que daban 404, y un contador que decía
"0 fotos" en productos que tenían cuatro.

---

## El panel (Sanity)

- **Proyecto:** `5202v4k4` · dataset `production`
- **Dirección:** `https://manufacturasmitchell.com/admin`
- **Se entra con Google**, no con usuario y contraseña

### Al recompilarlo hay que hacer tres cosas, en este orden

```bash
cd studio && npx sanity build dist
```
1. Reemplazar `/static/` por `/admin/static/` en todos los `.html .js .css .webmanifest`
   de `studio/dist`. Si no, el panel carga en negro.
2. Inyectar en `studio/dist/index.html`, antes del `<title>`, el script que restaura la
   ruta (`mitchell_ruta` en sessionStorage). Sin eso, refrescar el panel da 404.
3. Copiar `studio/dist` sobre `admin/` y hacer push.

El workflow vigila `src/**`, `admin/**` y `.github/workflows/**`. Un cambio solo en
`studio/` **no publica nada** — hay que recompilar a `admin/`.

---

## Cosas que parecen errores y no lo son

| Lo que se ve | Qué pasa de verdad |
|---|---|
| Publico en el panel y no cambia | Tarda ~45 s. Y el navegador guarda la página 10 min: `Ctrl+Shift+R` |
| El panel se ve viejo tras recompilar | Lo mismo: `Ctrl+Shift+R` sobre `/admin` |
| Una tarjeta del catálogo muestra 1 foto y el panel dice 6 | Correcto. La tarjeta muestra la primera; el resto salen en la ficha del producto |
| `/nosotros/` y `/servicios/` no tienen contenido | Son redirecciones del sitio viejo. Existen para no perder esas direcciones en Google |

---

## Lo que sigue pendiente

- Los textos de **Cómo trabajamos** (los 5 pasos) y **Nosotros** están en el código,
  no en el panel. El dueño pidió reescribirlos: hay que pasarlos al panel.
- **Razón social y NIT** están vacíos y el pie los muestra como "por confirmar".
- Faltan **13 líneas de producto** nuevas, a la espera de fotos.
- Falta el **carrusel de logos de clientes** — verificar permisos de uso de esas marcas.
