<script>
  import Carrusel from "$lib/components/Carrusel.svelte";
  import Card1 from "$lib/components/home/Card1.svelte";
  import Card2 from "$lib/components/home/Card2.svelte";
  import Card3 from "$lib/components/home/Card3.svelte";
  import Card4 from "$lib/components/home/Card4.svelte";
  import CardAlterna from "$lib/components/home/CardAlterna.svelte";
</script>

<style>
  .mission-section {
    padding: 4rem 1rem 2.5rem;
    text-align: center;
  }

  .mission-tag {
    display: inline-block;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #f97316;
    font-weight: 700;
    margin-bottom: 14px;
    opacity: 0;
    animation: fadeUp 0.7s 0.1s ease forwards;
  }

  .mission-title {
    font-size: clamp(1.5rem, 4vw, 2.4rem);
    font-weight: 800;
    color: #ff8c00;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0 auto 18px;
    max-width: 640px;
    line-height: 1.2;
    opacity: 0;
    animation: fadeUp 0.7s 0.25s ease forwards;
  }

  .mission-divider {
    width: 48px;
    height: 3px;
    background: #f97316;
    border-radius: 2px;
    margin: 0 auto 22px;
    opacity: 0;
    animation: fadeUp 0.7s 0.35s ease forwards;
  }

  .mission-text {
    font-size: clamp(0.9rem, 1.8vw, 1.05rem);
    line-height: 1.75;
    color: rgba(255, 255, 255, 0.82);
    max-width: 780px;
    margin: 0 auto;
    opacity: 0;
    animation: fadeUp 0.7s 0.45s ease forwards;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>


<!-- Carrusel -->
<Carrusel />

<!-- Sección de misión -->
<section class="mission-section">
  <span class="mission-tag">Nuestra misión</span>
  <h2 class="mission-title">Objetivos y Metas del Observatorio</h2>
  <div class="mission-divider"></div>
  <p class="mission-text">
    El Observatorio del Golfo San Jorge se concibe como una infraestructura tecnológica avanzada, diseñada para el monitoreo continuo y escalable del entorno marino, costero y atmosférico. Mediante la integración de diversas plataformas como boyas oceanográficas, estaciones meteorológicas y sensores costeros, se busca generar información científica precisa y en tiempo real para fortalecer la gestión ambiental, apoyar la toma de decisiones y contribuir al desarrollo sostenible de las comunidades costeras.
  </p>
</section>


<!-- Tarjetas -->
<div>

  <CardAlterna
  title="Red Inteligente para la Gestión Ambiental" 
  text=" Desplegar una red de plataformas interconectadas que permitan recolectar datos en tiempo real del entorno marino y atmosférico, posibilitando el seguimiento de parámetros clave como calidad del agua, vientos, oleaje y condiciones meteorológicas, para anticipar riesgos y preservar la biodiversidad."
  img="/imagenes/foto-desplegando-boya.webp"
/>

<CardAlterna
  title="Análisis de Dinámica Costera"
  text="Estudiar la interacción entre corrientes, erosión y sedimentación a lo largo del Golfo San Jorge mediante herramientas de monitoreo continuo, para comprender los impactos del cambio climático y la actividad humana en el litoral y diseñar estrategias de manejo sostenible."
  img="/imagenes/Imagenes-comodoro-Ivan/imagen 6.webp"
  reverse={true}
/>

<CardAlterna
  title="Soberanía y Ciencia Aplicada"
  text="Promover el uso del conocimiento científico para la gestión responsable de los recursos naturales del Atlántico Sur, apoyando políticas públicas basadas en evidencia y fomentando el desarrollo tecnológico nacional mediante la cooperación entre instituciones."
  img="/imagenes/focas/focas1.webp"
/>

<CardAlterna
  title="Impacto Social y Participación"
  text="Involucrar a las comunidades locales a través de programas de ciencia ciudadana y educación ambiental, fortaleciendo su rol en la protección del entorno costero y mejorando la resiliencia de actividades como la pesca y el turismo frente a fenómenos extremos."
  img="/imagenes/Personas/Personas.webp"
  reverse={true}
/>
</div>