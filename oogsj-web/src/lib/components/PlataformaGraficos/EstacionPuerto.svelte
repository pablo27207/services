<script>
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionPuertoVisualizacionDatos from '../datos/EstacionPuertoVisualizacionDatos.svelte';

  const Estacion = {
    nombre: "APPCR Puerto CR",
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
</script>

<PanelVariablesEstaciones
  endpoint="/api/appcr/puerto"
  titulo={Estacion.nombre}
  iconosVariables={iconosPuerto}
  variablesVisibles={variablesPuerto}
/>

<EstacionPuertoVisualizacionDatos />

<style>
  .cards-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
  }

  .variable-card {
    background: #f4f4f4;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    flex: 1;
    min-width: 120px;
    max-width: 150px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
  }

  .variable-card .icon {
    font-size: 24px;
  }

  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
    padding: 20px;
  }

  .tooltip {
    visibility: hidden;
    background-color: rgba(0, 0, 0, 0.8);
    color: #fffefe;
    text-align: center;
    padding: 3px 6px;
    border-radius: 5px;
    position: absolute;
    bottom: 50%;
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 12px;
  }

  .variable-card:hover .tooltip {
    visibility: visible;
    opacity: 1;
  }
</style>