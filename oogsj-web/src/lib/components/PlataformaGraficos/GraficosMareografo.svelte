<script>
  import MareografoVisualizacionDatos from '../datos/MareografoVisualizacionDatos.svelte';

  // Este componente queda como wrapper simple del bloque visual del mareógrafo.
  // A diferencia de la boya y las estaciones, acá no mostramos PanelVariables
  // porque el resumen comparativo ya vive dentro de MareografoVisualizacionDatos
  // y repetir un card superior no aporta claridad.
</script>

<!--
  Bloque principal del mareógrafo:
  - resumen superior
  - gráfico comparativo
  - leyenda
-->
<div class="chart-container">
  <MareografoVisualizacionDatos />
</div>

<style>
  .chart-container {
    margin-top: 0.5rem;
    width: 100%;
  }
</style>