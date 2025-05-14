<script lang="ts">
  import { onMount, afterUpdate } from 'svelte';

  let chart1: ApexCharts | null = null;

  let chartOptions = {
    chart: { type: 'line', height: 400, width: '100%' },
    series: [{ name: 'Radiación PAR (+2.0m)', data: [] }],
    xaxis: {
      categories: [],
      labels: {
        show: true,
        rotate: -45, // Girar etiquetas para evitar solapamientos
        formatter: (val: string) => {
          return new Date(val).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); // Mostrar solo la hora
        }
      },
      tickAmount: 10 // Mostrar un número limitado de etiquetas
    },
    yaxis: {
      labels: {
        formatter: (value: number) => `${value.toFixed(0)} µmol/m²·s` // Mostrar unidad
      }
    }
  };

  // Función para crear el gráfico
  const createChart = async () => {
    if (typeof window !== 'undefined') {
      const { default: ApexCharts } = await import('apexcharts');
      chart1 = new ApexCharts(document.querySelector("#chart4"), chartOptions);
      await chart1.render();
    }
  };

  // Función para obtener los datos de la API
  async function fetchData() {
    try {
      const response = await fetch("https://corsproxy.io/?http://emac.criba.edu.ar/servicios/getHistoryValues.php?station_code=EACC&var_code=33"); // borrar el 3 del final
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
<div id="chart4" style="width: 100%; max-width: 1200px; margin: 0 auto;"></div>
