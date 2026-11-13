export default {
  name:'pregunta', type:'document', title:'Pregunta frecuente',
  fields:[
    {name:'pregunta', type:'string', title:'La pregunta',
     description:'Escríbela como la hace el cliente, no como la haría la empresa. "¿Cuál es el mínimo?" y no "Política de cantidades mínimas".',
     validation: r => r.required().max(90)},
    {name:'respuesta', type:'text', rows:5, title:'La respuesta',
     description:'Responde de frente en la primera frase y después explica. Si la respuesta es un número, que el número vaya primero.',
     validation: r => r.required()},
    {name:'orden', type:'number', title:'Posición',
     description:'1 aparece de primera y sale abierta en la página.'},
  ],
  orderings:[{title:'Orden', name:'orden', by:[{field:'orden', direction:'asc'}]}],
  preview:{select:{title:'pregunta', subtitle:'respuesta'}}
}
