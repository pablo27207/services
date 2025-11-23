#!/usr/bin/env python3
"""
Script para generar presentación del Sistema OOGSJ
para las XII Jornadas Nacionales de Ciencias del Mar
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

def crear_presentacion():
    # Crear presentación en formato 4:3
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Colores institucionales (azul marino para oceanografía)
    COLOR_TITULO = RGBColor(0, 51, 102)  # Azul marino
    COLOR_SUBTITULO = RGBColor(0, 102, 153)  # Azul claro
    COLOR_TEXTO = RGBColor(40, 40, 40)  # Gris oscuro
    COLOR_ACENTO = RGBColor(0, 153, 204)  # Celeste

    # ==================== SLIDE 1: PORTADA ====================
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # Fondo azul suave
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 248, 255)

    # Título principal
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.text = "Sistema de Observación Oceanográfica\nGolfo San Jorge (OOGSJ)"
    title_frame.paragraphs[0].font.size = Pt(36)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = COLOR_TITULO
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Subtítulo
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Monitoreo en Tiempo Real de Variables Oceanográficas y Meteorológicas"
    subtitle_frame.paragraphs[0].font.size = Pt(18)
    subtitle_frame.paragraphs[0].font.color.rgb = COLOR_SUBTITULO
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Evento
    evento_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(9), Inches(0.5))
    evento_frame = evento_box.text_frame
    evento_frame.text = "XII Jornadas Nacionales de Ciencias del Mar"
    evento_frame.paragraphs[0].font.size = Pt(16)
    evento_frame.paragraphs[0].font.italic = True
    evento_frame.paragraphs[0].font.color.rgb = COLOR_TEXTO
    evento_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Autor/Institución (ajustar según corresponda)
    autor_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.2), Inches(9), Inches(0.8))
    autor_frame = autor_box.text_frame
    autor_frame.text = "Observatorio Oceanográfico Golfo San Jorge\n2024"
    autor_frame.paragraphs[0].font.size = Pt(14)
    autor_frame.paragraphs[0].font.color.rgb = COLOR_TEXTO
    autor_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # ==================== SLIDE 2: CONTEXTO ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content

    # Título
    title = slide.shapes.title
    title.text = "Contexto: Golfo San Jorge"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    # Contenido
    content = slide.placeholders[1].text_frame
    content.clear()

    puntos = [
        "Región de alta productividad biológica en el Atlántico Sur",
        "Zona de importancia económica: pesca, turismo, hidrocarburos",
        "Ecosistema sensible a cambios ambientales",
        "Necesidad de datos continuos para investigación y gestión",
        "Escasez histórica de datos oceanográficos in situ"
    ]

    for punto in puntos:
        p = content.add_paragraph()
        p.text = punto
        p.level = 0
        p.font.size = Pt(20)
        p.font.color.rgb = COLOR_TEXTO
        p.space_before = Pt(10)

    # ==================== SLIDE 3: PROBLEMÁTICA ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Problemática"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    puntos = [
        "Datos oceanográficos fragmentados y discontinuos",
        "Falta de acceso centralizado a información en tiempo real",
        "Dificultad para estudios de series temporales largas",
        "Limitaciones en el monitoreo de eventos extremos",
        "Necesidad de integrar múltiples fuentes de datos"
    ]

    for punto in puntos:
        p = content.add_paragraph()
        p.text = punto
        p.level = 0
        p.font.size = Pt(20)
        p.font.color.rgb = COLOR_TEXTO
        p.space_before = Pt(10)

    # ==================== SLIDE 4: OBJETIVOS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Objetivos del Sistema"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    # Objetivo general
    p = content.add_paragraph()
    p.text = "Objetivo General:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO

    p = content.add_paragraph()
    p.text = "Desarrollar una plataforma integrada de monitoreo oceanográfico y meteorológico en tiempo real para el Golfo San Jorge"
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_TEXTO
    p.space_after = Pt(15)

    # Objetivos específicos
    p = content.add_paragraph()
    p.text = "Objetivos Específicos:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO

    objetivos_esp = [
        "Integrar datos de múltiples plataformas de monitoreo",
        "Proporcionar acceso abierto a datos en tiempo real",
        "Facilitar análisis de series temporales para investigación",
        "Generar información para toma de decisiones"
    ]

    for obj in objetivos_esp:
        p = content.add_paragraph()
        p.text = obj
        p.level = 1
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO

    # ==================== SLIDE 5: PLATAFORMAS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Plataformas de Monitoreo Integradas"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    plataformas = [
        ("Mareógrafo - Puerto Comodoro Rivadavia",
         "• Sensor: Valeport TideMaster\n• Variable: Nivel del mar\n• Frecuencia: 10 minutos"),

        ("Boya Oceanográfica CIDMAR-2",
         "• Ubicación: 45.877°S, 67.442°W\n• Variables: Olas, corrientes, radiación PAR\n• Frecuencia: Horaria"),

        ("Estaciones Meteorológicas (WeatherLink)",
         "• Puerto CR y Caleta Córdova\n• Variables: T, P, viento, precipitación, UV\n• Frecuencia: 10 minutos"),

        ("Modelo de Predicción de Mareas",
         "• Servicio Hidrográfico Naval\n• Actualización: Cada 6 horas")
    ]

    for nombre, detalles in plataformas:
        p = content.add_paragraph()
        p.text = nombre
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACENTO

        p = content.add_paragraph()
        p.text = detalles
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(8)

    # ==================== SLIDE 6: VARIABLES OCEANOGRÁFICAS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Variables Oceanográficas Medidas"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    # Crear tabla de variables
    variables_ocean = [
        ("Altura de Olas", "Metros (m)", "Boya CIDMAR-2"),
        ("Periodo de Olas", "Segundos (s)", "Boya CIDMAR-2"),
        ("Dirección de Olas", "Grados (°)", "Boya CIDMAR-2"),
        ("Velocidad de Corriente", "m/s", "Boya CIDMAR-2"),
        ("Dirección de Corriente", "Grados (°)", "Boya CIDMAR-2"),
        ("Radiación PAR", "µmol/m²/s", "Boya CIDMAR-2"),
        ("Nivel del Mar", "Metros (m)", "Mareógrafo")
    ]

    for var, unidad, fuente in variables_ocean:
        p = content.add_paragraph()
        p.text = f"{var} ({unidad})"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACENTO

        p = content.add_paragraph()
        p.text = f"  Fuente: {fuente}"
        p.level = 1
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(5)

    # ==================== SLIDE 7: VARIABLES METEOROLÓGICAS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Variables Meteorológicas Medidas"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    # Dividir en dos columnas
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5.5))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True

    right_box = slide.shapes.add_textbox(Inches(5), Inches(1.5), Inches(4.5), Inches(5.5))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True

    # Columna izquierda
    vars_left = [
        "Temperatura del aire",
        "Humedad relativa",
        "Presión barométrica",
        "Velocidad del viento",
        "Dirección del viento",
        "Precipitación acumulada",
        "Tasa de precipitación"
    ]

    for var in vars_left:
        p = left_frame.add_paragraph()
        p.text = f"• {var}"
        p.font.size = Pt(16)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(8)

    # Columna derecha
    vars_right = [
        "Punto de rocío",
        "Índice de calor",
        "Sensación térmica",
        "Radiación solar",
        "Índice UV",
        "Evapotranspiración",
        "Cobertura nubosa"
    ]

    for var in vars_right:
        p = right_frame.add_paragraph()
        p.text = f"• {var}"
        p.font.size = Pt(16)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(8)

    # ==================== SLIDE 8: ARQUITECTURA ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Arquitectura del Sistema"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    # Descripción simple del flujo
    p = content.add_paragraph()
    p.text = "Flujo de Datos:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO
    p.space_after = Pt(10)

    flujo = [
        "1. Adquisición: APIs externas y sensores remotos",
        "2. Procesamiento: Validación y control de calidad (QC)",
        "3. Almacenamiento: Base de datos PostgreSQL con estándares COI",
        "4. Visualización: Interfaz web con gráficos interactivos",
        "5. Acceso: API REST para consultas y exportación de datos"
    ]

    for paso in flujo:
        p = content.add_paragraph()
        p.text = paso
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(12)

    p = content.add_paragraph()
    p.text = "\n✓ Actualización automática programada\n✓ Sistema operativo 24/7\n✓ Datos abiertos y accesibles"
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_ACENTO

    # ==================== SLIDE 9: CONTROL DE CALIDAD ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Control de Calidad de Datos"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    p = content.add_paragraph()
    p.text = "Sistema de Quality Flags (según COI/UNESCO):"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO
    p.space_after = Pt(10)

    flags = [
        ("Flag 1", "Dato verificado como bueno"),
        ("Flag 2", "Dato probablemente bueno"),
        ("Flag 3", "Dato sospechoso (requiere revisión)"),
        ("Flag 4", "Dato erróneo (descartado)")
    ]

    for flag, desc in flags:
        p = content.add_paragraph()
        p.text = f"{flag}: {desc}"
        p.level = 1
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(8)

    p = content.add_paragraph()
    p.text = "\nNiveles de Procesamiento:"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO
    p.space_after = Pt(10)

    niveles = ["Raw (crudo)", "QC-1 (control básico)", "QC-2 (control avanzado)",
               "Interpolated", "Derived (calculado)"]

    for nivel in niveles:
        p = content.add_paragraph()
        p.text = nivel
        p.level = 1
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO

    # ==================== SLIDE 10: VISUALIZACIÓN ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Interfaz de Visualización"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    p = content.add_paragraph()
    p.text = "Características de la Interfaz Web:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO
    p.space_after = Pt(10)

    caracteristicas = [
        "Gráficos interactivos de series temporales (D3.js)",
        "Mapas georreferenciados con ubicación de plataformas (Leaflet)",
        "Visualización de datos en tiempo real",
        "Selección de rangos temporales personalizados",
        "Exportación de datos (CSV, PDF)",
        "Acceso desde cualquier dispositivo (responsive design)",
        "Panel de estado de sensores y calidad de datos"
    ]

    for caract in caracteristicas:
        p = content.add_paragraph()
        p.text = caract
        p.level = 1
        p.font.size = Pt(17)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(6)

    # ==================== SLIDE 11: APLICACIONES ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Aplicaciones Científicas y Prácticas"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    aplicaciones = [
        ("Investigación Oceanográfica",
         "Análisis de variabilidad oceánica, circulación costera, interacción océano-atmósfera"),

        ("Biología Marina",
         "Correlación con distribución de especies, productividad primaria, eventos reproductivos"),

        ("Gestión Pesquera",
         "Monitoreo de condiciones ambientales en zonas de pesca, predicción de eventos extremos"),

        ("Seguridad Marítima",
         "Información en tiempo real para navegación, prevención de accidentes, planificación de operaciones"),

        ("Cambio Climático",
         "Series temporales largas para estudios de tendencias y variabilidad"),

        ("Educación y Divulgación",
         "Recurso educativo para instituciones académicas y público general")
    ]

    for titulo, desc in aplicaciones:
        p = content.add_paragraph()
        p.text = titulo
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACENTO

        p = content.add_paragraph()
        p.text = desc
        p.level = 1
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(6)

    # ==================== SLIDE 12: ESTADO ACTUAL ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Estado Actual del Sistema"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    p = content.add_paragraph()
    p.text = "Sistema Operativo:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO
    p.space_after = Pt(10)

    estado = [
        "✓ Sistema en operación continua 24/7",
        "✓ 5 plataformas de monitoreo integradas",
        "✓ 54 variables diferentes registradas",
        "✓ Base de datos con series temporales desde 2023",
        "✓ Interfaz web accesible públicamente",
        "✓ Actualizaciones automáticas programadas"
    ]

    for item in estado:
        p = content.add_paragraph()
        p.text = item
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(10)

    p = content.add_paragraph()
    p.text = "\nDatos disponibles para la comunidad científica"
    p.font.size = Pt(20)
    p.font.italic = True
    p.font.color.rgb = COLOR_ACENTO
    p.alignment = PP_ALIGN.CENTER

    # ==================== SLIDE 13: TRABAJO FUTURO ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Trabajo Futuro"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    p = content.add_paragraph()
    p.text = "Expansión y Mejoras Planificadas:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO
    p.space_after = Pt(10)

    futuro = [
        "Incorporación de nuevas plataformas de monitoreo",
        "Integración de datos satelitales (SST, clorofila, vientos)",
        "Desarrollo de modelos predictivos (ML/IA)",
        "Sistema de alertas automáticas para eventos extremos",
        "API pública para acceso programático a datos",
        "Colaboraciones con otras redes de monitoreo",
        "Expansión de cobertura geográfica"
    ]

    for item in futuro:
        p = content.add_paragraph()
        p.text = item
        p.level = 1
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(8)

    # ==================== SLIDE 14: CONCLUSIONES ====================
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    title.text = "Conclusiones"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.color.rgb = COLOR_TITULO

    content = slide.placeholders[1].text_frame
    content.clear()

    conclusiones = [
        "El sistema OOGSJ proporciona una infraestructura robusta para el monitoreo oceanográfico del Golfo San Jorge",

        "La integración de múltiples fuentes de datos permite una visión holística del ambiente marino",

        "Los datos en tiempo real y las series temporales son fundamentales para investigación y gestión",

        "El acceso abierto facilita colaboraciones y fortalece la investigación regional",

        "El sistema es escalable y adaptable a futuras necesidades"
    ]

    for i, concl in enumerate(conclusiones, 1):
        p = content.add_paragraph()
        p.text = f"{i}. {concl}"
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(12)

    # ==================== SLIDE 15: AGRADECIMIENTOS ====================
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # Fondo similar a portada
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 248, 255)

    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = "Agradecimientos"
    title_frame.paragraphs[0].font.size = Pt(36)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = COLOR_TITULO
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Contenido de agradecimientos
    content_box = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(8), Inches(3))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True

    agradecimientos = [
        "• CIDMAR - Centro de Investigación y Desarrollo en Medio Ambiente y Recursos Marinos",
        "• Servicio de Hidrografía Naval Argentina",
        "• Universidad Nacional de la Patagonia San Juan Bosco",
        "• Administración de Puertos del Puerto de Comodoro Rivadavia (APPCR)",
        "• A todos los investigadores y técnicos que contribuyen al monitoreo"
    ]

    for agr in agradecimientos:
        p = content_frame.add_paragraph()
        p.text = agr
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_TEXTO
        p.space_after = Pt(12)

    # Contacto
    contact_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.8))
    contact_frame = contact_box.text_frame
    contact_frame.text = "¿Preguntas?\nContacto: [correo electrónico de contacto]"
    contact_frame.paragraphs[0].font.size = Pt(16)
    contact_frame.paragraphs[0].font.color.rgb = COLOR_ACENTO
    contact_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Guardar presentación
    prs.save('/home/user/services/Presentacion_OOGSJ_XIIJNCM.pptx')
    print("✅ Presentación creada exitosamente: Presentacion_OOGSJ_XIIJNCM.pptx")
    print(f"📊 Total de diapositivas: {len(prs.slides)}")
    print(f"📐 Formato: 4:3 ({prs.slide_width/914400:.1f}\" x {prs.slide_height/914400:.1f}\")")

if __name__ == "__main__":
    crear_presentacion()
