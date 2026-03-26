<script>
    import { onMount } from 'svelte';
    import GraficoLineal from '$lib/components/datos/GraficosEstandar/GraficoLineal.svelte';
    import GraficoPolar from '$lib/components/datos/GraficosEstandar/GraficoPolar.svelte';

    const descripcionesVariables = {
    "Altura de Olas": "Altura media de las olas registradas. Útil para evaluar el estado del mar.",
    "Periodo de Olas": "Tiempo entre dos crestas de ola consecutivas. Relacionado con la energía del oleaje.",
    "Dirección de Olas": "Ángulo desde el que provienen las olas. Se mide en grados respecto al norte.",
    "Velocidad de Corriente": "Velocidad del flujo de agua en la zona. Es fundamental para navegación y dispersión de contaminantes.",
    "Dirección de la Corriente": "Dirección hacia donde se mueve la corriente. Expresada en grados.",
    "Radiación PAR": "Radiación fotosintéticamente activa. Importante para estudios biológicos y de producción primaria.",
    "Batería": "Voltaje de la batería de la plataforma. Indicador del estado energético del equipo."
};


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
        align-items: center;
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
    }

    .info-wrapper:hover .info-tooltip {
        display: block;
    }

    @media (max-width: 640px) {
        .charts {
            padding: 0.75rem;
            gap: 1.25rem;
        }

        .chart-card {
            padding: 0.85rem;
        }

        .chart-header {
            align-items: flex-start;
        }

        .chart-header h3 {
            font-size: 1rem;
        }

        .info-tooltip {
            width: 190px;
            font-size: 0.8rem;
            right: 0;
        }
    }
</style>

<div class="charts">
    {#each Object.entries(buoyVariables) as [label, id]}
        {#if label !== "Velocidad de Corriente"}<!-- Aca elimino alguno de los graficos -->
            <div class="chart-card">
                <div class="chart-header">
                    <h3>{label}</h3>
                    <div class="info-wrapper">
                        <button class="info-button">ℹ️</button>
                        <div class="info-tooltip">
                            {descripcionesVariables[label]}
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
        {/if}
    {/each}
</div>