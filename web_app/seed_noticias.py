"""
Seed script: inserta las noticias históricas del catálogo estático en oogsj_data.noticia.
Ejecutar UNA sola vez desde el contenedor web_app:

    docker-compose exec web_app python seed_noticias.py
"""

import sys
import psycopg2
import config

NOTICIAS = [
    {
        "titulo": "Un buque científico búlgaro visitó el puerto de Comodoro en su viaje a la Antártida",
        "contenido": (
            "Una embarcación búlgara llegó a Comodoro rumbo a la Antártida para una misión científica. "
            "Fue recibida por autoridades locales y de Bulgaria, quienes destacaron la importancia de la "
            "cooperación, la cultura búlgara en la ciudad y el valor del mar y la Antártida como espacios "
            "de paz e investigación.\n\n"
            "Fuente: Agencia Comodoro Conocimiento\n"
            "Más información: https://conocimiento.gob.ar/index.php/noticias/"
            "un-buque-cientifico-bulgaro-visito-el-puerto-de-comodoro-en-su-viaje-a-la-antartida-2"
        ),
        "categoria": "Institucional",
        "imagen_url": None,
        "publicado": True,
        "created_at": "2025-02-16",
    },
    {
        "titulo": "Comodoro Conocimiento impulsa la certificación profesional en los puertos",
        "contenido": (
            "Agencia Comodoro Conocimiento, CGT y SUPA impulsan capacitaciones portuarias con "
            "certificación, ampliadas a Madryn, Rawson y Camarones, para fortalecer empleo y "
            "competitividad regional.\n\n"
            "Fuente: Agencia Comodoro Conocimiento\n"
            "Más información: https://conocimiento.gob.ar/index.php/noticias/"
            "comodoro-conocimiento-impulsa-la-certificacion-profesional-en-los-puertos"
        ),
        "categoria": "Institucional",
        "imagen_url": None,
        "publicado": True,
        "created_at": "2025-01-26",
    },
    {
        "titulo": "Fue instalada la boya oceanográfica en las aguas del Golfo San Jorge",
        "contenido": (
            "Se puso en funcionamiento la boya oceanográfica Comodoro II, ubicada a 4 km de la costa "
            "en el Golfo San Jorge. El operativo de traslado e instalación fue realizado por el Municipio, "
            "Comodoro Conocimiento, el Puerto local, la Universidad y el CONICET. Esta boya transmitirá "
            "datos por al menos cinco meses y marca un hito en el desarrollo del Observatorio Oceanográfico. "
            "Permitirá obtener información clave para la navegación, obras costeras y políticas de "
            "sustentabilidad relacionadas con pesca y energía mareomotriz. El operativo incluyó buzos, "
            "embarcaciones de apoyo y un anclaje de 11 toneladas.\n\n"
            "Fuente: Agencia Comodoro Conocimiento\n"
            "Más información: https://conocimiento.gob.ar/index.php/noticias/"
            "fue-instalada-la-boya-oceanografica-en-las-aguas-del-golfo-san-jorge"
        ),
        "categoria": "Monitoreo",
        "imagen_url": None,
        "publicado": True,
        "created_at": "2025-01-21",
    },
    {
        "titulo": "Comodoro Conocimiento realizó una prueba de funcionamiento de la boya oceanográfica en el Puerto local",
        "contenido": (
            "En el marco del Programa CID MAR AUSTRAL, se realizó con éxito la botadura de una boya "
            "oceanográfica recuperada tras 10 años. La maniobra, liderada por el Observatorio Oceanográfico "
            "del Golfo San Jorge junto a Comodoro Conocimiento, CONICET y la UNPSJB, marca un paso clave "
            "para el monitoreo marino. Actualmente se encuentra en pruebas en el Puerto de Comodoro, "
            "equipada con sensores nacionales para medir corrientes, olas, temperatura, viento y radiación. "
            "Luego será instalada en su ubicación definitiva. Este avance fortalecerá la investigación "
            "oceanográfica y el monitoreo ambiental en el Atlántico Sur.\n\n"
            "Fuente: Agencia Comodoro Conocimiento\n"
            "Más información: https://conocimiento.gob.ar/index.php/noticias/"
            "comodoro-conocimiento-realizo-una-prueba-de-funcionamiento-de-la-boya-oceanografica-en-el-puerto-local"
        ),
        "categoria": "Monitoreo",
        "imagen_url": None,
        "publicado": True,
        "created_at": "2025-01-06",
    },
    {
        "titulo": "Comodoro Conocimiento, CONICET y la Administración Portuaria ponen en marcha el Observatorio Oceanográfico del Golfo San Jorge",
        "contenido": (
            "Se realizó el segundo encuentro de becarios e investigadores del CONICET del Golfo San Jorge, "
            "con la participación de autoridades académicas y públicas. Se firmaron dos convenios clave: "
            "uno entre Comodoro Conocimiento y el IIDEPyS-CONICET para avanzar en el Observatorio "
            "Oceanográfico del Golfo San Jorge, y otro con la Administración Portuaria para coordinar "
            "la logística y mantenimiento de la boya oceanográfica. Se destacó la importancia del "
            "monitoreo marino para el desarrollo sostenible. Además, se anunció el 1° Foro del Mar "
            "en noviembre, como espacio de debate sobre el uso estratégico del mar.\n\n"
            "Fuente: Agencia Comodoro Conocimiento\n"
            "Más información: https://conocimiento.gob.ar/index.php/noticias/"
            "comodoro-conocimiento-conicet-y-la-administracion-portuaria-ponen-en-marcha-el-observatorio-oceanografico-del-golfo-san-jorge"
        ),
        "categoria": "Institucional",
        "imagen_url": None,
        "publicado": True,
        "created_at": "2024-10-24",
    },
    {
        "titulo": "Un buque científico búlgaro visitó el puerto de Comodoro en su viaje a la Antártida (2024)",
        "contenido": (
            "Una embarcación científica búlgara en misión hacia la Antártida fue recibida en Comodoro "
            "Rivadavia por autoridades locales. La visita destacó los lazos entre Bulgaria y Argentina, "
            "el valor de la colectividad búlgara en la ciudad y la importancia del mar y la Antártida "
            "como espacios de paz e investigación. Autoridades resaltaron la preservación cultural y "
            "el compromiso con el desarrollo sustentable del océano.\n\n"
            "Fuente: Agencia Comodoro Conocimiento\n"
            "Más información: https://conocimiento.gob.ar/index.php/noticias/"
            "un-buque-cientifico-bulgaro-visito-el-puerto-de-comodoro-en-su-viaje-a-la-antartida"
        ),
        "categoria": "Institucional",
        "imagen_url": None,
        "publicado": True,
        "created_at": "2024-02-17",
    },
]


def main():
    conn = psycopg2.connect(**config.DB_CONFIG)
    cur  = conn.cursor()
    try:
        for n in NOTICIAS:
            cur.execute(
                """
                INSERT INTO oogsj_data.noticia
                    (titulo, contenido, categoria, imagen_url, publicado, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s::date, %s::date)
                ON CONFLICT DO NOTHING;
                """,
                (
                    n["titulo"],
                    n["contenido"],
                    n.get("categoria"),
                    n.get("imagen_url"),
                    n["publicado"],
                    n["created_at"],
                    n["created_at"],
                ),
            )
        conn.commit()
        print(f"OK: {len(NOTICIAS)} noticias insertadas (o ya existentes).")
    except Exception as ex:
        conn.rollback()
        print(f"ERROR: {ex}", file=sys.stderr)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
