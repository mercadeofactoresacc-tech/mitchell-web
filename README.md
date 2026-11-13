# Sitio web de Manufacturas Mitchell

El sitio `https://manufacturasmitchell.com` y su panel de edición.

Si vas a trabajar con Claude Code en este proyecto, **él ya sabe qué hacer**: las
reglas están en `CLAUDE.md` y las lee solo al abrir la carpeta.

---

## Lo que hay aquí

| Carpeta | Qué es |
|---|---|
| `src/` | El generador del sitio (Python) |
| `studio/` | El código del panel de edición |
| `admin/` | El panel ya compilado, listo para servir |

---

## Instalación en Windows (una sola vez)

### 1. Los tres programas base

| Programa | Dónde | Al instalar |
|---|---|---|
| **Git** | git-scm.com | Dejar todo por defecto |
| **Python** | python.org | ⚠️ Marcar **"Add Python to PATH"** en la primera pantalla |
| **Node.js** | nodejs.org | Versión **LTS**. Solo hace falta para el panel |

Comprobar que quedaron bien, en PowerShell:

```powershell
git --version ; python --version ; node --version
```

Si alguno dice que no se reconoce el comando, hay que reinstalarlo. Python falla casi
siempre por no haber marcado "Add Python to PATH".

### 2. Claude Code

```powershell
npm install -g @anthropic-ai/claude-code
```

### 3. Traer el proyecto

```powershell
cd $HOME
git clone https://github.com/mercadeofactoresacc-tech/mitchell-web.git
cd mitchell-web
claude
```

La primera vez pide iniciar sesión en el navegador.

---

## El día a día

### Ver el sitio en tu computador antes de publicar

```powershell
cd src
$env:BASE=""; $env:NOINDEX="0"; python construir.py
cd dist
python -m http.server 8000
```

Abrir `http://localhost:8000`. Para detenerlo: `Ctrl+C`.

### Publicar los cambios

```powershell
git add -A
git commit -m "qué cambié"
git push
```

En ~45 segundos está en vivo. No hay nada más que hacer.

### Si algo salió mal

```powershell
git log --oneline -5      # ver los últimos cambios
git revert HEAD           # deshacer el último
git push
```

O pedírselo a Claude: *"devuélveme el sitio a como estaba antes del último cambio"*.

---

## Lo que NO necesita tocar código

Textos, fotos, productos, preguntas frecuentes, teléfono, dirección y redes sociales
se editan en **`https://manufacturasmitchell.com/admin`**, desde el navegador, sin
instalar nada. Se entra con Google.

El código solo hace falta para cambiar el **diseño** o la **estructura** de la página.
