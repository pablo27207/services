<script>
    import PanelVariables from  '../PlataformaGraficos/PanelVariables.svelte';
    import { onMount, onDestroy } from 'svelte';
    import BoyaVisualizacionDatos from '../datos/BoyaVisualizacionDatos.svelte';
    let charts = {};
    let chartContainers = {};
   
    
    // Datos estáticos simulados para la maqueta de la Boya
    const Boya = {
      nombre: "Comodoro II",
      lat: -45.8613,
      lon: -67.4647,
      info: "Boya en Comodoro Rivadavia para monitoreo del nivel del mar.",
      
    };
  
  
</script>
  
<PanelVariables
endpoint="/api/buoy/latest"
titulo={Boya.nombre}
iconosVariables={{
  "Sensor de Altura de Olas - CIDMAR-2": "🌊",
  "Sensor de Velocidad de Corriente - CIDMAR-2": "🌊",
  "Sensor de Dirección de Corriente - CIDMAR-2": "🧭",
  "Sensor de Dirección de Olas - CIDMAR-2": "🧭",
  "Sensor de Periodo de Olas - CIDMAR-2": "🌊",
  "Sensor de Radiación PAR - CIDMAR-2": "☀️",
  "Sensor de Velocidad del Viento - CIDMAR-2": "💨",
  "Sensor de Batería - CIDMAR-2": "🔋"
}}
/>
<!-- Contenedor para los gráficos en el modal -->

  <BoyaVisualizacionDatos></BoyaVisualizacionDatos>
  
<!-- Estilos -->
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
 

  .variable-card {
  position: relative;
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
