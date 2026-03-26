<script>
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionMuelleVisualizacionDatos from '../datos/EstacionMuelleVisualizacionDatos.svelte';

  // Configuración base de la estación meteorológica del muelle.
  const estacion = {
    nombre: "Muelle de Comodoro Rivadavia",
    lat: -45.836,
    lon: -67.64667,
    info: "Estación meteorológica ubicada en el muelle de Comodoro Rivadavia."
  };

  // Íconos por variable visible en el panel superior.
  const iconosMuelle = {
    barometric_pressure: "/iconosPaginaDatos/PresionBarometrica.png",
    outdoor_temperature: "/iconosPaginaDatos/TemperaturaExterior.png",
    rainfall: "/iconosPaginaDatos/Precipitacion.png",
    wind_direction: "/iconosPaginaDatos/DireccionDelViento.png",
    wind_speed_avg: "/iconosPaginaDatos/VelocidadDeViento2.png"
  };

  // Variables principales visibles en el resumen superior.
  const variablesMuelle = [
    "barometric_pressure",
    "outdoor_temperature",
    "rainfall",
    "wind_direction",
    "wind_speed_avg"
  ];
</script>

<PanelVariablesEstaciones
  endpoint="/api/appcr/muelle_cc"
  titulo={estacion.nombre}
  iconosVariables={iconosMuelle}
  variablesVisibles={variablesMuelle}
/>

<EstacionMuelleVisualizacionDatos />