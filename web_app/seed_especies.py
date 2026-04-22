"""
Seed script: inserta las especies del catálogo estático en oogsj_data.especie.
Ejecutar UNA sola vez desde el contenedor web_app o con las variables de entorno correctas:

    docker-compose exec web_app python seed_especies.py
"""

import sys
import psycopg2
import config

ESPECIES = [
    {
        "nombre_comun":      "Abadejo",
        "nombre_cientifico": "Genypterus blacodes",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/abadejo.webp",
        "descripcion": """Familia: Ophidiidae

Cuerpo grueso anteriormente, adelgazándose hacia el extremo caudal. Escamas muy pequeñas en cuerpo y cabeza, gran cantidad de mucus protege la piel.

Cabeza robusta, hocico romo, ojos grandes. Boca con ligero prognatismo de la mandíbula superior. Los dientes de las mandíbulas son pequeños, biseriados, cónicos los de la fila externa y viliformes los de la interna. Presenta además dientes vomerinos y palatinos.

Una única aleta impar, formada por la fusión de dorsal, caudal y anal. Pectorales pequeñas. Ventrales en posición yugular, reducidas a una barba dividida en dos ramas.

Coloración: rosado intenso en dorso y flancos, aclarándose hacia la región abdominal, hasta llegar al blanco en el vientre. En el dorso y los flancos, manchas marrones que dan al conjunto aspecto marmolado.

Tamaño: La talla máxima observada (135 cm) corresponde a una hembra; los machos no exceden los 125 cm de longitud total.

Distribución: Habita aguas pacíficas y atlánticas sudamericanas. Por el Atlántico desde los 34° S. Los adultos tendrían tendencia a habitar en cañones submarinos, en el borde de la plataforma continental. Los juveniles permanecen en aguas costeras y son frecuentes en el Golfo San Jorge.

Tamaño del recurso: Moderado.

Formas de utilización: Se exporta entero, H&G y filet interfoliado con o sin piel.""",
    },
    {
        "nombre_comun":      "Besugo",
        "nombre_cientifico": "Pagrus pagrus",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/besugo.webp",
        "descripcion": """Familia: Sparidae

Cuerpo oblongo, comprimido, perfil dorsal más convexo que el ventral. Cubierto de escamas ctenoideas. Cabeza con perfil dorsal fuertemente convexo. Hocico corto, boca terminal. Dentición con caninos, dientes romos y molariformes. Aleta dorsal con 12 espinas y 8-11 radios blandos. Caudal furcada.

Coloración: rosada uniforme con pequeñas manchas azules, acentuadas en la cabeza. Aletas amarillo-rosadas.

Tamaño: Talla máxima observada: 54 cm.

Biología: Puesta anual entre diciembre y enero. Hermafroditismo juvenil. Madurez completa al quinto año. Talla de madurez: 23 cm. Longevidad: hasta 16 años.

Distribución: Presente en el Mediterráneo y en ambas márgenes del Atlántico. En Argentina, en fondos duros de la región bonaerense entre 10 y 50 m. También en el Golfo San Matías de forma estacional.

Tamaño del recurso: Pequeño.

Formas de utilización: Se exporta entero congelado, H&G y filetes con y sin piel. También se exporta fresco vía aérea.""",
    },
    {
        "nombre_comun":      "Caballa",
        "nombre_cientifico": "Scomber colias",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/caballa.webp",
        "descripcion": """Familia: Scombridae

Otros nombres: Argentina: magrú — Brasil: cavalinha — Inglés: Atlantic chub mackerel.

Cuerpo alargado, fusiforme, robusto, cubierto de escamas diminutas. Cabeza pequeña con boca terminal. Dos aletas dorsales, caudal furcada, y pínulas detrás de dorsal y anal.

Coloración: Dorso azul verdoso marmorado, flancos y vientre blanco iridiscente.

Tamaño: Hasta 57 cm; comúnmente entre 20-45 cm.

Biología: Se reproduce en primavera tardía y verano, de noche, con temperaturas entre 16°-17°C. Desova de 4 a 5 veces. Crecimiento rápido; puede vivir hasta 13 años.

Alimentación: Plancton, peces (principalmente anchoíta, sureles, cornalitos) y calamares.

Distribución: En Mar del Plata de septiembre a febrero. Cardúmenes en El Rincón y norte patagónico. En invierno en la plataforma (100-200 m) y en verano se acerca a la costa.

Tamaño del recurso: Grande.

Formas de utilización: Principalmente para conservería y mercado interno.""",
    },
    {
        "nombre_comun":      "Langostino",
        "nombre_cientifico": "Pleoticus muelleri",
        "categoria":         "Invertebrados",
        "imagen_url":        "/imagenes/Especies/langostino.png",
        "descripcion": """Familia: Solenoceridae

Nombre en inglés: Argentine red shrimp.

Cuerpo alargado y comprimido lateralmente, cubierto por un caparazón con surcos característicos. Presenta un rostro largo y curvado hacia arriba con dientes. Coloración general rojiza a rosada, más intensa en adultos. Tiene cinco pares de patas torácicas, el primero con pinzas prominentes.

Tamaño: Puede alcanzar hasta 22 cm de longitud total. El tamaño comercial más frecuente es entre 12 y 18 cm.

Biología: La reproducción se produce en aguas profundas del talud continental, principalmente entre noviembre y marzo. La madurez sexual se alcanza al primer año de vida.

Alimentación: Son omnívoros. Se alimentan de pequeños crustáceos, gusanos, detritos orgánicos y materia vegetal.

Distribución: Se encuentra principalmente en el Mar Argentino, desde Río de Janeiro hasta el sur de Santa Cruz, siendo más abundante entre los paralelos 42° y 47°S, en profundidades entre 50 y 250 metros.

Importancia comercial: Es una de las especies pesqueras más valiosas de la Argentina. Se exporta principalmente a Europa y Asia.

Pesca y uso: Se captura mediante redes de arrastre. La flota langostinera opera mayoritariamente en la provincia de Chubut y parte de Santa Cruz.""",
    },
    {
        "nombre_comun":      "Merluza común",
        "nombre_cientifico": "Merluccius hubbsi",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/merluza.png",
        "descripcion": """Familia: Merlucciidae

Otros nombres: Argentina: merluza hubbsi — Brasil: merluza — Inglés: Argentine hake.

Cuerpo alargado y fusiforme, cubierto de escamas cicloides. Cabeza grande y robusta con boca terminal y dientes fuertes. Posee dos aletas dorsales claramente separadas y caudal truncada.

Coloración: Gris claro en cabeza y dorso, blanco tiza en la zona ventral. Reflejos dorados en todo el cuerpo.

Tamaño: Hasta 95 cm en hembras y 60 cm en machos. Capturas comerciales entre 25-40 cm.

Biología: Reproductor parcial con actividad reproductiva casi todo el año. Madurez sexual: hembras (36 cm), machos (33 cm), entre 3 y 4 años. Existen zonas de concentración de juveniles en el Golfo San Jorge.

Alimentación: Zooplanctófaga hasta los 30-35 cm. Luego predadora carnívora y oportunista. Frecuente canibalismo.

Distribución: Desde Cabo Frío (Brasil, 22° S) hasta el sur de Argentina (55° S), en profundidades entre 50 y 500 m. Prefiere temperaturas entre 5° y 10° C.

Tamaño del recurso: Grande.

Formas de utilización: Base de la industria pesquera argentina. Se exporta como filet congelado, H&G, en salazón y fresco. Muy importante también en el mercado interno.""",
    },
    {
        "nombre_comun":      "Centolla",
        "nombre_cientifico": "Lithodes santolla",
        "categoria":         "Invertebrados",
        "imagen_url":        "/imagenes/Especies/centolla.webp",
        "descripcion": """Clase: Malacostraca — Orden: Decapoda — Familia: Lithodidae
Nombre en inglés: King crab.

Distribución geográfica: Habita aguas templado-frías (4°-15°C) del Atlántico suroccidental: desde las Islas Malvinas y Tierra del Fuego hasta el Golfo San Jorge, siguiendo la Corriente de Malvinas hasta el sur de Brasil. También está presente en las costas chilenas del Pacífico. Se encuentra desde el litoral hasta profundidades de 700 m, concentrándose comercialmente entre 30 y 120 m.

Poblaciones:
- Canal Beagle: veda permanente desde 1994 por sobrepesca.
- Costa atlántica de Tierra del Fuego y Santa Cruz: explotado artesanalmente.
- Golfo San Jorge: explotado por flotas costeras y capturado como bycatch.

Características biológicas:
- Reproducción anual. Las hembras incuban los huevos durante 10 meses.
- Se estima una vida útil de 14 años.

Importancia pesquera: La centolla es muy apreciada y su carne es considerada un manjar. En el Golfo San Jorge se están desarrollando nuevas pesquerías con trampas por la expansión poblacional en esa zona.""",
    },
    {
        "nombre_comun":      "Pez Gallo",
        "nombre_cientifico": "Callorinchus callorynchus",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/PezGallo.webp",
        "descripcion": """Clase: Chondrichthyes — Orden: Chimaeriformes — Familia: Callorhinchidae.

Este pez cartilaginoso posee un cuerpo fusiforme, robusto, recubierto por una piel lisa sin escamas. Su característica más notable es una prolongación en la parte frontal de la cabeza que recuerda a una trompa, utilizada para detectar presas en el fondo marino (de ahí el nombre de "pez elefante" o "pez gallo"). Su boca está ubicada en la parte inferior de la cabeza y contiene placas dentarias para triturar.

Coloración: Gris plateado con reflejos azulados y manchas oscuras en el dorso, vientre blanco.

Tamaño: Puede alcanzar hasta 1 metro de longitud total; los ejemplares más comunes miden entre 40 y 70 cm.

Distribución y hábitat: Océano Atlántico sudoccidental, principalmente entre el sur de Brasil, Uruguay y Argentina, desde aguas costeras hasta profundidades de 200 metros. Se encuentra sobre fondos arenosos o fangosos (especie bentónica).

Alimentación: Invertebrados del fondo como moluscos, crustáceos y poliquetos.

Reproducción: Es ovíparo. Las hembras depositan huevos de gran tamaño con forma de cápsulas alargadas.

Importancia comercial: Tiene valor comercial regional en Argentina y Uruguay, capturado con redes de arrastre junto a otras especies demersales.""",
    },
    {
        "nombre_comun":      "Robálo",
        "nombre_cientifico": "Eleginops maclovinus",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/robalo.webp",
        "descripcion": """Clase: Actinopterygii — Orden: Perciformes — Familia: Eleginopidae.

Pez de cuerpo alargado, fusiforme y comprimido lateralmente, con una apariencia robusta y fuerte. Posee una cabeza grande, boca amplia y ligeramente oblicua, con dientes cónicos bien desarrollados. Tiene dos aletas dorsales separadas: la primera con radios espinosos y la segunda con radios blandos. La aleta caudal es ligeramente ahorquillada.

Coloración: Gris verdoso o marrón oscuro en el dorso, aclarando hacia los flancos y el vientre blanco plateado.

Distribución y hábitat: Especie costera del litoral patagónico argentino y chileno, desde el Golfo San Matías hasta Tierra del Fuego. Se encuentra en estuarios, desembocaduras de ríos, bahías y zonas arenosas, y puede ingresar ocasionalmente en aguas dulces.

Tamaño: Puede alcanzar tallas de hasta 90 cm; las capturas comerciales oscilan entre 40 y 70 cm.

Alimentación: Carnívoro. Se alimenta de crustáceos, peces pequeños, moluscos y otros invertebrados bentónicos.

Importancia comercial: Tiene importante valor pesquero y gastronómico. Muy buscado por pescadores deportivos. Su carne blanca, firme y sabrosa lo convierte en un pescado apreciado en la cocina regional.""",
    },
    {
        "nombre_comun":      "Pejerrey",
        "nombre_cientifico": "Odontesthes spp.",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/pejerrey.webp",
        "descripcion": """Clase: Actinopterygii — Orden: Atheriniformes — Familia: Atherinopsidae.

Pez de cuerpo esbelto, alargado y ligeramente comprimido. Presenta una cabeza pequeña y boca protráctil orientada hacia arriba. Tiene dos aletas dorsales separadas. Su característica más notable es una línea plateada brillante que recorre ambos flancos del cuerpo.

Coloración: Dorso verdoso a azulado, flancos plateados y vientre blanco. Reflejos iridiscentes.

Tamaño: Dependiendo de la especie y del ambiente, puede medir entre 20 y 45 cm, aunque algunos ejemplares pueden superar los 50 cm.

Distribución y hábitat: Presente en ambientes costeros marinos, estuarios, lagunas y ríos de agua dulce. Se distribuye ampliamente en el sur de Brasil, Uruguay y Argentina, siendo muy común en la región pampeana y costera del Atlántico sudoccidental.

Alimentación: Omnívoro y oportunista. Se alimenta de zooplancton, insectos acuáticos, crustáceos, pequeños peces e incluso huevos de otras especies.

Reproducción: Desova entre fines del invierno y la primavera, en aguas templadas y bien oxigenadas.

Importancia: Una de las especies más emblemáticas para la pesca deportiva en Argentina y Uruguay. También tiene valor comercial. Su carne es blanca, sabrosa y libre de espinas grandes.""",
    },
    {
        "nombre_comun":      "Salmón de mar",
        "nombre_cientifico": "Pseudopercis semifasciata",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/salmon.webp",
        "descripcion": """Clase: Actinopterygii — Orden: Perciformes — Familia: Pinguipedidae.

También llamado salmonete. Pez demersal de cuerpo alargado, ligeramente comprimido lateralmente, robusto y de gran tamaño. Tiene una cabeza grande, ojos prominentes y una boca terminal con dientes pequeños. Posee una única aleta dorsal larga con radios espinosos y blandos, y una aleta caudal ligeramente ahorquillada.

Coloración: Generalmente de fondo marrón o verdoso con tonos más claros en el vientre. En los flancos puede presentar bandas o manchas transversales oscuras, más evidentes en juveniles.

Tamaño: Puede alcanzar hasta 1 metro de longitud total y superar los 8 kg. Las tallas comerciales comunes oscilan entre 40 y 80 cm.

Distribución y hábitat: Océano Atlántico sudoccidental, desde el sur de Brasil hasta el Golfo San Jorge y la costa patagónica argentina. Prefiere fondos arenosos o fangosos entre los 10 y 100 metros de profundidad.

Alimentación: Carnívoro. Se alimenta de peces pequeños, crustáceos bentónicos (cangrejos, camarones) y moluscos.

Importancia comercial: Muy apreciado por su carne blanca, firme y sabrosa. Se comercializa fresco o congelado. Es objetivo de la pesca artesanal y deportiva.""",
    },
    {
        "nombre_comun":      "Escrófalo",
        "nombre_cientifico": "Sebastes oculatus",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/escrofalo.webp",
        "descripcion": """Clase: Actinopterygii — Orden: Scorpaeniformes — Familia: Sebastidae.

Pez marino bentónico de cuerpo comprimido lateralmente, cabeza robusta y espinosa, con una gran boca orientada hacia el frente. Presenta espinas óseas bien desarrolladas en la cabeza y radios espinosos en las aletas dorsal y pectorales. Posee glándulas venenosas asociadas a las espinas, cuya picadura puede causar dolor.

Coloración: Color base rojo a rojizo-anaranjado, con manchas oscuras o irregulares a lo largo del cuerpo. Los ojos son grandes y de color oscuro.

Tamaño: Alcanza longitudes de hasta 35-40 cm; más común entre 20 y 30 cm.

Distribución y hábitat: Atlántico sudoccidental, desde el sur de Brasil hasta Tierra del Fuego, siendo frecuente en el Golfo San Jorge. Vive en fondos rocosos o mixtos, a profundidades de 20 a 200 metros. Especie demersal, sedentaria y de hábitos solitarios.

Alimentación: Carnívoro. Se alimenta de crustáceos, moluscos y pequeños peces bentónicos. Depredador oportunista al acecho.

Reproducción: Es vivíparo. La fecundación es interna y las crías se desarrollan en el interior de la madre.

Importancia comercial: Valor pesquero regional como especie acompañante en la pesca de arrastre. También apreciado en la pesca recreativa.""",
    },
    {
        "nombre_comun":      "Pez Sapo",
        "nombre_cientifico": "Notothenia angustata",
        "categoria":         "Peces",
        "imagen_url":        "/imagenes/Especies/pezsapo.webp",
        "descripcion": """Clase: Actinopterygii — Orden: Perciformes — Familia: Nototheniidae.

Pez bentónico de cuerpo robusto y cabeza ancha, con características morfológicas propias de las especies nototeníidas adaptadas a aguas frías. Es típico de fondos costeros y sublitorales del Atlántico sudoccidental.

Distribución y hábitat: Se encuentra en aguas frías del Atlántico suroccidental, principalmente en costas patagónicas. Vive en fondos rocosos y mixtos, a profundidades variables.

Alimentación: Carnívoro bentónico. Se alimenta de invertebrados y pequeños peces del fondo marino.

Importancia: Capturado ocasionalmente por la pesca artesanal y como bycatch en pesquerías dirigidas a otras especies.""",
    },
    {
        "nombre_comun":      "Pulpo Colorado",
        "nombre_cientifico": "Enteroctopus megalocyathus",
        "categoria":         "Invertebrados",
        "imagen_url":        "/imagenes/Especies/pulporojo.webp",
        "descripcion": """Clase: Cephalopoda — Orden: Octopoda — Familia: Octopodidae.

El pulpo colorado es un cefalópodo bentónico de cuerpo robusto, brazos largos con dos filas de ventosas y una coloración que varía entre rojizo y pardo. Es una de las especies de pulpos de mayor tamaño en el sur de Sudamérica.

Coloración: Tono rojizo a pardo, con la capacidad de cambiar ligeramente su color y textura para camuflarse con el entorno.

Tamaño: Puede alcanzar hasta 4 kg de peso y más de 1 metro de envergadura (de brazo a brazo).

Distribución y hábitat: Habita en las aguas frías del Pacífico suroriental (sur de Chile) y del Atlántico sudoccidental (sur de Argentina, principalmente en el Golfo San Jorge). Se encuentra en fondos rocosos, grietas y cuevas, desde la zona intermareal hasta unos 100 metros de profundidad.

Alimentación: Carnívoro oportunista. Se alimenta de crustáceos, peces pequeños y moluscos, a los que caza con sus brazos y picos córneos.

Reproducción: Especie semélpara: se reproduce una sola vez en su vida. La hembra deposita los huevos en grietas y cuevas, y los cuida activamente hasta que eclosionan. Durante este período deja de alimentarse y muere poco después de la eclosión.

Importancia comercial: Tiene valor pesquero local. Su carne es apreciada en gastronomía por su sabor y textura.""",
    },
]


def main():
    conn = psycopg2.connect(**config.DB_CONFIG)
    cur  = conn.cursor()
    try:
        for e in ESPECIES:
            cur.execute(
                """
                INSERT INTO oogsj_data.especie
                    (nombre_comun, nombre_cientifico, descripcion, categoria, imagen_url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (
                    e["nombre_comun"],
                    e.get("nombre_cientifico"),
                    e.get("descripcion"),
                    e.get("categoria"),
                    e.get("imagen_url"),
                ),
            )
        conn.commit()
        print(f"OK: {len(ESPECIES)} especies insertadas (o ya existentes).")
    except Exception as ex:
        conn.rollback()
        print(f"ERROR: {ex}", file=sys.stderr)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
