<script>
  import { onMount, onDestroy } from 'svelte';
  import ApexCharts from 'apexcharts';

  export let data = [];
  export let label = '';
  export let height = 360;

  let chartContainer;
  let chartInstance;

  // =========================================================
  // CONFIGURACIÓN DE SECTORES
  // =========================================================

  // 8 sectores para que sea simple y entendible para cualquier usuario.
  const sectoresBase = [
    { key: 'N',  nombre: 'Norte',      desde: 337.5, hasta: 22.5 },
    { key: 'NE', nombre: 'Noreste',    desde: 22.5,  hasta: 67.5 },
    { key: 'E',  nombre: 'Este',       desde: 67.5,  hasta: 112.5 },
    { key: 'SE', nombre: 'Sudeste',    desde: 112.5, hasta: 157.5 },
    { key: 'S',  nombre: 'Sur',        desde: 157.5, hasta: 202.5 },
    { key: 'SO', nombre: 'Suroeste',   desde: 202.5, hasta: 247.5 },
    { key: 'O',  nombre: 'Oeste',      desde: 247.5, hasta: 292.5 },
    { key: 'NO', nombre: 'Noroeste',   desde: 292.5, hasta: 337.5 }
  ];

  // =========================================================
  // HELPERS DE FORMATO
  // =========================================================

  function formatearFechaHora(fecha) {
    if (!fecha || isNaN(fecha.getTime())) return '–';

    return fecha.toLocaleString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  }

  function formatearPorcentaje(valor) {
    const numero = Number(valor);
    if (Number.isNaN(numero)) return '0.0';
    return numero.toFixed(1);
  }

  // Normaliza grados al rango 0–360
  function normalizarGrados(valor) {
    const numero = Number(valor);
    if (Number.isNaN(numero)) return null;

    return ((numero % 360) + 360) % 360;
  }

  // Determina a qué sector pertenece cada valor angular
  function obtenerSector(grados) {
    const valor = normalizarGrados(grados);
    if (valor === null) return null;

    if (valor >= 337.5 || valor < 22.5) return 'N';
    if (valor >= 22.5 && valor < 67.5) return 'NE';
    if (valor >= 67.5 && valor < 112.5) return 'E';
    if (valor >= 112.5 && valor < 157.5) return 'SE';
    if (valor >= 157.5 && valor < 202.5) return 'S';
    if (valor >= 202.5 && valor < 247.5) return 'SO';
    if (valor >= 247.5 && valor < 292.5) return 'O';
    if (valor >= 292.5 && valor < 337.5) return 'NO';

    return null;
  }

  function obtenerRangoTexto(sector) {
    if (!sector) return '–';

    if (sector.key === 'N') return '337.5°–360° y 0°–22.5°';
    return `${sector.desde}°–${sector.hasta}°`;
  }

  // =========================================================
  // NORMALIZACIÓN DE DATOS
  // =========================================================

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

  function agruparPorSectores(datosNormalizados) {
    const total = datosNormalizados.length;

    const acumulado = sectoresBase.map(sector => ({
      ...sector,
      count: 0,
      percentage: 0
    }));

    datosNormalizados.forEach(dato => {
      const claveSector = obtenerSector(dato.value);
      if (!claveSector) return;

      const sector = acumulado.find(s => s.key === claveSector);
      if (sector) sector.count += 1;
    });

    acumulado.forEach(sector => {
      sector.percentage = total > 0 ? (sector.count / total) * 100 : 0;
      sector.rango = obtenerRangoTexto(sector);
    });

    return acumulado;
  }

  function obtenerPeriodo(datosNormalizados) {
    if (!datosNormalizados.length) {
      return {
        desde: null,
        hasta: null,
        texto: 'Sin período disponible'
      };
    }

    const desde = datosNormalizados[0].timestamp;
    const hasta = datosNormalizados[datosNormalizados.length - 1].timestamp;

    return {
      desde,
      hasta,
      texto: `Porcentajes calculados entre ${formatearFechaHora(desde)} y ${formatearFechaHora(hasta)}`
    };
  }

  // =========================================================
  // DATOS DERIVADOS
  // =========================================================

  $: datosNormalizados = normalizarDatos(data);
  $: sectoresAgrupados = agruparPorSectores(datosNormalizados);
  $: periodo = obtenerPeriodo(datosNormalizados);

  // Serie que consume ApexCharts
  $: seriesApex = sectoresAgrupados.map(sector => Number(sector.percentage.toFixed(2)));
  $: labelsApex = sectoresAgrupados.map(sector => sector.key);

  // =========================================================
  // OPCIONES DEL GRÁFICO
  // =========================================================

  function crearOpciones() {
    const esMobile = typeof window !== 'undefined' ? window.innerWidth < 640 : false;

    return {
      chart: {
        type: 'polarArea',
        height,
        toolbar: {
          show: true,
          tools: {
            download: false,
            selection: false,
            zoom: false,
            zoomin: false,
            zoomout: false,
            pan: false,
            reset: false
          },
          export: {
            csv: {
              filename: `${label.toLowerCase().replace(/\s+/g, '_')}_polar`,
              columnDelimiter: ',',
              headerCategory: 'sector',
              headerValue: 'porcentaje',
              categoryFormatter: function (x) {
                return x;
              },
              valueFormatter: function (y) {
                return y;
              }
            }
          }
        },
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 350
        },
        fontFamily: 'inherit'
      },

      series: seriesApex,

      labels: labelsApex,

      stroke: {
        colors: ['#ffffff'],
        width: 1.5
      },

      fill: {
        opacity: 0.9
      },

      legend: {
        show: true,
        position: esMobile ? 'bottom' : 'right',
        fontSize: esMobile ? '11px' : '12px',
        labels: {
          colors: '#374151'
        }
      },

      dataLabels: {
        enabled: true,
        formatter: function (val) {
          return `${formatearPorcentaje(val)}%`;
        },
        style: {
          fontSize: esMobile ? '10px' : '11px',
          fontWeight: 600
        },
        dropShadow: {
          enabled: false
        }
      },

      plotOptions: {
        polarArea: {
          rings: {
            strokeWidth: 1
          },
          spokes: {
            strokeWidth: 1
          }
        }
      },

      yaxis: {
        show: false
      },

      xaxis: {
        labels: {
          show: true,
          style: {
            fontSize: esMobile ? '10px' : '11px',
            colors: ['#374151']
          }
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

      tooltip: {
        shared: false,
        intersect: true,
        custom: function ({ series, seriesIndex, w }) {
          const sector = sectoresAgrupados[seriesIndex];
          if (!sector) return '<div class="apex-tooltip-custom">Sin datos</div>';

          return `
            <div class="apex-tooltip-custom">
              <div><strong>${label}</strong></div>
              <div><strong>Sector:</strong> ${sector.nombre} (${sector.key})</div>
              <div><strong>Rango:</strong> ${sector.rango}</div>
              <div><strong>Observaciones:</strong> ${sector.count}</div>
              <div><strong>Porcentaje:</strong> ${formatearPorcentaje(sector.percentage)}%</div>
              <div><strong>Período:</strong> ${formatearFechaHora(periodo.desde)} a ${formatearFechaHora(periodo.hasta)}</div>
            </div>
          `;
        }
      },

      responsive: [
        {
          breakpoint: 640,
          options: {
            chart: {
              height: 320
            }
          }
        },
        {
          breakpoint: 420,
          options: {
            chart: {
              height: 290
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

  // Redibuja si cambian los datos
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

<div class="grafico-polar-card">
  {#if datosNormalizados.length > 0}
    <p class="periodo-texto">{periodo.texto}</p>
    <p class="ayuda-texto">
      Este gráfico muestra desde qué direcciones se registró con mayor frecuencia la variable medida.
    </p>
  {/if}

  <div bind:this={chartContainer} class="chart-container"></div>
</div>

<style>
  .grafico-polar-card {
    width: 100%;
    position: relative;
    padding: 0.5rem;
    background: white;
    border-radius: 12px;
    margin-bottom: 1rem;
    box-sizing: border-box;

    overflow: visible; /* ← CLAVE */
  }

  .periodo-texto {
    margin: 0 0 0.25rem 0.35rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #4b5563;
    text-align: left;
  }

  .ayuda-texto {
    margin: 0 0 0.6rem 0.35rem;
    font-size: 0.88rem;
    color: #6b7280;
    text-align: left;
    line-height: 1.35;
  }

  .chart-container {
    width: 100%;
    overflow: visible;
    position: relative;
  }

  :global(.apex-tooltip-custom) {
    background: #ffffff;
    border: 1px solid #d1d5db;
    padding: 10px 12px;
    border-radius: 8px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
    color: #111827;
    font-size: 0.84rem;
    line-height: 1.45;
    max-width: 240px;
     z-index: 9999;
  }

  @media (max-width: 640px) {
    .grafico-polar-card {
      padding: 0.35rem;
      border-radius: 10px;
    }

    .periodo-texto {
      font-size: 0.82rem;
      margin-left: 0.25rem;
    }

    .ayuda-texto {
      font-size: 0.8rem;
      margin-left: 0.25rem;
    }

    :global(.apex-tooltip-custom) {
      font-size: 0.78rem;
      max-width: 210px;
      padding: 8px 10px;
    }
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
</style>