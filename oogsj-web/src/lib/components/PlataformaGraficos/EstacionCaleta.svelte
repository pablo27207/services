<script>
    import PanelVariables from '../PlataformaGraficos/PanelVariables.svelte';
    import { onMount, onDestroy } from 'svelte';
    import PanelVariablesEstaciones from './PanelVariablesEstaciones.svelte';
    import BoyaVisualizacionDatos from '../datos/BoyaVisualizacionDatos.svelte'; // para futuro
    import EstacionMuelleVisualizacionDatos from '../datos/EstacionMuelleVisualizacionDatos.svelte';
  
    const Estacion = {
      nombre: "APPCR Muelle CC",
      lat: -45.836,
      lon: -67.64667,
      info: "Estación meteorológica ubicada en el Muelle de Comodoro Rivadavia.",
    };
  </script>
  
  <PanelVariablesEstaciones
    endpoint="/api/appcr/muelle_cc"
    titulo={Estacion.nombre}
/>
  <!--<BoyaVisualizacionDatos />-->
  <!--Aca agrega los graficos debo agrego los graficos posibles para esto-->
  <EstacionMuelleVisualizacionDatos></EstacionMuelleVisualizacionDatos>
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
  