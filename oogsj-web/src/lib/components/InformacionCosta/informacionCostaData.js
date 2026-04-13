export const temasCosta = [
  {
    icono: '🌬️',
    titulo: 'Viento',
    descripcion: 'Aprendé cómo influye en la costa, el mar y las actividades recreativas.'
  },
  {
    icono: '🌊',
    titulo: 'Oleaje',
    descripcion: 'Entendé mejor la altura, energía y comportamiento de las olas.'
  },
  {
    icono: '🌗',
    titulo: 'Mareas',
    descripcion: 'Conocé cómo cambian las condiciones de la costa a lo largo del día.'
  },
  {
    icono: '🚩',
    titulo: 'Banderas',
    descripcion: 'Interpretá señales visuales de precaución, peligro y condiciones del mar.'
  },
  {
    icono: '🌀',
    titulo: 'Corrientes',
    descripcion: 'Identificá situaciones donde el agua puede arrastrarte o complicar el regreso.'
  },
  {
    icono: '🏄',
    titulo: 'Actividades',
    descripcion: 'Recomendaciones básicas para disfrutar la costa con más información.'
  },
  {
    icono: '🐋',
    titulo: 'Ambiente',
    descripcion: 'Valorá la fauna, el entorno costero y la importancia de cuidarlo.'
  }
];

export const escenariosCosta = [
  {
    icono: '🌬️',
    titulo: 'Viento hacia la costa',
    descripcion:
      'Cuando el viento sopla desde el mar hacia la playa, suele empujar hacia la orilla y puede dar una sensación de mayor control cerca de la costa.',
    implica:
      'Puede resultar más favorable para ciertas actividades recreativas cerca de la orilla, aunque igualmente hay que observar oleaje y corrientes.',
    accion:
      'Prestá atención al estado general del mar y elegí sectores habilitados o vigilados.'
  },
  {
    icono: '🌀',
    titulo: 'Viento mar adentro',
    descripcion:
      'Cuando el viento empuja desde la costa hacia el mar, puede alejar rápidamente a personas, tablas, kayaks u otros elementos flotantes.',
    implica:
      'Aumenta el riesgo de perder cercanía con la orilla, especialmente en actividades con inflables, SUP o kayak.',
    accion:
      'Evitá ingresar con elementos livianos o flotantes si notás que el viento te empuja mar adentro.'
  },
  {
    icono: '🌊',
    titulo: 'Oleaje fuerte',
    descripcion:
      'Las olas con mayor energía pueden generar rompientes más intensas, pérdida de estabilidad y dificultad para salir del agua.',
    implica:
      'Puede haber golpes, arrastre y cansancio más rápido, sobre todo en personas con poca experiencia.',
    accion:
      'Observá varios minutos antes de ingresar y evitá entrar si el comportamiento del mar se ve inestable o exigente.'
  },
  {
    icono: '🌗',
    titulo: 'Cambio de marea',
    descripcion:
      'La marea modifica la forma de la costa, el espacio disponible en la playa y el comportamiento del agua en ciertos sectores.',
    implica:
      'Puede generar cambios en accesos, profundidad y dinámica del mar cerca de rocas, restingas o canales.',
    accion:
      'No te guíes solo por cómo viste la playa unas horas antes; las condiciones pueden cambiar.'
  }
];

export const checklistCosta = [
  {
    numero: '01',
    titulo: 'Mirá la señalización del lugar',
    descripcion:
      'Antes de ingresar, observá cartelería, banderas y cualquier indicación visible en la zona.'
  },
  {
    numero: '02',
    titulo: 'Observá el viento',
    descripcion:
      'Detectá si el viento empuja hacia la playa o hacia mar adentro. Eso cambia mucho las condiciones.'
  },
  {
    numero: '03',
    titulo: 'Revisá el oleaje',
    descripcion:
      'Tomate unos minutos para mirar el comportamiento del mar antes de decidir ingresar.'
  },
  {
    numero: '04',
    titulo: 'Elegí zonas concurridas o vigiladas',
    descripcion:
      'Siempre es mejor priorizar sectores donde haya más presencia de personas o controles.'
  },
  {
    numero: '05',
    titulo: 'No ingreses solo',
    descripcion:
      'Entrar acompañado reduce riesgos y permite una mejor respuesta ante cualquier problema.'
  },
  {
    numero: '06',
    titulo: 'Prestá atención a cambios del entorno',
    descripcion:
      'El viento, el oleaje y la marea pueden cambiar. No des por estable una condición que ya cambió.'
  }
];

// ─── AGREGAR este export al final de informacionCostaData.js ──────────────
// Los exports existentes (temasCosta, escenariosCosta, checklistCosta) se mantienen intactos.

export const categoriasTemas = [
  {
    id: 'mar',
    titulo: 'El Mar',
    icono: '🌊',
    temas: [
      {
        id: 'olas',
        icono: '🌊',
        titulo: 'Cómo leer el mar',
        descripcion:
          'El comportamiento de las olas da señales claras sobre el estado del mar antes de ingresar.',
        contenido: {
          intro:
            'Las olas no son aleatorias. Su tamaño, frecuencia y forma en la costa brindan información concreta sobre la energía del mar en ese momento. Aprender a observarlas permite tomar decisiones con más criterio.',
          puntos: [
            {
              titulo: 'Altura de ola',
              texto:
                'Se mide desde el punto más bajo (valle) hasta el punto más alto (cresta). Olas más altas implican mayor energía y pueden dificultar el ingreso o permanencia en el agua.'
            },
            {
              titulo: 'Período',
              texto:
                'Es el tiempo entre dos crestas consecutivas. Un período largo indica olas más organizadas, con mayor energía y alcance. Un período corto indica oleaje fragmentado y menos potente.'
            },
            {
              titulo: 'Zona de rompiente',
              texto:
                'Área donde las olas pierden profundidad y colapsan. Su distancia de la orilla y la forma en que rompen indican cuánta energía liberan y qué tan profundo es el fondo.'
            },
            {
              titulo: 'Corrientes de retorno',
              texto:
                'Cuando las olas rompen cerca de la orilla, el agua vuelve al mar formando corrientes. Son difíciles de ver pero pueden arrastrar a una persona rápidamente hacia afuera.'
            }
          ],
          nota: 'El oleaje puede cambiar con rapidez. Condiciones aparentemente calmas pueden modificarse en minutos por efecto del viento o la marea.'
        }
      },
      {
        id: 'mareas',
        icono: '🌙',
        titulo: 'Mareas',
        descripcion:
          'La variación del nivel del mar afecta profundidades, corrientes y zonas de acceso a lo largo del día.',
        contenido: {
          intro:
            'Las mareas son el ascenso y descenso periódico del nivel del mar, producido principalmente por la atracción gravitacional de la Luna y el Sol. En el Golfo San Jorge, son un factor clave para entender el entorno costero.',
          puntos: [
            {
              titulo: 'Pleamar y bajamar',
              texto:
                'La pleamar es el nivel máximo del agua; la bajamar, el mínimo. Entre ambos estados transcurren aproximadamente 6 horas. El ciclo se repite dos veces por día (mareas semidiurnas).'
            },
            {
              titulo: 'Amplitud mareal',
              texto:
                'En el Golfo San Jorge, la diferencia entre pleamar y bajamar puede superar los 5 metros en algunos sectores, modificando significativamente las zonas accesibles y la extensión de playa.'
            },
            {
              titulo: 'Efecto en corrientes',
              texto:
                'El cambio de marea genera corrientes que fluyen a lo largo y hacia afuera del mar. Durante la transición (marea vaciante), las corrientes pueden ser especialmente intensas.'
            },
            {
              titulo: 'Zonas expuestas',
              texto:
                'Con marea baja se exponen rocas, pozas y fondos que en pleamar permanecen cubiertos. Estas zonas pueden ser resbaladizas y albergar fauna marina frágil.'
            }
          ],
          nota: 'Las tablas de mareas locales indican el estado del mar para cada hora del día. Consultarlas antes de actividades costeras es una práctica recomendada.'
        }
      }
    ]
  },
  {
    id: 'viento',
    titulo: 'El Viento',
    icono: '💨',
    temas: [
      {
        id: 'viento',
        icono: '💨',
        titulo: 'Viento en la costa',
        descripcion:
          'La dirección y velocidad del viento cambia las condiciones del mar y determina riesgos según cada actividad.',
        contenido: {
          intro:
            'El viento es uno de los factores más influyentes en la costa. No solo genera oleaje: también determina corrientes superficiales, afecta la temperatura percibida y puede crear situaciones de riesgo para actividades en el agua.',
          puntos: [
            {
              titulo: 'Viento hacia la costa (onshore)',
              texto:
                'Sopla desde el mar hacia la tierra. Genera olas que rompen con más frecuencia cerca de la orilla. Puede dificultar el ingreso al agua pero facilita el regreso. La temperatura percibida baja notablemente.'
            },
            {
              titulo: 'Viento desde la costa (offshore)',
              texto:
                'Sopla desde la tierra hacia el mar. Puede parecer inofensivo pero representa un riesgo importante: arrastra hacia afuera colchonetas, flotadores y embarcaciones pequeñas, incluso a baja velocidad.'
            },
            {
              titulo: 'Ráfagas',
              texto:
                'Son aumentos repentinos y breves de la velocidad del viento. En la Patagonia son frecuentes y pueden sorprender incluso cuando el viento base parecía moderado, amplificando el efecto de arrastre offshore.'
            },
            {
              titulo: 'Viento en el Golfo San Jorge',
              texto:
                'La región presenta predominancia de vientos del oeste y suroeste, especialmente en primavera y verano. Su intensidad puede variar significativamente a lo largo del día.'
            }
          ],
          nota: 'La percepción de viento suave desde la costa puede ser engañosa. A baja velocidad ya puede arrastrar flotadores o embarcaciones livianas lejos de la orilla.'
        }
      }
    ]
  },
  {
    id: 'prevencion',
    titulo: 'Prevención',
    icono: '⚠️',
    temas: [
      {
        id: 'precauciones',
        icono: '⚠️',
        titulo: 'Precauciones generales',
        descripcion:
          'Conocer el entorno costero patagónico y anticiparse a sus condiciones es la forma más efectiva de disfrutarlo.',
        contenido: {
          intro:
            'La costa patagónica tiene características propias que la diferencian de otros entornos. La temperatura del agua, la amplitud mareal y los vientos frecuentes hacen que la preparación y la observación sean especialmente importantes.',
          puntos: [
            {
              titulo: 'No ingresar solo al agua',
              texto:
                'Siempre es recomendable tener al menos otra persona presente que pueda asistir o pedir ayuda en caso necesario. Aplica tanto en playas habilitadas como en zonas naturales.'
            },
            {
              titulo: 'Temperatura del agua',
              texto:
                'El agua del Golfo San Jorge es fría durante todo el año. El ingreso sin preparación puede provocar hiperventilación y reducir la capacidad de respuesta ante una situación imprevista.'
            },
            {
              titulo: 'Flotadores y colchonetas',
              texto:
                'Con viento offshore, incluso suave, estos elementos pueden alejarse rápidamente de la orilla. No utilizarlos como apoyo para adentrarse en el mar y retirarlos si el viento aumenta.'
            },
            {
              titulo: 'Respetar las indicaciones',
              texto:
                'Las señales, banderas y recomendaciones del personal de guardavidas se basan en el conocimiento del entorno local. Seguirlas contribuye a una experiencia más consciente para todos.'
            },
            {
              titulo: 'Marea roja',
              texto:
                'En determinados períodos, floraciones de microalgas pueden hacer peligroso el consumo de mariscos y moluscos. Ante avisos de marea roja, no recolectar ni consumir estos organismos.'
            }
          ],
          nota: 'Esta información tiene carácter educativo y preventivo. No reemplaza la evaluación en terreno ni las indicaciones de los organismos responsables de cada playa o zona costera.'
        }
      }
    ]
  }
];