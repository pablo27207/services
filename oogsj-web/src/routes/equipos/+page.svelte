<script>
  import Carrusel from "$lib/components/Carrusel.svelte";
  import MapaEquipos from "$lib/components/Mapas/MapaEquipos.svelte";
  import Plataforma from "$lib/components/Plataforma.svelte";
</script>

<br>

<style>
  h1, h2 {
      color: #ff8c00;
      font-family: 'Arial', sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      transition: transform 0.3s ease, color 0.3s ease;
      transform-origin: center;
  }

  /* Efecto hover */
  h1:hover, h2:hover {
      color: #ffa500;
      transform: scale(1.05);
  }

  /* Contenedor principal en dos columnas */
  .equiposVisual {
      display: flex;
      gap: 20px; /* Espaciado entre las columnas */
      padding: 20px;
      
      
  }

  /* Contenedor del mapa */
  .map {
      flex: 1; /* Ocupar el 50% del espacio disponible */
      min-width: 50%;
      z-index: 0;
  }

  /* Contenedor de la información de la plataforma */
  .plataforma {
      flex: 1;
      min-width: 50%;
      background: rgb(56, 66, 81);
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(183, 152, 152, 0.344);
      
      
  }

  /* Responsive: cuando la pantalla sea pequeña, se apila en columna */
  @media (max-width: 768px) {
      .equiposVisual {
          flex-direction: column;
      }

      .map, .plataforma {
          width: 100%;
          min-width: unset;
          
      }
  }
</style>


<br>

<!-- Sección de título y descripción -->
<div class="text-center mt-8">
  <h2 class="text-4xl font-bold">Plataformas y Ubicaciones</h2>
 <!-- <p class="mt-4 text-lg text-white-900">
      En esta sección se presentarán las distintas plataformas de monitoreo que se están implementando en el Golfo San Jorge, junto con sus ubicaciones específicas. Estas plataformas son parte integral del Observatorio Oceanográfico del Golfo San Jorge, un proyecto destinado a mejorar la gestión sostenible de los recursos marinos y a proporcionar datos críticos para la investigación científica.
  </p> -->
</div>
<br>

<!-- Contenedor con el mapa a la izquierda y la plataforma a la derecha -->
<div class="equiposVisual">
  <div class="map">
      <MapaEquipos />
  </div>
  <div class="plataforma">
      <Plataforma />
  </div>
</div>
