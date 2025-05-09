<script lang="ts">
  import { onMount, afterUpdate } from 'svelte';

  let chart1: ApexCharts | null = null;

  let chartOptions = {
    chart: { type: 'line', height: 350 },
    series: [{ name: 'Velocidad Corriente (-0.5m)', data: [] }], // Serie vacía, se llenará dinámicamente
    xaxis: { categories: [] } // Categorías vacías, se llenarán dinámicamente
  };

  // Función para crear el gráfico
  const createChart = async () => {
    if (typeof window !== 'undefined') {
      const { default: ApexCharts } = await import('apexcharts');
      chart1 = new ApexCharts(document.querySelector("#chart3"), chartOptions);
      await chart1.render();
    }
  };

  // Función para obtener los datos de la API
  async function fetchData() {
    try {
      const response = await fetch("https://corsproxy.io/?http://emac.criba.edu.ar/servicios/getHistoryValues.php?station_code=EACC&var_code=23");
      const csvText = await response.text();

      // Parsear el CSV
      const { fechas, valores } = parseCSV(csvText);

      // Actualizar opciones del gráfico
      chartOptions.series[0].data = valores;
      chartOptions.xaxis.categories = fechas;

      // Actualizar el gráfico si ya está creado
      if (chart1) {
        chart1.updateOptions(chartOptions);
      }
    } catch (error) {
      console.error("Error al obtener datos de la API:", error);
    }
  }

  /**
   * Función para parsear el contenido CSV de la API.
   * @param {string} csv
   * @returns {{ fechas: string[], valores: number[] }}
   */
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

<div id="chart3"></div>
