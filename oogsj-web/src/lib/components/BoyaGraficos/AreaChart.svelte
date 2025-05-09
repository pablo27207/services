<script lang="ts">
    import { onMount } from 'svelte';
  
    let chartDonut: ApexCharts | null = null;
  
    // Datos para el gráfico de dona
    let chartOptions = {
      chart: {
        type: 'donut',  // Cambiado a 'donut' para crear un gráfico de dona
        height: 350,
        zoom: {
          enabled: false
        }
      },
      dataLabels: {
        enabled: true,  // Habilitado para mostrar etiquetas dentro de la dona
        style: {
          fontSize: '16px',
          fontWeight: 'bold'
        }
      },
      stroke: {
        width: 0
      },
      labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
      series: [35, 55, 75, 90, 120, 140, 135, 160, 180, 200, 230, 250],  // Ejemplo de datos, puedes ajustarlos
      title: {
        text: 'Iradiación Solar Horizontal',
        align: 'center',
      },
      fill: {
        type: 'gradient',
        gradient: {
          opacityFrom: 0.7,
          opacityTo: 0.2,
        },
      },
    };
  
    const createChart = async () => {
      if (typeof window !== 'undefined') {
        const { default: ApexCharts } = await import('apexcharts');
        chartDonut = new ApexCharts(document.querySelector("#chartDonut"), chartOptions);
        chartDonut.render();
      }
    };
  
    onMount(() => {
      createChart();
    });
  </script>
  
  <style>
    #chartDonut {
      width: 100%;
      height: 350px; /* Asegúrate de que el contenedor tenga un tamaño adecuado */
    }
  </style>
  
  <div id="chartDonut"></div>
  