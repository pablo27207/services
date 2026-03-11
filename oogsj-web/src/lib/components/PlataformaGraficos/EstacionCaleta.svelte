<script>
  import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  import EstacionMuelleVisualizacionDatos from '../datos/EstacionMuelleVisualizacionDatos.svelte';

  const Estacion = {
    nombre: "APPCR Muelle CC",
    lat: -45.836,
    lon: -67.64667,
    info: "Estación meteorológica ubicada en el Muelle de Comodoro Rivadavia."
  };
  
  //  indoor_temperature: null,heat_index_outdoor: null, wind_chill: null,

  const iconosMuelle = {
    barometric_pressure: "/iconosPaginaDatos/PresionBarometrica.png",

    
  
    outdoor_temperature: "/iconosPaginaDatos/TemperaturaExterior.png",
    rainfall: "/iconosPaginaDatos/Precipitacion.png",
   
    wind_direction: "/iconosPaginaDatos/DireccionDelViento.png",
    wind_speed_avg: "/iconosPaginaDatos/VelocidadDeViento2.png"
  };

  //    "dew_point_outdoor",  "indoor_temperature","wind_chill",    "heat_index_outdoor",
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
  titulo={Estacion.nombre}
  iconosVariables={iconosMuelle}
  variablesVisibles={variablesMuelle}
/>

<EstacionMuelleVisualizacionDatos />

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