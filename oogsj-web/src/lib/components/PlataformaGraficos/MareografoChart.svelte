<script lang="ts">
    import ApexChart from 'svelte-apexcharts';
  
    export let data = [];
  
    let chartOptions = {
      chart: { type: 'line', height: 200 },
      stroke: { curve: 'smooth' },
      xaxis: { categories: [] },
      colors: ["#1E88E5"]
    };
  
    let chartSeries = [
      {
        name: "Nivel del Mar",
        data: []
      }
    ];
  
    function generateSineWave() {
      let points = 100;
      let xValues = Array.from({ length: points }, (_, i) => i);
      let yValues = xValues.map(x => Math.sin(x * 0.1) * 1.5 + 1.5);
  
      chartOptions = { ...chartOptions, xaxis: { categories: xValues } };
      chartSeries = [{ name: "Nivel del Mar", data: yValues }];
    }
  
    $: generateSineWave();
  </script>
  
  <div class="chart-container">
    <ApexChart type="line" options={chartOptions} series={chartSeries} height="200" />
  </div>
  
  <style>
    .chart-container {
      width: 100%;
      height: 250px;
      margin-top: 10px;
    }
  </style>
  