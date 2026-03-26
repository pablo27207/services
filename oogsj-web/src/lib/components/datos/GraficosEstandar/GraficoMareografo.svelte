<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import ApexCharts from 'apexcharts';

  // Serie del mareógrafo observado
  export let mareographData: { timestamp: string; level: number }[] = [];

  // Serie de referencia / predicción de marea
  export let tideForecastData: { timestamp: string; level: number }[] = [];

  // Altura base del gráfico
  export let height = 360;

  let chartContainer: HTMLDivElement;
  let chartInstance: ApexCharts | null = null;

  // =========================================================
  // HELPERS DE FORMATO
  // =========================================================

  function formatearValor(valor: number | string | null | undefined): string {
    const numero = Number(valor);
    if (Number.isNaN(numero)) return '–';
    return numero.toFixed(2);
  }

  function formatearFechaCorta(timestamp: number): string {
    const fecha = new Date(timestamp);

    return fecha.toLocaleDateString('es-AR', {
      day: '2-digit',
      month: '2-digit'
    });
  }

  function formatearFechaTooltip(timestamp: number): string {
    const fecha = new Date(timestamp);

    return fecha.toLocaleDateString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }

  function formatearHoraTooltip(timestamp: number): string {
    const fecha = new Date(timestamp);

    return fecha.toLocaleTimeString('es-AR', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  }

  // Convierte y limpia la serie del mareógrafo
  function normalizarSerieMareografo(data: { timestamp: string; level: number }[]) {
    if (!Array.isArray(data)) return [];

    return data
      .filter(d => d && d.timestamp !== undefined && d.level !== undefined && d.level !== null && !isNaN(Number(d.level)))
      .map(d => ({
        x: new Date(d.timestamp).getTime(),
        y: Number(d.level)
      }))
      .filter(d => !isNaN(d.x) && !isNaN(d.y))
      .sort((a, b) => a.x - b.x);
  }

  // Convierte y limpia la serie de referencia / predicción
  function normalizarSeriePrediccion(data: { timestamp: string; level: number }[]) {
    if (!Array.isArray(data)) return [];

    return data
      .filter(d => d && d.timestamp !== undefined && d.level !== undefined && d.level !== null && !isNaN(Number(d.level)))
      .map(d => ({
        x: new Date(d.timestamp).getTime(),
        y: Number(d.level)
      }))
      .filter(d => !isNaN(d.x) && !isNaN(d.y))
      .sort((a, b) => a.x - b.x);
  }

  // Calcula rango Y dinámico tomando ambas series
  function obtenerRangoY(
    serie1: { x: number; y: number }[],
    serie2: { x: number; y: number }[]
  ) {
    const todosLosValores = [...serie1, ...serie2].map(p => p.y);

    if (!todosLosValores.length) {
      return { min: 0, max: 1 };
    }

    const min = Math.min(...todosLosValores);
    const max = Math.max(...todosLosValores);

    let buffer = (max - min) * 0.1;

    if (buffer === 0) {
      buffer = Math.abs(max) * 0.05 || 0.2;
    }

    return {
      min: Number((min - buffer).toFixed(2)),
      max: Number((max + buffer).toFixed(2))
    };
  }

  // =========================================================
  // DATOS DERIVADOS
  // =========================================================

  $: serieMareografo = normalizarSerieMareografo(mareographData);
  $: seriePrediccion = normalizarSeriePrediccion(tideForecastData);
  $: rangoY = obtenerRangoY(serieMareografo, seriePrediccion);

  $: seriesApex = [
    {
      name: 'Mareógrafo observado',
      data: serieMareografo
    },
    {
      name: 'Referencia naval',
      data: seriePrediccion
    }
  ];

  // =========================================================
  // CONFIGURACIÓN APEXCHARTS
  // =========================================================

  function crearOpciones() {
    const esMobile = typeof window !== 'undefined' ? window.innerWidth < 640 : false;

    return {
      chart: {
        type: 'line',
        height,
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 350
        },
        toolbar: {
          show: true,
          tools: {
            download: false,
            selection: false,
            zoom: true,
            zoomin: true,
            zoomout: true,
            pan: true,
            reset: true
          },
          export: {
            csv: {
              filename: 'mareografo_comodoro_rivadavia',
              columnDelimiter: ',',
              headerCategory: 'fecha',
              headerValue: 'nivel_mar',
              categoryFormatter: function (x: number) {
                return new Date(x).toLocaleString('es-AR');
              },
              valueFormatter: function (y: number) {
                return y;
              }
            }
          }
        },
        zoom: {
          enabled: true
        },
        fontFamily: 'inherit',
        foreColor: '#374151'
      },

      series: seriesApex,

      colors: ['#2563eb', '#dc2626'],

      stroke: {
        curve: 'straight',
        width: [3, 2.5],
        dashArray: [0, 6]
      },

      markers: {
        size: esMobile ? 0 : 0
      },

      dataLabels: {
        enabled: false
      },

      legend: {
        show: true,
        position: esMobile ? 'bottom' : 'top',
        horizontalAlign: esMobile ? 'center' : 'left',
        fontSize: esMobile ? '11px' : '12px',
        labels: {
          colors: '#374151'
        }
      },

      noData: {
        text: 'No hay datos disponibles',
        align: 'center',
        verticalAlign: 'middle',
        style: {
          color: '#6b7280',
          fontSize: '14px'
        }
      },

      grid: {
        borderColor: '#e5e7eb',
        strokeDashArray: 3,
        padding: {
          left: 8,
          right: 10,
          top: 10,
          bottom: 0
        }
      },

      xaxis: {
        type: 'datetime',
        labels: {
          datetimeUTC: false,
          style: {
            fontSize: esMobile ? '10px' : '11px'
          },
          formatter: function (value: number) {
            return formatearFechaCorta(value);
          }
        },
        axisBorder: {
          color: '#9ca3af'
        },
        axisTicks: {
          color: '#9ca3af'
        },
        tooltip: {
          enabled: false
        }
      },

      yaxis: {
        min: rangoY.min,
        max: rangoY.max,
        tickAmount: 6,
        labels: {
          style: {
            fontSize: esMobile ? '10px' : '11px'
          },
          formatter: function (value: number) {
            return formatearValor(value);
          }
        },
        title: {
          text: 'Altura del mar (m)',
          style: {
            fontSize: esMobile ? '11px' : '12px',
            fontWeight: 600
          }
        }
      },

      tooltip: {
        shared: true,
        intersect: false,
        x: {
          formatter: function (value: number) {
            const fecha = formatearFechaTooltip(value);
            const hora = formatearHoraTooltip(value);
            return `${fecha} ${hora}`;
          }
        },
        y: {
          formatter: function (value: number) {
            return `${formatearValor(value)} m`;
          }
        }
      },

      responsive: [
        {
          breakpoint: 640,
          options: {
            chart: {
              height: 290
            }
          }
        },
        {
          breakpoint: 420,
          options: {
            chart: {
              height: 260
            }
          }
        }
      ]
    };
  }

  // =========================================================
  // RENDER Y ACTUALIZACIÓN
  // =========================================================

  async function renderChart() {
    if (!chartContainer) return;

    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }

    const opciones = crearOpciones();
    chartInstance = new ApexCharts(chartContainer, opciones);
    await chartInstance.render();
  }

  onMount(() => {
    renderChart();

    const onResize = () => {
      renderChart();
    };

    window.addEventListener('resize', onResize);

    return () => {
      window.removeEventListener('resize', onResize);

      if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
      }
    };
  });

  // Si cambian los datos, se vuelve a renderizar
  $: if (chartContainer && (mareographData.length || tideForecastData.length)) {
    renderChart();
  }

  onDestroy(() => {
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
  });
</script>

<div class="grafico-card">
  <p class="unidad-grafico">Unidad: m</p>
  <div bind:this={chartContainer} class="chart-container"></div>
</div>

<style>
  .grafico-card {
    width: 100%;
    position: relative;
    padding: 0.5rem;
    background: white;
    border-radius: 12px;
    margin-bottom: 1rem;
    box-sizing: border-box;
    overflow: visible;
  }

  .unidad-grafico {
    margin: 0 0 0.45rem 0.4rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #4b5563;
    text-align: left;
  }

  .chart-container {
    width: 100%;
    position: relative;
    overflow: visible;
  }

  :global(.apexcharts-canvas) {
    overflow: visible !important;
  }

  :global(.apexcharts-tooltip) {
    z-index: 9999 !important;
  }

  :global(.apexcharts-menu) {
    z-index: 9999 !important;
  }

  @media (max-width: 640px) {
    .grafico-card {
      padding: 0.35rem;
      border-radius: 10px;
    }

    .unidad-grafico {
      font-size: 0.82rem;
      margin-left: 0.25rem;
    }
  }
</style>