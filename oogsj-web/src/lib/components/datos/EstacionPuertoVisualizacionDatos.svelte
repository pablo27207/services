<script>
    import { onMount } from 'svelte';
    import GraficoLineal from '$lib/components/datos/GraficosEstandar/GraficoLineal.svelte';
    import GraficoPolar from '$lib/components/datos/GraficosEstandar/GraficoPolar.svelte';

    const descripcionesVariables = {
        "Humedad Exterior": "Porcentaje de humedad relativa en el aire.",
        "Presión Barométrica": "Presión atmosférica, útil para pronósticos del tiempo.",
        "Temperatura Exterior": "Temperatura del aire exterior.",
        "Velocidad del Viento": "Velocidad del aire en la estación."
    };

    const variablesAmostrar = {
        "Humedad Exterior": "humedadExteriorChart",
        "Presión Barométrica": "presionBarometricaChart",
        "Temperatura Exterior": "temperaturaExteriorChart",
        "Velocidad del Viento": "velocidadVientoChart"
    };

    let datos = {};
    let isLoading = true;
    let error = null;

    const endpointUrl = '/api/appcr/puerto/history';

    onMount(async () => {
        try {
            const res = await fetch(endpointUrl);
            if (!res.ok) {
                throw new Error(`Error HTTP: ${res.status} - ${res.statusText}`);
            }
            const jsonData = await res.json();
            console.log("📦 Datos del puerto recibidos:", jsonData);
            
            // Verificamos si los datos tienen la estructura esperada
            if (Object.keys(jsonData).length > 0) {
                datos = jsonData;
            } else {
                error = "La respuesta de la API no contiene datos válidos.";
            }
        } catch (err) {
            console.error("❌ Error al obtener datos de la estación del puerto:", err);
            error = "No se pudieron cargar los datos. Por favor, intente de nuevo más tarde.";
        } finally {
            isLoading = false;
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

    .loading-spinner {
        border: 4px solid rgba(0, 0, 0, 0.1);
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border-left-color: #09f;
        animation: spin 1s ease infinite;
        margin: 2rem auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>

<div class="charts">
    {#if isLoading}
        <div class="loading-spinner"></div>
        <p>Cargando datos...</p>
    {:else if error}
        <p style="color: red;">{error}</p>
    {:else}
        {#each Object.entries(variablesAmostrar) as [label, id]}
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

                {#if datos[label] && datos[label].data.length > 0}
                    {#if label.includes("Dirección")}
                        <!-- Aquí iría GraficoPolar, si la API lo proporcionara -->
                        <p>Gráfico polar no disponible para este conjunto de datos.</p>
                    {:else}
                        <GraficoLineal data={datos[label].data} label={label} color="steelblue" />
                    {/if}
                {:else}
                    <p>No hay datos disponibles para esta variable.</p>
                {/if}
            </div>
        {/each}
    {/if}
</div>
