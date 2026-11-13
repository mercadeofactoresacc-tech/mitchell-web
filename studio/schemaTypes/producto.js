export default {
  name: 'producto', type: 'document', title: 'Producto',
  groups: [
    {name: 'texto',  title: '1. Textos',  default: true},
    {name: 'fotos',  title: '2. Fotos'},
    {name: 'ficha',  title: '3. Ficha técnica'},
    {name: 'avanzado', title: 'Avanzado'},
  ],
  fields: [
    {name:'nombre', type:'string', title:'Título del producto', group:'texto',
     description:'Es el título grande de la página y el nombre en el catálogo. Ojo: si lo haces muy específico (una sola técnica), las fotos de otras técnicas dejan de encajar.',
     validation: r => r.required().max(48).warning('Más de 48 letras se ve apretado en celular.')},

    {name:'descripcion', type:'text', rows:6, title:'Descripción', group:'texto',
     description:'El párrafo que se lee debajo del título. Di de qué material es, para qué sirve y qué gana el cliente. Las primeras 20 palabras son las que salen en la tarjeta del catálogo.',
     validation: r => r.required().min(60).warning('Muy corta: menos de 60 letras se ve descuidado.')},

    {name:'fotos', type:'array', title:'Fotos del producto', group:'fotos',
     description:'DÓNDE SALE CADA FOTO — La 1.ª es la única que se ve en el catálogo de la portada, y es también la foto grande de esta ficha. De la 2.ª en adelante salen en la galería "Piezas que han salido de la planta", más abajo en esta misma ficha. Para cambiar la del catálogo, arrastra otra al primer puesto con el icono de puntos de la izquierda.',
     of:[{
       type:'image', options:{hotspot:true},
       fields:[{name:'alt', type:'string', title:'¿Qué se ve en esta foto?',
                description:'Escríbelo y aparecerá como nombre de la foto en esta lista. Además es lo que lee Google. Ejemplo: marquilla tejida dorada sobre tela negra'}],
       preview:{
         select:{alt:'alt', archivo:'asset.originalFilename', media:'asset'},
         prepare:({alt, archivo, media}) => ({
           title: alt || archivo || 'Sin descripción',
           subtitle: alt ? archivo : 'Sin descripción — escríbela para reconocerla',
           media,
         }),
       },
     }],
     validation: r => r.min(1).warning('Un producto sin foto casi no se consulta.')},

    {name:'minimo', type:'string', title:'Mínimo de pedido', group:'ficha',
     description:'Ejemplo: 500 unidades'},
    {name:'entrega', type:'string', title:'Tiempo de entrega', group:'ficha',
     description:'Ejemplo: 8 días hábiles'},
    {name:'ficha', type:'array', title:'Tabla de especificaciones', group:'ficha',
     description:'Cada fila es un dato. A la izquierda el nombre, a la derecha el valor.',
     of:[{type:'object', fields:[
       {name:'campo', type:'string', title:'Nombre del dato', description:'Ejemplo: Material'},
       {name:'valor', type:'string', title:'Valor', description:'Ejemplo: Damasco, satén, taffeta'}
     ], preview:{select:{title:'campo', subtitle:'valor'}}}]},

    {name:'grupo', type:'string', title:'Familia', group:'avanzado',
     description:'Define en qué filtro del catálogo aparece.',
     options:{list:['Marquillas','Clisés','Apliques en PVC','Calzado','Herrajes','Publicitario']}},
    {name:'orden', type:'number', title:'Posición en el catálogo', group:'avanzado',
     description:'1 aparece de primero.'},
    {name:'slug', type:'slug', title:'Dirección web', group:'avanzado',
     // El cliente no deberia ver nunca este campo. En un producto nuevo la
     // direccion se arma sola con el titulo, al construir el sitio. Aqui solo
     // aparece -y bloqueada- en los que ya la tienen, como referencia.
     readOnly: true,
     hidden: ({value}) => !value,
     description:'🔒 Es la dirección de esta página en internet. Se bloquea a propósito: si se cambia, Google pierde la página y el posicionamiento que ya tenía.',
     options:{source:'nombre', maxLength:60}},
  ],
  orderings:[
    {title:'Orden del catálogo', name:'orden', by:[{field:'orden', direction:'asc'}]},
    {title:'Por familia', name:'familia', by:[{field:'grupo',direction:'asc'},{field:'orden',direction:'asc'}]},
    {title:'Alfabético', name:'az', by:[{field:'nombre', direction:'asc'}]},
  ],
  // Sanity no resuelve 'fotos.length' ni el arreglo completo, y tampoco
  // 'fotos.N.asset._ref'. Lo que SI resuelve es 'fotos.N.asset', igual que media.
  preview:{
    select:{
      title:'nombre', grupo:'grupo', media:'fotos.0.asset',
      f0:'fotos.0.asset', f1:'fotos.1.asset', f2:'fotos.2.asset',
      f3:'fotos.3.asset', f4:'fotos.4.asset', f5:'fotos.5.asset',
    },
    prepare(s){
      const n = ['f0','f1','f2','f3','f4','f5'].filter(k => s[k]).length
      const cuenta = n === 0 ? 'sin fotos' : n > 5 ? '6 o más fotos' : n + (n===1 ? ' foto' : ' fotos')
      return {title: s.title, media: s.media, subtitle: (s.grupo || 'sin familia') + ' · ' + cuenta}
    }
  }
}
