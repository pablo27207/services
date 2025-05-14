<script>
  import BoyaVistaDatos1 from '../datos/MareografoVisualizacionDatos.svelte';
  import PanelVariables from '../PlataformaGraficos/PanelVariables.svelte';

  const mareografo = {
    nombre: "Mareógrafo Puerto de Comodoro Rivadavia",
    lat: -45.8613,
    lon: -67.4647,
    info: "Mareógrafo en Comodoro Rivadavia para monitoreo del nivel del mar.",
    imagen: "/imagenes/mareografo.jpg"
  };
</script>

<PanelVariables
  endpoint="/api/mareograph/latest"
  titulo={mareografo.nombre}
  iconosVariables={{
    "Valeport TideMaster": "🌊"
  }}
/>

<div class="chart-container">
  <div><BoyaVistaDatos1 /></div>
</div>


<style>
  .mareografo-info {
    background-color: #f9f9f9;
    padding: 1.5rem;
    border-radius: 1rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .nombre {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.2rem;
  }

  .fecha,
  .estado {
    font-size: 0.95rem;
    color: #666;
    margin: 0.3rem 0 0.8rem 0;
  }

  .valor-principal {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.25rem;
    font-weight: 600;
    gap: 0.5rem;
    color: #333;
  }

  .icon {
    font-size: 1.6rem;
    
  }

  .valor {
    font-size: 1.4rem;
  }

  .chart-container {
    margin-top: 20px;
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

  .tooltip-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.tooltip {
  position: absolute;
  bottom: 125%; /* ajusta la distancia sobre el ícono */
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.75);
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease-in-out;
  z-index: 1;
}

.tooltip-wrapper:hover .tooltip {
  opacity: 1;
}
</style>
