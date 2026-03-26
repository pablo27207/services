<script>
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionPuertoVisualizacionDatos from '../datos/EstacionPuertoVisualizacionDatos.svelte';

  // Configuración base de la estación meteorológica del puerto.
  const estacion = {
    nombre: "Puerto Comodoro Rivadavia",
    lat: -45.86222,
    lon: -67.46334,
    info: "Estación meteorológica ubicada en el Puerto de Comodoro Rivadavia."
  };

  // Íconos por variable visible en el panel superior.
  const iconosPuerto = {
    barometric_pressure: "/iconosPaginaDatos/PresionBarometrica.png",
    outdoor_humidity: "/iconosPaginaDatos/HumedadExterior.png",
    outdoor_temperature: "/iconosPaginaDatos/TemperaturaExterior.png",
    wind_speed: "/iconosPaginaDatos/VelocidadDeViento2.png"
  };

  // Orden y selección de variables principales para el resumen superior.
  const variablesPuerto = [
    "barometric_pressure",
    "outdoor_humidity",
    "outdoor_temperature",
    "wind_speed"
  ];
</script>

<PanelVariablesEstaciones
  endpoint="/api/appcr/puerto"
  titulo={estacion.nombre}
  iconosVariables={iconosPuerto}
  variablesVisibles={variablesPuerto}
/>

<EstacionPuertoVisualizacionDatos />