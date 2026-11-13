import {defineCliConfig} from 'sanity/cli'

// La base cambia segun donde viva el panel:
//   /mitchell-web/admin/  mientras probamos en GitHub Pages
//   /admin/               cuando el dominio propio este conectado
const BASE = process.env.STUDIO_BASE || '/mitchell-web/admin/'

export default defineCliConfig({
  api: {projectId: '5202v4k4', dataset: 'production'},
  vite: (config) => ({...config, base: BASE}),
})
