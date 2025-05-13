<script>
  import Carrusel from "$lib/components/Carrusel.svelte";
  import Card1 from "$lib/components/home/Card1.svelte";
  import Card2 from "$lib/components/home/Card2.svelte";
  import Card3 from "$lib/components/home/Card3.svelte";
  import Card4 from "$lib/components/home/Card4.svelte";
  import CardAlterna from "$lib/components/home/CardAlterna.svelte";
</script>

<style>


  h1, h2 {
      color: #ff8c00; /* Color naranja */
      font-family: 'Arial', sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      transition: transform 0.3s ease, color 0.3s ease;
      transform-origin: center;
  }

  .content {
      margin-top: 60px; /* Espacio debajo del navbar fijo */
  }

  h1:hover, h2:hover {
      color: #ffa500;
      transform: scale(1.05);
  }
</style>


<!-- Carrusel -->
<Carrusel />
<br>

<!-- Sección de misión -->
<h2 class="text-3xl font-bold text-center">Objetivos y Metas del Observatorio</h2>
<p class="mt-4 text-lg text-white-900 text-center max-w-4xl mx-auto">
  El Observatorio del Golfo San Jorge se concibe como una infraestructura tecnológica avanzada, diseñada para el monitoreo continuo y escalable del entorno marino, costero y atmosférico. Mediante la integración de diversas plataformas como boyas oceanográficas, estaciones meteorológicas y sensores costeros. Se busca generar información científica precisa y en tiempo real para fortalecer la gestión ambiental, apoyar la toma de decisiones y contribuir al desarrollo sostenible de las comunidades costeras.
</p>


<!-- Tarjetas -->
<div>

  <CardAlterna
  title="Red Inteligente para la Gestión Ambiental" 
  text=" Desplegar una red de plataformas interconectadas que permitan recolectar datos en tiempo real del entorno marino y atmosférico, posibilitando el seguimiento de parámetros clave como calidad del agua, vientos, oleaje y condiciones meteorológicas, para anticipar riesgos y preservar la biodiversidad."
  img="/imagenes/foto-desplegando-boya.png"
/>

<CardAlterna
  title="Análisis de Dinámica Costera"
  text="Estudiar la interacción entre corrientes, erosión y sedimentación a lo largo del Golfo San Jorge mediante herramientas de monitoreo continuo, para comprender los impactos del cambio climático y la actividad humana en el litoral y diseñar estrategias de manejo sostenible."
  img="/imagenes/Imagenes-comodoro-Ivan/imagen 6.jpg"
  reverse={true}
/>

<CardAlterna
  title="Soberanía y Ciencia Aplicada"
  text="Promover el uso del conocimiento científico para la gestión responsable de los recursos naturales del Atlántico Sur, apoyando políticas públicas basadas en evidencia y fomentando el desarrollo tecnológico nacional mediante la cooperación entre instituciones."
  img="/imagenes/focas/focas1.jpg"
/>

<CardAlterna
  title="Impacto Social y Participación"
  text="Involucrar a las comunidades locales a través de programas de ciencia ciudadana y educación ambiental, fortaleciendo su rol en la protección del entorno costero y mejorando la resiliencia de actividades como la pesca y el turismo frente a fenómenos extremos."
  img="/imagenes/Personas/Personas.png"
  reverse={true}
/>
</div>