export default {
  name: 'empresa', type: 'document', title: 'Datos de la empresa',
  description: 'Se cambian aquí una vez y cambian en las 22 páginas del sitio.',
  groups: [
    {name:'contacto', title:'1. Contacto', default:true},
    {name:'redes', title:'2. Redes sociales'},
    {name:'marca', title:'3. Marca'},
    {name:'legal', title:'4. Datos legales'},
  ],
  fields: [
    {name:'whatsapp', type:'string', title:'WhatsApp', group:'contacto',
     description:'SOLO NÚMEROS, con el 57 del país y sin espacios. Así: 573123794395',
     validation: r => r.required().regex(/^\d{10,15}$/,{name:'solo números'})
       .error('Solo números, empezando por 57. Sin +, sin espacios, sin guiones.')},
    {name:'telefono', type:'string', title:'Teléfono fijo', group:'contacto',
     description:'Tal como quieres que se lea. Ejemplo: (601) 366 0319'},
    {name:'correo', type:'string', title:'Correo electrónico', group:'contacto'},
    {name:'direccion', type:'text', rows:2, title:'Dirección', group:'contacto',
     description:'Calle en la primera línea, barrio y ciudad en la segunda.'},
    {name:'horario', type:'string', title:'Horario de atención', group:'contacto',
     description:'Ejemplo: Lunes a viernes, 7:00 a.m. – 5:00 p.m.'},
    {name:'mapa', type:'url', title:'Enlace del mapa (opcional)', group:'contacto',
     description:'El mapa del sitio se arma solo con la dirección de arriba. Si Google pone el pin en el lugar equivocado, busca la fábrica en Google Maps, dale a Compartir, copia el enlace y pégalo aquí: manda este enlace en vez de la dirección.'},

    {name:'facebook', type:'url', title:'Facebook', group:'redes',
     description:'Pega la dirección completa del perfil. Si lo dejas vacío, el ícono no aparece en la página.'},
    {name:'instagram', type:'url', title:'Instagram', group:'redes',
     description:'Pega la dirección completa del perfil.'},
    {name:'tiktok', type:'url', title:'TikTok', group:'redes',
     description:'Pega la dirección completa del perfil.'},

    {name:'logoLinea1', type:'string', title:'Logo — línea de arriba', group:'marca',
     description:'El texto pequeño del logo. Hoy: Marquillas y clisés'},
    {name:'logoLinea2', type:'string', title:'Logo — línea de abajo', group:'marca',
     description:'El texto grande. Hoy: Mitchell'},
    {name:'anios', type:'number', title:'Años de experiencia', group:'marca',
     description:'Sale en el encabezado y en las cifras de la portada.'},

    {name:'razonSocial', type:'string', title:'Razón social', group:'legal',
     description:'⚠️ Está vacío y el pie de página dice "Razón social por confirmar" a la vista de todos.'},
    {name:'nit', type:'string', title:'NIT', group:'legal',
     description:'⚠️ Está vacío y se ve en el pie de página.'},
  ],
  preview: {prepare: () => ({title: 'Datos de la empresa', subtitle: 'WhatsApp, teléfono, dirección, logo y datos legales'})}
}
