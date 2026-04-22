<script>
  import ZonaHeader from '../zona/ZonaHeader.svelte';
  import ZonaEstado from '../zona/ZonaEstado.svelte';
  import ZonaActividades from '../zona/ZonaActividades.svelte';
  import ZonaGuardavidas from '../zona/ZonaGuardavidas.svelte';
  import ZonaCondicionesMar from '../zona/ZonaCondicionesMar.svelte';
  import ZonaRecomendaciones from '../zona/ZonaRecomendaciones.svelte';

  export let zonaSeleccionada;
</script>

<section class="bloque detalle-zona">
  <ZonaHeader {zonaSeleccionada} />

  <div class="detalle-contenido">
    <ZonaEstado estado={zonaSeleccionada.estadoZona} />

    <div class="mini-grid">
      <ZonaActividades actividades={zonaSeleccionada.actividades} />
      <ZonaGuardavidas
        guardavidas={zonaSeleccionada.guardavidas}
        horarioGuardavidas={zonaSeleccionada.horarioGuardavidas}
      />
    </div>

    <ZonaRecomendaciones
      titulo="Consideraciones para esta zona"
      items={zonaSeleccionada.consideraciones}
    />
  </div>
</section>

<ZonaCondicionesMar items={zonaSeleccionada.condicionesMar} />

<ZonaRecomendaciones
  titulo="Recomendaciones específicas de esta zona"
  items={zonaSeleccionada.recomendacionesZona}
/>

<style>
  .bloque {
    margin-top: 1.5rem;
  }

  .detalle-zona {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    align-items: stretch;
  }

  .detalle-contenido {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .mini-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.85rem;
  }

  @media (min-width: 900px) {
    .bloque {
      margin-top: 2rem;
    }

    .detalle-zona {
      grid-template-columns: 1.1fr 1fr;
      gap: 1.5rem;
    }

    .detalle-contenido {
      gap: 1rem;
    }

    .mini-grid {
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }
  }
</style>