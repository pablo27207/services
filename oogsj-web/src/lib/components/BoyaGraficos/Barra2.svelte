<script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    let chart: ApexCharts | null = null;
    let chartContainer: HTMLDivElement | null = null;

    let chartOptions = {
        chart: {
            type: 'bar',
            height: 350
        },
        series: [
            {
                name: 'Mínimo Normal',
                data: [200]  // Mínimo de Radiación PAR
            },
            {
                name: 'Máximo Normal',
                data: [800]  // Máximo de Radiación PAR
            },
            {
                name: 'Valor Medido',
                data: [500]  // Valor actual medido
            }
        ],
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '40%', // Ajusta el ancho de las barras
            }
        },
        xaxis: {
            categories: ['Radiación PAR'] // Etiqueta de la categoría
        },
        yaxis: {
            title: {
                text: 'Radiación PAR (µmol/m²/s)' // Unidad de medida
            }
        },
        title: {
            text: 'Radiación PAR',
            align: 'center'
        },
        colors: ['#00C853', '#D50000', '#2962FF'], // Verde (mínimo), Rojo (máximo), Azul (medido)
        dataLabels: {
            enabled: true
        }
    };

    const createChart = async () => {
        if (typeof window !== 'undefined' && chartContainer) {
            const { default: ApexCharts } = await import('apexcharts');
            chart = new ApexCharts(chartContainer, chartOptions);
            chart.render();
        }
    };

    onMount(() => {
        createChart();
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
            chart = null;
        }
    });
</script>

<style>
    #barRadiacion {
        max-width: 500px;
        margin: auto;
    }
</style>

<div bind:this={chartContainer} id="barRadiacion"></div>
