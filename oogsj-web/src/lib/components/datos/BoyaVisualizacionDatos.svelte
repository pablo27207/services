<script>
  import { onMount } from 'svelte';
  import GraficoLineal from '$lib/components/datos/GraficosEstandar/GraficoLineal.svelte';
  import GraficoPolar from '$lib/components/datos/GraficosEstandar/GraficoPolar.svelte';

  const buoyVariables = {
    "Altura de Olas": "altura_olas_chart",
    "Periodo de Olas": "periodo_olas_chart",
    "Dirección de Olas": "direccion_olas_chart",
    "Velocidad de Corriente": "velocidad_corriente_chart",
    "Dirección de la Corriente": "direccion_corriente_chart",
    "Radiación PAR": "radiacion_par_chart",
    "Batería": "bateria_chart"
  };

  let datos = {};

  onMount(async () => {
    try {
      const res = await fetch('/api/buoy');
      datos = await res.json();
      console.log("📦 Datos recibidos:", datos);
    } catch (error) {
      console.error("❌ Error al obtener datos:", error);
    }
  });
</script>

<style>
  .charts {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    padding: 1rem;
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
    align-items: center;
    width: 100%;
     max-width: 100%;
  }

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .chart-header h3 {
    margin: 0;
  }

  .info-wrapper {
    position: relative;
  }

  .info-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
  }

  .info-tooltip {
    display: none;
    position: absolute;
    top: 130%;
    left: 50%;
    transform: translateX(-50%);
    background: #f1f1f1;
    color: #333;
    padding: 0.6rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 0.85rem;
    width: 220px;
    z-index: 5;
  }

  .info-wrapper:hover .info-tooltip {
    display: block;
  }
</style>

<div class="charts">
  {#each Object.entries(buoyVariables) as [label, id]}
    <div class="chart-card">
      <div class="chart-header">
        <h3>{label}</h3>
        <div class="info-wrapper">
          <button class="info-button">ℹ️</button>
          <div class="info-tooltip">
            Explicación sobre {label}. Aquí podés poner cómo se interpreta esta variable.
          </div>
        </div>
      </div>

      {#if datos[label]}
        {#if label.includes("Dirección")}
          <GraficoPolar data={datos[label]} label={label} />
        {:else}
          <GraficoLineal data={datos[label]} label={label} color="steelblue" />
        {/if}
      {:else}
        <p>Cargando datos...</p>
      {/if}
    </div>
  {/each}
</div>
