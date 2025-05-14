<script>
    import PanelVariables from '../PlataformaGraficos/PanelVariables.svelte';
    import { onMount, onDestroy } from 'svelte';
    import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
    import BoyaVisualizacionDatos from '../datos/BoyaVisualizacionDatos.svelte'; // para futuro
  
    const Estacion = {
      nombre: "APPCR Muelle CC",
      lat: -45.836,
      lon: -67.64667,
      info: "Estación meteorológica ubicada en el Muelle de Comodoro Rivadavia.",
    };
  </script>
  
  <PanelVariablesEstaciones
    endpoint="/api/weatherstation/muelle"
    titulo={Estacion.nombre}
    iconosVariables={{
      "Sensor Virtual - abs_press - 191512": "🌡️",
      "Sensor Virtual - bar - 191512": "📏",
      "Sensor Virtual - bar_alt - 191512": "📏",
      "Sensor Virtual - bar_noaa - 191512": "📏",
      "Sensor Virtual - deg_days_cool - 191512": "❄️",
      "Sensor Virtual - deg_days_heat - 191512": "🔥",
      "Sensor Virtual - dew_point_out - 191512": "💧🌤️",
      "Sensor Virtual - et - 191512": "🌫️",
      "Sensor Virtual - heat_index_out - 191512": "🌡️🌤️",
      "Sensor Virtual - hum_out - 191512": "💦🌤️",
      "Sensor Virtual - night_cloud_cover - 191512": "☁️🌙",
      "Sensor Virtual - rain_rate_hi_clicks - 191512": "🌧️📈",
      "Sensor Virtual - rain_rate_hi_in - 191512": "🌧️📈",
      "Sensor Virtual - rain_rate_hi_mm - 191512": "🌧️📈",
      "Sensor Virtual - rainfall_clicks - 191512": "🌧️",
      "Sensor Virtual - rainfall_in - 191512": "🌧️",
      "Sensor Virtual - rainfall_mm - 191512": "🌧️",
      "Sensor Virtual - solar_energy - 191512": "🔆⚡",
      "Sensor Virtual - solar_rad_avg - 191512": "🔆📊",
      "Sensor Virtual - solar_rad_hi - 191512": "🔆📈",
      "Sensor Virtual - temp_in - 191512": "🌡️🏠",
      "Sensor Virtual - temp_out - 191512": "🌡️🌤️",
      "Sensor Virtual - temp_out_hi - 191512": "🌞📈",
      "Sensor Virtual - temp_out_lo - 191512": "❄️📉",
      "Sensor Virtual - thsw_index - 191512": "🌡️🌬️☀️",
      "Sensor Virtual - thw_index - 191512": "🌪️",
      "Sensor Virtual - uv_dose - 191512": "🌞💥",
      "Sensor Virtual - uv_index_avg - 191512": "🌞📊",
      "Sensor Virtual - uv_index_hi - 191512": "🌞📈",
      "Sensor Virtual - wet_bulb - 191512": "💧🌡️",
      "Sensor Virtual - wind_chill - 191512": "💨❄️",
      "Sensor Virtual - wind_dir_of_hi - 191512": "🧭📈",
      "Sensor Virtual - wind_dir_of_prevail - 191512": "🧭📉",
      "Sensor Virtual - wind_num_samples - 191512": "📊",
      "Sensor Virtual - wind_run - 191512": "🏃💨",
      "Sensor Virtual - wind_speed_avg - 191512": "💨📊",
      "Sensor Virtual - wind_speed_hi - 191512": "💨📈"
    }}
  />
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
  