<script>
  import { onMount } from 'svelte';
  import GraficoLineal from '$lib/components/datos/GraficosEstandar/GraficoLineal.svelte';

  // Descripciones breves para cada variable del puerto
  const descripcionesVariables = {
    "Humedad Exterior": "Porcentaje de humedad relativa en el aire.",
    "Presión Barométrica": "Presión atmosférica, útil para pronósticos del tiempo.",
    "Temperatura Exterior": "Temperatura del aire exterior.",
    "Velocidad del Viento": "Velocidad del aire registrada en la estación."
  };

  // Variables visibles del histórico
  const variablesAMostrar = {
    "Humedad Exterior": "humedadExteriorChart",
    "Presión Barométrica": "presionBarometricaChart",
    "Temperatura Exterior": "temperaturaExteriorChart",
    "Velocidad del Viento": "velocidadVientoChart"
  };

  let datos = {};
  let isLoading = true;
  let error = '';

  const endpointUrl = '/api/appcr/puerto/history';

  onMount(async () => {
    try {
      const res = await fetch(endpointUrl);

      if (!res.ok) {
        throw new Error(`Error HTTP: ${res.status} - ${res.statusText}`);
      }

      const jsonData = await res.json();
      console.log("📦 Datos del puerto recibidos:", jsonData);

      if (Object.keys(jsonData).length > 0) {
        datos = jsonData;
      } else {
        error = "La respuesta de la API no contiene datos válidos.";
      }
    } catch (err) {
      console.error("❌ Error al obtener datos de la estación del puerto:", err);
      error = "No se pudieron cargar los datos. Intentalo nuevamente más tarde.";
    } finally {
      isLoading = false;
    }
  });
</script>

<div class="charts">
  {#if isLoading}
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p class="estado">Cargando datos...</p>
    </div>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else}
    {#each Object.entries(variablesAMostrar) as [label, id]}
      <section class="chart-card">
        <div class="chart-header">
          <h3>{label}</h3>

          <div class="info-wrapper">
            <button class="info-button" aria-label={`Información sobre ${label}`}>ℹ️</button>

            <div class="info-tooltip">
              {descripcionesVariables[label]}
            </div>
          </div>
        </div>

        {#if datos[label] && datos[label].data.length > 0}
          <GraficoLineal
            data={datos[label].data}
            label={label}
            color="steelblue"
          />
        {:else}
          <p class="estado">No hay datos disponibles para esta variable.</p>
        {/if}
      </section>
    {/each}
  {/if}
</div>

<style>
  .charts {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    padding: 1rem;
    overflow: visible;
  }

  .chart-card {
    background: #fff;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    width: 100%;
    max-width: 100%;
    position: relative;
    overflow: visible;
  }

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 100%;
    margin-bottom: 0.5rem;
    gap: 0.75rem;
    overflow: visible;
  }

  .chart-header h3 {
    margin: 0;
    flex: 1;
    font-size: 1.1rem;
    color: #1f2937;
  }

  .info-wrapper {
    position: relative;
    z-index: 50;
    flex-shrink: 0;
  }

  .info-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
    line-height: 1;
    padding: 0;
  }

  .info-tooltip {
    display: none;
    position: absolute;
    top: 130%;
    right: 0;
    left: auto;
    transform: none;
    background: #f1f1f1;
    color: #333;
    padding: 0.6rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 0.85rem;
    width: 220px;
    z-index: 9999;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    line-height: 1.35;
  }

  .info-wrapper:hover .info-tooltip {
    display: block;
  }

  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
  }

  .loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: #09f;
    animation: spin 1s ease infinite;
    margin: 1rem auto 0;
  }

  .estado {
    margin: 0.5rem 0;
    font-size: 0.95rem;
    color: #4b5563;
    text-align: center;
  }

  .estado.error {
    color: #b91c1c;
    font-weight: 600;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @media (max-width: 640px) {
    .charts {
      padding: 0.75rem;
      gap: 1.25rem;
    }

    .chart-card {
      padding: 0.85rem;
    }

    .chart-header h3 {
      font-size: 1rem;
    }

    .info-tooltip {
      width: 190px;
      font-size: 0.8rem;
    }
  }
</style>