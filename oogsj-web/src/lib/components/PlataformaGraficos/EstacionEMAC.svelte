<script>
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionEMACVisualizacionDatos from '../datos/EstacionEMACVisualizacionDatos.svelte';

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
</script>

<PanelVariablesEstaciones
  endpoint="/api/emac_cmd0"
  titulo="Estación EMAC - Caleta Córdova"
  iconosVariables={iconosEMAC}
  variablesVisibles={variablesEMAC}
/>

<EstacionEMACVisualizacionDatos />
