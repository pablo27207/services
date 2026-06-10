<script>
  import { onMount } from 'svelte';
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionMuelleVisualizacionDatos from '../datos/EstacionMuelleVisualizacionDatos.svelte';
  import MantenimientoBanner from './MantenimientoBanner.svelte';

  const PLATFORM_ID = 5;

  const estacion = {
    nombre: "Muelle de Comodoro Rivadavia",
    lat: -45.836,
    lon: -67.64667,
    info: "Estación meteorológica ubicada en el muelle de Comodoro Rivadavia."
  };

  const iconosMuelle = {
    barometric_pressure: "/iconosPaginaDatos/PresionBarometrica.png",
    outdoor_temperature: "/iconosPaginaDatos/TemperaturaExterior.png",
    rainfall: "/iconosPaginaDatos/Precipitacion.png",
    wind_direction: "/iconosPaginaDatos/DireccionDelViento.png",
    wind_speed_avg: "/iconosPaginaDatos/VelocidadDeViento2.png"
  };

  const variablesMuelle = [
    "barometric_pressure",
    "outdoor_temperature",
    "rainfall",
    "wind_direction",
    "wind_speed_avg"
  ];

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
  <PanelVariablesEstaciones
    endpoint="/api/appcr/muelle_cc"
    titulo={estacion.nombre}
    iconosVariables={iconosMuelle}
    variablesVisibles={variablesMuelle}
  />
  <EstacionMuelleVisualizacionDatos />
{/if}
