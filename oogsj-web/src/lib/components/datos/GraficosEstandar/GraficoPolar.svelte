<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    export let data = [];
    export let label = '';
    export let size = 350;
  
    const margin = 50;
    const radius = size / 2 - margin;
  
    let svgContainer;
  
    onMount(() => {
      drawPolarGraph();
    });
  
    function drawPolarGraph() {
      const svg = d3.select(svgContainer)
        .attr("width", size)
        .attr("height", size)
        .style("display", "block")
        .style("margin", "0 auto")
        .html("")
        .append("g")
        .attr("transform", `translate(${size / 2},${size / 2})`);
  
      if (!data?.length) {
        svg.append("text")
          .attr("text-anchor", "middle")
          .attr("dy", "0.35em")
          .text("No hay datos disponibles");
        return;
      }
  
      data.forEach(d => {
        d.timestamp = new Date(d.timestamp);
        d.value = parseFloat(d.value);
      });
  
      const filteredData = data.filter(d => !isNaN(d.value));
  
      const binSize = 10;
      const bins = d3.range(0, 360 + binSize, binSize).map(d => ({ angle: d, count: 0 }));
  
      filteredData.forEach(d => {
        const idx = Math.floor(d.value / binSize);
        bins[idx].count += 1;
      });
  
      const angleScale = d3.scaleLinear()
        .domain([0, 360])
        .range([0, 2 * Math.PI]);
  
      const rScale = d3.scaleLinear()
        .domain([0, d3.max(bins, d => d.count) || 1])
        .range([0, radius]);
  
      const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(d => rScale(d.count))
        .startAngle(d => angleScale(d.angle))
        .endAngle(d => angleScale(d.angle + binSize))
        .padAngle(0.01);
  
      svg.selectAll("path")
        .data(bins)
        .enter().append("path")
        .attr("d", arc)
        .attr("fill", "steelblue")
        .attr("stroke", "white")
        .attr("opacity", 0.8);
  
      svg.selectAll(".angle-line")
        .data(d3.range(0, 360, 45))
        .enter().append("line")
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", d => rScale(d3.max(bins, d => d.count)) * Math.cos(angleScale(d)))
        .attr("y2", d => rScale(d3.max(bins, d => d.count)) * Math.sin(angleScale(d)))
        .attr("stroke", "#999")
        .attr("stroke-width", 1);
  
      svg.selectAll(".angle-label")
        .data(d3.range(0, 360, 45))
        .enter().append("text")
        .attr("x", d => (radius + 10) * Math.cos(angleScale(d)))
        .attr("y", d => (radius + 10) * Math.sin(angleScale(d)))
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("font-size", "10px")
        .attr("fill", "#333")
        .text(d => `${d}°`);
    }
  </script>
  
  <svg bind:this={svgContainer}></svg>
  