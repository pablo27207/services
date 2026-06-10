<script>
  import { onMount } from 'svelte';
  import PanelVariables from './PanelVariables.svelte';
  import BoyaVisualizacionDatos from '../datos/BoyaVisualizacionDatos.svelte';
  import MantenimientoBanner from './MantenimientoBanner.svelte';

  const PLATFORM_ID = 3;

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
  <!-- espera silenciosa mientras carga el estado -->
{:else if enMantenimiento}
  <MantenimientoBanner mensaje={mensajeMantenimiento} />
{:else}
  <PanelVariables
    endpoint="/api/buoy/latest"
    titulo={"Comodoro II"}
    ordenVariables={[
      "Sensor de Altura de Olas - CIDMAR-2",
      "Sensor de Dirección de Olas - CIDMAR-2",
      "Sensor de Periodo de Olas - CIDMAR-2",
      "Sensor de Dirección de la Corriente - CIDMAR-2",
      "Sensor de Radiación PAR - CIDMAR-2",
      "Sensor de Batería - CIDMAR-2"
    ]}
    iconosVariables={{
      "Sensor de Altura de Olas - CIDMAR-2": "/iconosPaginaDatos/AlturaDeOlas.jpeg",
      "Sensor de Dirección de Olas - CIDMAR-2": "/iconosPaginaDatos/DireccionDeOlas_v2.png",
      "Sensor de Periodo de Olas - CIDMAR-2": "/iconosPaginaDatos/PeriodoDeOla_v2.png",
      "Sensor de Dirección de la Corriente - CIDMAR-2": "/iconosPaginaDatos/DireccionDeCorriente.png",
      "Sensor de Velocidad de Corriente - CIDMAR-2": "/iconosPaginaDatos/VelocidadDeCorriente.png",
      "Sensor de Radiación PAR - CIDMAR-2": "/iconosPaginaDatos/RadiacionPar.png",
      "Sensor de Batería - CIDMAR-2": "/iconosPaginaDatos/Bateria.png"
    }}
  />

  <BoyaVisualizacionDatos />
{/if}
