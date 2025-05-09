<script>
    import PanelVariables from '../PlataformaGraficos/PanelVariables.svelte';
    import { onMount, onDestroy } from 'svelte';
    import BoyaVisualizacionDatos from '../datos/BoyaVisualizacionDatos.svelte'; // ⚠️ no se usa aún
    import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
  
    const Estacion = {
      nombre: "APPCR Puerto CR",
      lat: -45.86222,
      lon: -67.46334,
      info: "Estación meteorológica ubicada en el Puerto de Comodoro Rivadavia.",
    };
  </script>
  
  <!--Cambiar el endpoit por el de produccion -->
  <PanelVariablesEstaciones
    endpoint="/api/weatherstation/puerto"
    titulo={Estacion.nombre}
    iconosVariables={{
      "Sensor Virtual - abs_press - 160710": "🌡️",
      "Sensor Virtual - bar - 160710": "📏",
      "Sensor Virtual - bar_alt - 160710": "📏",
      "Sensor Virtual - bar_noaa - 160710": "📏",
      "Sensor Virtual - deg_days_cool - 160710": "❄️",
      "Sensor Virtual - deg_days_heat - 160710": "🔥",
      "Sensor Virtual - dew_point_in - 160710": "💧🏠",
      "Sensor Virtual - dew_point_out - 160710": "💧🌤️",
      "Sensor Virtual - emc - 160710": "🌾",
      "Sensor Virtual - et - 160710": "🌫️",
      "Sensor Virtual - heat_index_in - 160710": "🌡️🏠",
      "Sensor Virtual - heat_index_out - 160710": "🌡️🌤️",
      "Sensor Virtual - hum_in - 160710": "💦🏠",
      "Sensor Virtual - hum_out - 160710": "💦🌤️",
      "Sensor Virtual - rain_rate_hi_clicks - 160710": "🌧️📈",
      "Sensor Virtual - rain_rate_hi_in - 160710": "🌧️📈",
      "Sensor Virtual - rain_rate_hi_mm - 160710": "🌧️📈",
      "Sensor Virtual - rainfall_clicks - 160710": "🌧️",
      "Sensor Virtual - rainfall_in - 160710": "🌧️",
      "Sensor Virtual - rainfall_mm - 160710": "🌧️",
      "Sensor Virtual - temp_extra_1 - 160710": "🌡️🌍",
      "Sensor Virtual - temp_in - 160710": "🌡️🏠",
      "Sensor Virtual - temp_out - 160710": "🌡️🌤️",
      "Sensor Virtual - temp_out_hi - 160710": "🌞📈",
      "Sensor Virtual - temp_out_lo - 160710": "❄️📉",
      "Sensor Virtual - thw_index - 160710": "🌪️",
      "Sensor Virtual - wet_bulb - 160710": "💧🌡️",
      "Sensor Virtual - wind_chill - 160710": "💨❄️",
      "Sensor Virtual - wind_dir_of_hi - 160710": "🧭📈",
      "Sensor Virtual - wind_dir_of_prevail - 160710": "🧭📉",
      "Sensor Virtual - wind_num_samples - 160710": "📊",
      "Sensor Virtual - wind_run - 160710": "🏃💨",
      "Sensor Virtual - wind_speed - 160710": "💨",
      "Sensor Virtual - wind_speed_avg - 160710": "💨📊",
      "Sensor Virtual - wind_speed_hi - 160710": "💨📈"
    }}
  />
  
  <!-- Componente de gráficos para el futuro -->
  <!--<BoyaVisualizacionDatos />-->
  
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
  