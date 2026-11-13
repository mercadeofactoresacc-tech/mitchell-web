import {defineConfig} from 'sanity'
import {structureTool} from 'sanity/structure'
import {esESLocale} from '@sanity/locale-es-es'
import {schemaTypes} from './schemaTypes'

const SITIO = 'https://manufacturasmitchell.com'

// El menu sigue el ORDEN DE LA PAGINA, de arriba abajo. El dueño no piensa
// "quiero editar el documento inicio": piensa "quiero cambiar eso de arriba".
const FAMILIAS = [
  {titulo: 'Marquillas',      grupo: 'Marquillas'},
  {titulo: 'Clisés',          grupo: 'Clisés'},
  {titulo: 'Apliques en PVC', grupo: 'Apliques en PVC'},
  {titulo: 'Calzado',         grupo: 'Calzado'},
  {titulo: 'Herrajes',        grupo: 'Herrajes'},
  {titulo: 'Publicitario',    grupo: 'Publicitario'},
]

const abrirProducto = (S) => (id) =>
  S.document().schemaType('producto').documentId(id).views([S.view.form().title('Editar')])

const listaFamilia = (S, {titulo, grupo}) =>
  S.listItem().title(titulo).id('fam-' + grupo.replace(/\W/g, ''))
    .child(
      S.documentList().title(titulo)
        .filter('_type == "producto" && grupo == $grupo')
        .params({grupo})
        .defaultOrdering([{field: 'orden', direction: 'asc'}])
        .child(abrirProducto(S))
    )

export default defineConfig({
  name: 'mitchell',
  title: 'Manufacturas Mitchell',
  projectId: '5202v4k4',
  dataset: 'production',
  basePath: '/admin',
  plugins: [structureTool({
    structure: (S) =>
      S.list().title('Qué quieres cambiar').items([

        S.listItem().title('1. Lo primero que se ve').id('inicio')
          .child(S.document().schemaType('inicio').documentId('inicio')
                  .title('Lo primero que se ve')
                  .views([S.view.form().title('Editar')])),

        S.listItem().title('2. Productos y sus fotos').id('productos')
          .child(
            S.list().title('Productos por familia').items([
              ...FAMILIAS.map(f => listaFamilia(S, f)),
              S.divider(),
              S.listItem().title('Ver los 15 juntos').id('todos')
                .child(S.documentTypeList('producto').title('Todos los productos')
                        .defaultOrdering([{field: 'orden', direction: 'asc'}])
                        .child(abrirProducto(S))),
            ])
          ),

        S.listItem().title('3. Preguntas frecuentes').id('preguntas')
          .child(S.documentTypeList('pregunta').title('Preguntas frecuentes')
                  .defaultOrdering([{field: 'orden', direction: 'asc'}])),

        S.divider(),

        S.listItem().title('4. Contacto, logo y redes').id('empresa')
          .child(S.document().schemaType('empresa').documentId('empresa')
                  .title('Contacto, logo y redes')
                  .views([S.view.form().title('Editar')])),
      ])
  }), esESLocale()],
  schema: {types: schemaTypes},
  document: {
    // Boton "Abrir vista previa" en cada documento: lleva a la pagina real.
    productionUrl: async (prev, {document}) => {
      const s = document?.slug?.current
      if (document?._type === 'producto' && s) return `${SITIO}/${s}/`
      if (document?._type === 'inicio')        return `${SITIO}/`
      if (document?._type === 'pregunta')      return `${SITIO}/#preguntas`
      if (document?._type === 'empresa')       return `${SITIO}/contacto/`
      return prev
    },
    // Duplicar si se quita: crea dos paginas con el mismo contenido y Google
    // lo penaliza. Borrar NO se bloquea. Se intento y estaba mal: el caso real
    // no es alguien borrando a lo loco una pagina con posicionamiento, es
    // alguien que publico una prueba por error y queda atrapado con ella a la
    // vista de todos. El panel avisa, no encarcela. Sanity ya pide confirmar.
    actions: (prev, {schemaType}) =>
      schemaType !== 'producto' ? prev : prev
        .filter(a => a.action !== 'duplicate')
        .map(a => a.action !== 'delete' ? a : (props) => {
          const r = a(props)
          return r && {...r, title: props.published
            ? 'Ojo: esta página ya está publicada. Si Google la tiene indexada, esa dirección quedará rota.'
            : r.title}
        }),

    // Puede crear productos y preguntas. Borrar sigue bloqueado en productos:
    // crear una pagina nueva no le hace daño a nadie, borrar una indexada si.
    newDocumentOptions: (prev, {creationContext}) =>
      creationContext.type === 'global'
        ? prev.filter(t => ['pregunta','producto'].includes(t.templateId))
        : prev,
  },
})
