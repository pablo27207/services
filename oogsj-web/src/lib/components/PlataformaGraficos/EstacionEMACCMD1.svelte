<script>
  import { onMount } from 'svelte';
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionEMACCMD1VisualizacionDatos from '../datos/EstacionEMACCMD1VisualizacionDatos.svelte';
  import MantenimientoBanner from './MantenimientoBanner.svelte';

  const iconosEMAC = {
    water_level:       "/iconosPaginaDatos/PresionBarometrica.png",
    water_temperature: "/iconosPaginaDatos/TemperaturaExterior.png",
    conductivity:      "/iconosPaginaDatos/HumedadExterior.png",
    air_temperature:   "/iconosPaginaDatos/TemperaturaExterior.png",
    wind_speed:        "/iconosPaginaDatos/VelocidadDeViento2.png",
    wind_direction:    "/iconosPaginaDatos/DireccionDelViento.png"
  };

  const variablesEMAC = [
    "water_level",
    "water_temperature",
    "conductivity",
    "air_temperature",
    "wind_speed",
    "wind_direction"
  ];

  let enMantenimiento = false;
  let mensajeMantenimiento = '';
  let estadoCargando = true;

  onMount(async () => {
    try {
      const res = await fetch('/api/emac_cmd1/estado');
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
    endpoint="/api/emac_cmd1/"
    titulo="Estación EMAC - Club Náutico"
    iconosVariables={iconosEMAC}
    variablesVisibles={variablesEMAC}
  />
  <EstacionEMACCMD1VisualizacionDatos />
{/if}
