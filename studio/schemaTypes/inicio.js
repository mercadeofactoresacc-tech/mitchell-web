export default {
  name: 'inicio', type: 'document', title: 'Página de inicio',
  fields: [
    {name:'titular', type:'string', title:'Titular principal',
     description:'Lo primero y más grande que se lee al entrar. Debe decir QUÉ se fabrica y DÓNDE. Máximo 70 letras: más largo se desarma en celular.',
     validation: r => r.required().max(70)},
    {name:'subtitulo', type:'text', rows:3, title:'Texto debajo del titular',
     description:'Dos frases. Una razón para creerles y una razón para escribir hoy.',
     validation: r => r.max(220)},
    {name:'cifras', type:'array', title:'Las cuatro cifras de la franja',
     description:'La franja de números debajo del catálogo. Son exactamente cuatro: con menos se ve incompleta.',
     of:[{type:'object', fields:[
       {name:'numero', type:'string', title:'El número', description:'Ejemplo: 25  ·  +400  ·  24 h'},
       {name:'texto', type:'string', title:'Qué significa', description:'Ejemplo: años fabricando en Bogotá'}
     ], preview:{select:{title:'numero', subtitle:'texto'}}}],
     validation: r => r.max(4).min(4).warning('Deben ser cuatro.')},
  ],
  preview: {prepare: () => ({title: 'Página de inicio', subtitle: 'Titular, texto de entrada y las cuatro cifras'})}
}
