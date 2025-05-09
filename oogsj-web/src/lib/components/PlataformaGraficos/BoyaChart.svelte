<script lang="ts">
    import ApexChart from 'svelte-apexcharts';
  
    export let variables = [];
  
    let chartOptions = {
      chart: { type: 'line', height: 200 },
      stroke: { curve: 'smooth' },
      xaxis: { categories: [] }
    };
  
    function generateData(variable) {
      let points = 50;
      let xValues = Array.from({ length: points }, (_, i) => i);
      let yValues = xValues.map(x => Math.sin(x * 0.1) * Math.random() * 2);
  
      return {
        name: variable.nombre,
        data: yValues
      };
    }
  
    let chartSeries = variables.map(variable => generateData(variable));
  </script>
  
  <div class="chart-container">
    {#each chartSeries as series}
      <ApexChart type="line" options={chartOptions} series={[series]} height="200" />
    {/each}
  </div>
  
  <style>
    .chart-container {
      width: 100%;
      height: auto;
      margin-top: 10px;
    }
  </style>
  