<script>
  import { onMount, onDestroy } from 'svelte';
  import ApexCharts from 'apexcharts';

  export let data = [];
  export let label = '';
  export let color = '#2563eb';
  export let height = 320;

  let chartContainer;
  let chartInstance;

  // =========================================================
  // HELPERS DE FORMATO
  // =========================================================

  function obtenerDecimales(label) {
    const texto = (label || '').toLowerCase();

    if (texto.includes('altura')) return 2;
    if (texto.includes('periodo') || texto.includes('período')) return 1;
    if (texto.includes('bater')) return 2;
    if (texto.includes('radiación') || texto.includes('radiacion')) return 0;
    if (texto.includes('temperatura')) return 1;
    if (texto.includes('humedad')) return 0;
    if (texto.includes('velocidad')) return 1;

    return 1;
  }

  function formatearValor(label, valor) {
    const numero = Number(valor);
    if (Number.isNaN(numero)) return '–';

    return numero.toFixed(obtenerDecimales(label));
  }

  function obtenerUnidad(data) {
    const unidad = data.find(d => d?.unit)?.unit;
    return unidad ? String(unidad).trim() : '';
  }

  function obtenerGapMaximoMs(label) {
    const texto = (label || '').toLowerCase();

    // Regla base razonable para cortar líneas en huecos grandes
    if (texto.includes('bater')) return 12 * 60 * 60 * 1000;
    return 6 * 60 * 60 * 1000;
  }

  function normalizarDatos(data) {
    if (!Array.isArray(data)) return [];

    return data
      .filter(d => d && d.timestamp !== undefined && d.value !== undefined && d.value !== null && !isNaN(d.value))
      .map(d => ({
        ...d,
        timestamp: d.timestamp instanceof Date ? d.timestamp : new Date(d.timestamp),
        value: parseFloat(d.value)
      }))
      .filter(d => !isNaN(d.timestamp.getTime()) && !isNaN(d.value))
      .sort((a, b) => a.timestamp - b.timestamp);
  }

  // Esta función arma segmentos separados cuando hay huecos grandes.
  // Así evitamos que el gráfico una puntos con una línea engañosa.
  function construirSeriesConGaps(datosNormalizados, label) {
    const gapMaximoMs = obtenerGapMaximoMs(label);
    const series = [];

    if (datosNormalizados.length === 0) return series;

    let segmentoActual = [];

    for (let i = 0; i < datosNormalizados.length; i++) {
      const punto = datosNormalizados[i];

      if (i === 0) {
        segmentoActual.push({
          x: punto.timestamp.getTime(),
          y: punto.value
        });
        continue;
      }

      const anterior = datosNormalizados[i - 1];
      const diferencia = punto.timestamp - anterior.timestamp;

      if (diferencia > gapMaximoMs) {
        if (segmentoActual.length > 0) {
          series.push({
            name: label,
            data: segmentoActual
          });
        }

        segmentoActual = [];
      }

      segmentoActual.push({
        x: punto.timestamp.getTime(),
        y: punto.value
      });
    }

    if (segmentoActual.length > 0) {
      series.push({
        name: label,
        data: segmentoActual
      });
    }

    return series;
  }

  function formatearFechaCorta(timestamp) {
    const fecha = new Date(timestamp);

    return fecha.toLocaleDateString('es-AR', {
      day: '2-digit',
      month: '2-digit'
    });
  }

  function formatearFechaTooltip(timestamp) {
    const fecha = new Date(timestamp);

    return fecha.toLocaleDateString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }

  function formatearHoraTooltip(timestamp) {
    const fecha = new Date(timestamp);

    return fecha.toLocaleTimeString('es-AR', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  }

  // =========================================================
  // DATOS DERIVADOS
  // =========================================================

  $: datosNormalizados = normalizarDatos(data);
  $: unidadGrafico = obtenerUnidad(datosNormalizados);
  $: seriesApex = construirSeriesConGaps(datosNormalizados, label);

  // =========================================================
  // OPCIONES DEL GRÁFICO
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
            download: true,
            selection: false,
            zoom: true,
            zoomin: true,
            zoomout: true,
            pan: true,
            reset: true
          }
        },
        zoom: {
          enabled: true
        },
        foreColor: '#374151',
        fontFamily: 'inherit'
      },

      series: seriesApex,

      colors: [color],

      stroke: {
        curve: 'straight',
        width: esMobile ? 2 : 3
      },

      markers: {
        size: esMobile ? 3 : 4,
        hover: {
          sizeOffset: 2
        }
      },

      dataLabels: {
        enabled: false
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
          formatter: function (value) {
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
        decimalsInFloat: obtenerDecimales(label),
        labels: {
          style: {
            fontSize: esMobile ? '10px' : '11px'
          },
          formatter: function (value) {
            return formatearValor(label, value);
          }
        }
      },

      tooltip: {
        shared: false,
        intersect: true,
        x: {
          formatter: function (value) {
            const fecha = formatearFechaTooltip(value);
            const hora = formatearHoraTooltip(value);
            return `${fecha} ${hora}`;
          }
        },
        y: {
          formatter: function (value) {
            const valor = formatearValor(label, value);
            return unidadGrafico ? `${valor} ${unidadGrafico}` : valor;
          },
          title: {
            formatter: function () {
              return `${label}: `;
            }
          }
        }
      },

      legend: {
        show: false
      },

      responsive: [
        {
          breakpoint: 640,
          options: {
            chart: {
              height: 260
            }
          }
        },
        {
          breakpoint: 420,
          options: {
            chart: {
              height: 240
            }
          }
        }
      ]
    };
  }

  // =========================================================
  // RENDER / UPDATE
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

  // Si cambian los datos o propiedades, recreamos el gráfico.
  $: if (chartContainer && data) {
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
  {#if unidadGrafico}
    <p class="unidad-grafico">Unidad: {unidadGrafico}</p>
  {/if}

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