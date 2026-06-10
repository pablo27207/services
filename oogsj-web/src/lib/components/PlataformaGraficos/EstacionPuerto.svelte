<script>
  import { onMount } from 'svelte';
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionPuertoVisualizacionDatos from '../datos/EstacionPuertoVisualizacionDatos.svelte';
  import MantenimientoBanner from './MantenimientoBanner.svelte';

  const PLATFORM_ID = 4;

  const estacion = {
    nombre: "Puerto Comodoro Rivadavia",
    lat: -45.86222,
    lon: -67.46334,
    info: "Estación meteorológica ubicada en el Puerto de Comodoro Rivadavia."
  };

  const iconosPuerto = {
    barometric_pressure: "/iconosPaginaDatos/PresionBarometrica.png",
    outdoor_humidity: "/iconosPaginaDatos/HumedadExterior.png",
    outdoor_temperature: "/iconosPaginaDatos/TemperaturaExterior.png",
    wind_speed: "/iconosPaginaDatos/VelocidadDeViento2.png"
  };

  const variablesPuerto = [
    "barometric_pressure",
    "outdoor_humidity",
    "outdoor_temperature",
    "wind_speed"
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
    endpoint="/api/appcr/puerto"
    titulo={estacion.nombre}
    iconosVariables={iconosPuerto}
    variablesVisibles={variablesPuerto}
  />
  <EstacionPuertoVisualizacionDatos />
{/if}
