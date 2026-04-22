export const zonasCosta = [
  {
    id: 'rada-tilly',
    nombre: 'Rada Tilly',
    descripcion:
      'Zona costera muy concurrida para actividades recreativas y deportivas. Es importante respetar los sectores habilitados y las indicaciones del personal de guardavidas.',
    imagen: '/imagenes/costa-segura/rada-tilly.webp',
    actividades: ['Natación', 'Caminata', 'Kayak', 'Recreación'],
    guardavidas: 'Sí, en temporada',
    horarioGuardavidas: 'Horario a confirmar',
    consideraciones: [
      'Ingresar solo en sectores habilitados.',
      'Prestar atención al viento y al estado del mar.',
      'Supervisar permanentemente a menores.',
      'Evitar ingresar al agua si hay bandera de advertencia.'
    ],
    coordenadas: {
      lat: -45.933,
      lon: -67.554
    }
  },
  {
    id: 'costa-comodoro',
    nombre: 'Costa Comodoro',
    descripcion:
      'Sector costero urbano con uso recreativo y comunitario. Las condiciones del mar pueden cambiar rápidamente según viento, marea y oleaje.',
    imagen: '/imagenes/costa-segura/Costa-ComodoroRivadavia.jpg',
    actividades: ['Caminata', 'Recreación', 'Observación costera'],
    guardavidas: 'Sí, según sector y temporada',
    horarioGuardavidas: 'Horario a confirmar',
    consideraciones: [
      'Respetar siempre la cartelería y señalización local.',
      'No ingresar al mar en zonas no habilitadas.',
      'Evitar acercarse a sectores rocosos con marea cambiante.',
      'Consultar las condiciones antes de realizar actividades.'
    ],
    coordenadas: {
      lat: -45.864,
      lon: -67.483
    }
  },
  {
    id: 'caleta-cordova',
    nombre: 'Caleta Córdova',
    descripcion:
      'Área costera de interés recreativo, comunitario y paisajístico. Las condiciones naturales del lugar requieren atención a la marea, el viento y el tipo de costa.',
    imagen: '/imagenes/costa-segura/Costa-caleta-cordova.jpg',
    actividades: ['Pesca recreativa', 'Caminata', 'Observación del mar'],
    guardavidas: 'A confirmar',
    horarioGuardavidas: 'Horario a confirmar',
    consideraciones: [
      'Prestar especial atención a la marea.',
      'Evitar circular por sectores resbaladizos o rocosos sin precaución.',
      'No realizar actividades acuáticas sin conocer el lugar.',
      'Consultar siempre el estado general del entorno.'
    ],
    coordenadas: {
      lat: -45.748,
      lon: -67.366
    }
  }
 /* {
    id: 'restinga-ali',
    nombre: 'Restinga Alí',
    descripcion:
      'Zona costera con características naturales particulares, donde las condiciones del mar y del terreno pueden variar notablemente según el momento del día y el clima.',
    imagen: '/imagenes/costa-segura/restinga-ali.jpg',
    actividades: ['Caminata', 'Pesca recreativa', 'Observación costera'],
    guardavidas: 'A confirmar',
    horarioGuardavidas: 'Horario a confirmar',
    consideraciones: [
      'Evitar ingresar a sectores desconocidos sin información previa.',
      'Prestar atención a cambios en el viento y a la subida de la marea.',
      'Usar calzado adecuado en zonas de piedra o superficie irregular.',
      'No sobreestimar la seguridad del lugar por aparente calma.'
    ],
    coordenadas: {
      lat: -45.793,
      lon: -67.383
    } 
  } */
];

export const enlacesExternos = [
  {
    nombre: 'Servicio de Hidrografía Naval',
    descripcion: 'Información oficial sobre mareas y condiciones marítimas.',
    url: 'https://www.hidro.gov.ar'
  },
  {
    nombre: 'Windy',
    descripcion: 'Visualización meteorológica y oceánica con mapas interactivos.',
    url: 'https://www.windy.com'
  },
  {
    nombre: 'Windguru',
    descripcion: 'Pronóstico de viento y oleaje para actividades costeras y náuticas.',
    url: 'https://www.windguru.cz'
  },
  {
    nombre: 'Prefectura Naval Argentina',
    descripcion: 'Información oficial y avisos relacionados con navegación y seguridad.',
    url: 'https://www.argentina.gob.ar/prefecturanaval'
  }
];

export const recomendacionesGenerales = [
  'Ingresar al mar únicamente en sectores habilitados.',
  'Respetar siempre las indicaciones del cuerpo de guardavidas.',
  'No ingresar solo al agua.',
  'Evitar entrar al mar con viento fuerte o mar agitado.',
  'Supervisar permanentemente a niñas, niños y adolescentes.',
  'Ante dudas sobre las condiciones, no ingresar al agua.'
];

export const contenidoEducativo = [
  {
    titulo: 'Cómo influye el viento',
    texto:
      'La dirección e intensidad del viento pueden modificar el oleaje, la dificultad para nadar y la seguridad general de una actividad costera.'
  },
  {
    titulo: 'Por qué importa la marea',
    texto:
      'La marea cambia la línea de costa, la profundidad y las condiciones del entorno. Un lugar aparentemente seguro puede cambiar en pocas horas.'
  },
  {
    titulo: 'Qué observar antes de entrar al mar',
    texto:
      'Es recomendable revisar el estado del mar, la señalización, la presencia de guardavidas y las condiciones generales del tiempo.'
  }
];