<script lang="ts">
  import { onMount, afterUpdate } from 'svelte';

  let chart1: ApexCharts | null = null;

  let chartOptions = {
    chart: {
      type: 'line',
      height: 400,
      width: '100%',
      background: '#1e1e1e', // Fondo oscuro
      foreColor: '#ffffff' // Color del texto por defecto
    },
    series: [
      { name: 'Altura de Olas Medida (m)', data: [] },
      { name: 'Altura de Olas Pronosticada (m)', data: [1.0, 0.95, 1.1, 1.2, 1.05, 1.0, 1.15, 1.05] }
    ],
    xaxis: {
      categories: [],
      labels: {
        show: true,
        rotate: -45,
        style: {
          colors: '#ffffff', // Color de las etiquetas del eje X
          fontSize: '12px'
        },
        formatter: (val: string) => {
          return new Date(val).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
      },
      tickAmount: 10,
      axisBorder: {
        color: '#ffffff' // Color de la línea del eje X
      },
      axisTicks: {
        color: '#ffffff' // Color de las marcas de los ticks
      }
    },
    yaxis: {
      labels: {
        style: {
          colors: '#ffffff', // Color de las etiquetas del eje Y
          fontSize: '12px'
        },
        formatter: (value: number) => value.toFixed(2) + ' m'
      },
      axisBorder: {
        color: '#ffffff' // Color de la línea del eje Y
      },
      axisTicks: {
        color: '#ffffff' // Color de las marcas de los ticks
      }
    },
    grid: {
      borderColor: '#444444' // Color de las líneas de la cuadrícula
    },
    stroke: {
      curve: 'smooth',
      colors: ['#ff8c00', '#ffa500'] // Colores de las líneas
    },
    tooltip: {
      theme: 'dark' // Tema oscuro para el tooltip
    },
    legend: {
      labels: {
        colors: '#ffffff' // Color de las etiquetas en la leyenda
      }
    }
  };

  // Función para crear el gráfico
  const createChart = async () => {
    if (typeof window !== 'undefined') {
      const { default: ApexCharts } = await import('apexcharts');
      chart1 = new ApexCharts(document.querySelector("#chart1"), chartOptions);
      await chart1.render();
    }
  };

  // Función para obtener los datos de la API
  async function fetchData() {
    try {
      const response = await fetch("https://corsproxy.io/?http://emac.criba.edu.ar/servicios/getHistoryValues.php?station_code=EACC&var_code=14");
      const csvText = await response.text();

      const { fechas, valores } = parseCSV(csvText);

      // Actualizar opciones del gráfico
      chartOptions.series[0].data = valores;
      chartOptions.xaxis.categories = fechas;

      if (chart1) {
        chart1.updateOptions(chartOptions);
      }
    } catch (error) {
      console.error("Error al obtener datos de la API:", error);
    }
  }

  // Función para parsear el contenido CSV de la API
  function parseCSV(csv: string) {
    const rows = csv.split("\n").slice(1); // Saltar la cabecera
    const fechas: string[] = [];
    const valores: number[] = [];

    for (const row of rows) {
      if (row.trim()) {
        const [fecha, valor] = row.split(",");
        fechas.push(fecha.trim());
        valores.push(parseFloat(valor.trim()) || 0);
      }
    }
    return { fechas, valores };
  }

  onMount(() => {
    createChart();
    fetchData();
  });

  afterUpdate(() => {
    if (chart1) {
      chart1.updateOptions(chartOptions);
    }
  });
</script>

<!-- Contenedor del gráfico -->
<div id="chart1" style="width: 100%; max-width: 1200px; margin: 0 auto;"></div>
