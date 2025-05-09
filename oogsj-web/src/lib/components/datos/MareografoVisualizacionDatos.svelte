<!-- MareografoVisualizacionDatos.svelte -->
<script lang="ts">
    import { onMount } from "svelte";
    import GraficoMareografo from '$lib/components/datos/GraficosEstandar/GraficoMareografo.svelte';

    let mareographData: { timestamp: string; level: number }[] = [];
    let tideForecastData: { timestamp: string; level: number }[] = [];
    let infoTooltip: HTMLDivElement | null = null;

    const fetchData = async () => {
        try {
            const mareographResponse = await fetch("/api/mareograph");
            mareographData = await mareographResponse.json();

            const tideResponse = await fetch("/api/tide_forecast");
            tideForecastData = await tideResponse.json();
        } catch (error) {
            console.error("❌ Error al obtener datos:", error);
        }
    };

    onMount(fetchData);
</script>

<!-- Contenedor -->
<div class="chart-container">
    <div class="chart-header">
        <h3>Mareógrafo y Predicción de Marea</h3>
        <div class="info-button" 
             on:mouseover={() => infoTooltip && (infoTooltip.style.display = "block")}
             on:mouseout={() => infoTooltip && (infoTooltip.style.display = "none")}
        >
            ℹ️
            <div bind:this={infoTooltip} class="info-tooltip">
                📊 Este gráfico muestra los niveles del mareógrafo y la predicción de marea. 
                La línea azul representa los datos reales del mareógrafo, 
                mientras que la línea roja punteada muestra la predicción de los niveles de marea esperados.
            </div>
        </div>
    </div>

    {#if mareographData.length || tideForecastData.length}
        <GraficoMareografo {mareographData} {tideForecastData} />
    {:else}
        <p>Cargando datos...</p>
    {/if}

    <div class="legend-container">
        <div class="legend-item">
            <div class="legend-color" style="background: steelblue;"></div>
            <span><strong>Mareógrafo</strong></span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: red;"></div>
            <span><strong>Predicción de Marea</strong></span>
        </div>
    </div>
</div>

<style>
    .chart-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 700px;
        margin: auto;
        padding: 1rem;
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        position: relative;
    }

    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    .info-button {
        position: relative;
        font-size: 1.2rem;
        cursor: pointer;
        margin-right: 20px;
    }

    .info-tooltip {
        display: none;
        position: absolute;
        top: 25px;
        left: -100px;
        background: rgba(0, 0, 0, 0.8);
        color: #fff;
        padding: 6px 10px;
        border-radius: 5px;
        font-size: 12px;
        width: 220px;
        text-align: center;
    }

    .legend-container {
        display: flex;
        gap: 15px;
        margin-top: 10px;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #f4f4f4;
        padding: 5px 10px;
        border-radius: 5px;
    }

    .legend-color {
        width: 16px;
        height: 16px;
        border-radius: 3px;
    }
</style>