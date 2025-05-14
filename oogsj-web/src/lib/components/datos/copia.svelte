<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    
  
    let tooltip;
  
    
    const width = 600;
  const height = 200;
  
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  
    const buoyVariables = {
      "Altura de Olas": "altura_olas_chart",
      "Periodo de Olas": "periodo_olas_chart",
      "Dirección de Olas": "direccion_olas_chart",
      "Velocidad de Corriente": "velocidad_corriente_chart",
      "Dirección de la Corriente": "direccion_corriente_chart",
      "Radiación PAR": "radiacion_par_chart",
      "Batería": "bateria_chart"
    };
  
    onMount(async () => {
      tooltip = d3.select("#tooltip");
      const data = await d3.json('/api/buoy');
      Object.entries(buoyVariables).forEach(([key, id]) => {
        if (key.includes("Dirección")) {
          plotPolarGraph(id, data[key], key);
        } else {
          plotGraph(id, [data[key]], [key], ["steelblue"]);
        }
      });
    });
  
    function plotGraph(svgId, datasets, labels, colors) {
      const svg = d3.select(`#${svgId}`)
        .attr("width", width)
        .attr("height", height)
        .html("");
  
      if (!datasets.length || !datasets[0].length) {
        svg.append("text")
          .attr("x", width / 2)
          .attr("y", height / 2)
          .attr("text-anchor", "middle")
          .text("No hay datos disponibles");
        return;
      }
  
      datasets.forEach(data => {
        data.forEach(d => {
          d.timestamp = new Date(d.timestamp);
          d.value = parseFloat(d.value);
          if (isNaN(d.value)) d.value = null;
        });
      });
  
      datasets = datasets.map(data => data.filter(d => d.value !== null));
  
      const x = d3.scaleTime()
        .domain(d3.extent(datasets.flat(), d => d.timestamp))
        .range([margin.left, width - margin.right]);
  
      const y = d3.scaleLinear()
        .domain([0, d3.max(datasets.flat(), d => d.value) || 1])
        .range([height - margin.bottom, margin.top]);
  
      const xAxis = d3.axisBottom(x).ticks(5);
      const yAxis = d3.axisLeft(y);
  
      const gX = svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(xAxis);
  
      svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(yAxis);
  
      const paths = datasets.map((data, i) =>
        svg.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", colors[i])
          .attr("stroke-width", 2)
          .attr("d", d3.line()
            .x(d => x(d.timestamp))
            .y(d => y(d.value)))
      );
  
      const points = datasets.map((data, i) =>
    svg.selectAll(`.circle-${i}`)
      .data(data)
      .enter().append("circle")
      .attr("class", `circle-${i}`)
      .attr("cx", d => x(d.timestamp))
      .attr("cy", d => y(d.value))
      .attr("r", 4)
      .attr("fill", colors[i])
      .on("mouseover", function(event, d) {
        tooltip
          .style("display", "block")
          .html(`📅 ${d3.utcFormat("%d/%m/%Y %H:%M")(d.timestamp)}<br>🔹 ${labels[i]}: ${d.value}`);
      })
      .on("mousemove", function(event) {
        tooltip
          .style("left", `${event.pageX + 10}px`)
          .style("top", `${event.pageY - 40}px`);
      })
      .on("mouseout", function() {
        tooltip.style("display", "none");
      })
  );
  
  
  
  
      svg.call(d3.zoom()
        .scaleExtent([1, 10])
        .translateExtent([[0, 0], [width, height]])
        .on("zoom", event => {
          const newX = event.transform.rescaleX(x);
          gX.call(d3.axisBottom(newX));
          paths.forEach(path =>
            path.attr("d", d3.line()
              .x(d => newX(d.timestamp))
              .y(d => y(d.value)))
          );
          points.forEach(p =>
            p.attr("cx", d => newX(d.timestamp))
          );
        }));
    }
  
    function plotPolarGraph(svgId, data, label) {
      const size = 350, margin = 50, radius = size / 2 - margin;
  
      // Seleccionar el contenedor SVG y centrarlo bien
      const svg = d3.select(`#${svgId}`)
        .attr("width", size)
        .attr("height", size)
        .style("display", "block")  // Evita problemas con el inline-block de SVG
        .style("margin", "0 auto")  // Centra horizontalmente
        .html("")
        .append("g")
        .attr("transform", `translate(${size / 2},${size / 2})`); // Centra el gráfico en el SVG
  
      // Mensaje si no hay datos
      if (!data || !data.length) {
        svg.append("text")
          .attr("text-anchor", "middle")
          .attr("dy", "0.35em")
          .text("No hay datos disponibles");
        return;
      }
  
      // Convertir y filtrar datos
      data.forEach(d => {
          d.timestamp = new Date(d.timestamp);
          d.value = parseFloat(d.value);
          if (isNaN(d.value)) d.value = null;
      });
  
      data = data.filter(d => d.value !== null);
  
      // Crear bins (grupos de datos en intervalos de 10°)
      const binSize = 10;
      const bins = d3.range(0, 360 + binSize, binSize).map(d => ({ angle: d, count: 0 }));
  
      // Contar ocurrencias en cada intervalo
      data.forEach(d => {
          const idx = Math.floor(d.value / binSize);
          bins[idx].count += 1;
      });
  
      // Escalas
      const angleScale = d3.scaleLinear()
          .domain([0, 360])
          .range([0, 2 * Math.PI]);
  
      const rScale = d3.scaleLinear()
          .domain([0, d3.max(bins, d => d.count) || 1])
          .range([0, radius]);
  
      // Crear arcos (sectores del gráfico)
      const arc = d3.arc()
          .innerRadius(0)
          .outerRadius(d => rScale(d.count))
          .startAngle(d => angleScale(d.angle))
          .endAngle(d => angleScale(d.angle + binSize))
          .padAngle(0.01)
          .padRadius(0.01);
  
      // Dibujar el gráfico polar
      svg.selectAll("path")
          .data(bins)
          .enter().append("path")
          .attr("d", arc)
          .attr("fill", "steelblue")
          .attr("stroke", "white")
          .attr("opacity", 0.8);
  
      // Líneas de dirección (cada 45°)
      svg.selectAll(".angle-line")
          .data(d3.range(0, 360, 45))
          .enter().append("line")
          .attr("x1", 0)
          .attr("y1", 0)
          .attr("x2", d => rScale(d3.max(bins, d => d.count)) * Math.cos(angleScale(d)))
          .attr("y2", d => rScale(d3.max(bins, d => d.count)) * Math.sin(angleScale(d)))
          .attr("stroke", "#999")
          .attr("stroke-width", 1);
  
      // Etiquetas de dirección
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
  
  <style>
    #tooltip {
    position: absolute;
    background: white;
    padding: 6px 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.85rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    pointer-events: none;
    display: none;
    z-index: 9999; /* 🔥 muy por encima de todo */
  }
  
  
    .charts {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    padding: 1rem;
    
  }
  
  .chart-card {
    
    background: #fff;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center; /* Centra los gráficos horizontalmente */
    justify-content: center; /* Centra el contenido si es necesario */
  
    
  }
    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }
  
    .chart-header h3 {
      margin: 0;
    }
  
    .info-wrapper {
      position: relative;
    }
  
    .info-button {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 1.2rem;
    }
  
    .info-tooltip {
      display: none;
      position: absolute;
      top: 130%;
      left: 50%;
      transform: translateX(-50%);
      background: #f1f1f1;
      color: #333;
      padding: 0.6rem;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 0.85rem;
      width: 220px;
      z-index: 5;
    }
  
    .info-wrapper:hover .info-tooltip {
      display: block;
    }
  
    /* .download-button {
      background: none;
      border: none;
      font-size: 1.2rem;
      cursor: pointer;
    } */
  
    svg {
    width: 100% !important;
    height: auto !important;
    max-height: 600px;
    display: block;
    margin:  auto;
    background: #f9f9f9;
    border-radius: 8px;
    
  }
  </style>
  
  <div id="tooltip"></div>
  <div class="charts">
    {#each Object.entries(buoyVariables) as [label, id]}
      <div class="chart-card">
        <div class="chart-header">
          <h3>{label}</h3>
          <div class="info-wrapper">
            <button class="info-button">ℹ️</button>
            <div class="info-tooltip">
              Explicación sobre {label}. Aquí podés poner cómo se interpreta esta variable.
            </div>
          </div>
          <!-- <button class="download-button" on:click={() => downloadChart(id, label)}>📥</button> -->
        </div>
        <svg id={id}></svg>
      </div>
    {/each}
  </div>
  
  
  
  
  
  
  