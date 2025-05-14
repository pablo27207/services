<script lang="ts">
    import { onMount, onDestroy, afterUpdate } from 'svelte';
    
    let chart2: ApexCharts | null = null;
    let chartOptions = {
      chart: {
        type: 'bar',
        height: 350
      },
      series: [
        {
          name: 'Temperatura',
          data: [20, 35, 25, 30, 40]  // Mínimo de Temperatura
        },
        {
          name: 'Temperatura Máxima',
          data: [25, 38, 32, 36, 45]  // Máximo de Temperatura
        }
      ],
      xaxis: {
        categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']  // Meses
      },
      yaxis: {
        title: {
          text: 'Temperatura (°C)'
        }
      },
      title: {
        text: 'Factores Ambientales:',
        align: 'center'
      }
    };
  
    // Función para crear el gráfico
    const createChart = async () => {
      if (typeof window !== 'undefined') {
        const { default: ApexCharts } = await import('apexcharts');
        chart2 = new ApexCharts(document.querySelector("#barra1"), chartOptions);
        chart2.render();
      }
    };
  
    // En el montaje inicial
    onMount(() => {
      createChart();
    });
  
    // Cuando el componente se actualiza (cualquier cambio)
    afterUpdate(() => {
      if (chart2) {
        chart2.updateOptions(chartOptions);
      }
    });
  
    // En el desmontaje
   // onDestroy(() => {
     // if (chart2) chart2.destroy();
    //});
  </script>
  
  <div id="barra1"></div>
  