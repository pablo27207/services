<script>
  import PanelVariables from '../PlataformaGraficos/PanelVariables.svelte';
  import BoyaVisualizacionDatos from '../datos/BoyaVisualizacionDatos.svelte';

  // Datos estáticos simulados para la maqueta de la Boya
  const Boya = {
    nombre: "Comodoro-II",
    lat: -45.8613,
    lon: -67.4647,
    info: "Boya en Comodoro Rivadavia para monitoreo del nivel del mar.",
  };
</script>

<PanelVariables
  endpoint="/api/buoy/latest"
  titulo={Boya.nombre}
  ordenVariables={[
    "Sensor de Altura de Olas - CIDMAR-2",
    "Sensor de Dirección de Olas - CIDMAR-2",
    "Sensor de Periodo de Olas - CIDMAR-2",
    "Sensor de Dirección de la Corriente - CIDMAR-2",
    "Sensor de Velocidad de Corriente - CIDMAR-2",
    "Sensor de Radiación PAR - CIDMAR-2",
    "Sensor de Batería - CIDMAR-2"
  ]}
  iconosVariables={{
    "Sensor de Altura de Olas - CIDMAR-2": "/iconosPaginaDatos/AlturaDeOlas.png",
    "Sensor de Dirección de Olas - CIDMAR-2": "/iconosPaginaDatos/DireccionDeOlas.png",
    "Sensor de Periodo de Olas - CIDMAR-2": "/iconosPaginaDatos/PeriodoDeOla.png",
    "Sensor de Dirección de la Corriente - CIDMAR-2": "/iconosPaginaDatos/DireccionDeCorriente.png",
    "Sensor de Velocidad de Corriente - CIDMAR-2": "/iconosPaginaDatos/VelocidadDeCorriente.png",
    "Sensor de Radiación PAR - CIDMAR-2": "/iconosPaginaDatos/RadiacionPar.png",
    "Sensor de Batería - CIDMAR-2": "/iconosPaginaDatos/Bateria.png"
  }}
/>

<!-- Visualización de gráficos -->
<BoyaVisualizacionDatos />

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
    position: relative;
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