<script>
  import { onMount } from 'svelte';
  import MareografoVisualizacionDatos from '../datos/MareografoVisualizacionDatos.svelte';
  import MantenimientoBanner from './MantenimientoBanner.svelte';

  const PLATFORM_ID = 1;

  let enMantenimiento = false;
  let mensajeMantenimiento = '';
  let estadoCargando = true;

  onMount(async () => {
    try {
      const res = await fetch(`/api/plataforma/${PLATFORM_ID}/estado`);
      const data = await res.json();
      enMantenimiento = data.en_mantenimiento ?? false;
      mensajeMantenimiento = data.mensaje ?? '';
    } catch {
      enMantenimiento = false;
    } finally {
      estadoCargando = false;
    }
  });
</script>

{#if estadoCargando}
  <!-- espera silenciosa -->
{:else if enMantenimiento}
  <MantenimientoBanner mensaje={mensajeMantenimiento} />
{:else}
  <div class="chart-container">
    <MareografoVisualizacionDatos />
  </div>
{/if}

<style>
  .chart-container {
    margin-top: 0.5rem;
    width: 100%;
  }
</style>
