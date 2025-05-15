<script>
  import { onMount, tick } from 'svelte';
  import * as d3 from 'd3';
  import { timeFormatLocale } from 'd3';
  import { onDestroy } from 'svelte';

  let resizeObserver;


  export let data = [];
  export let label = '';
  export let color = 'steelblue';
  export let height = 300;

  const margin = { top: 20, right: 30, bottom: 40, left: 50 };

  let svgContainer;
  let tooltip;
  let chartCard;

  const localeEs = timeFormatLocale({
    dateTime: "%A, %e de %B de %Y, %X",
    date: "%d/%m/%Y",
    time: "%H:%M:%S",
    periods: ["AM", "PM"],
    days: ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"],
    shortDays: ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"],
    months: ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    shortMonths: ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
  });

 onMount(async () => {
  await tick(); // Espera que el DOM esté visible
  tooltip = d3.select(`#tooltip-${label.replace(/\s+/g, '-')}`);
  drawChart();

  // Redibuja cuando el contenedor cambia de tamaño
  resizeObserver = new ResizeObserver(() => {
    drawChart();
  });
  if (chartCard) resizeObserver.observe(chartCard);

  // Redibuja cuando la ventana cambia de tamaño
  window.addEventListener("resize", drawChart);
});



  function drawChart() {
    const width = chartCard.clientWidth;

    const svg = d3.select(svgContainer)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .html("");

    if (!data?.length) {
      svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .text("No hay datos disponibles");
      return;
    }

    data.forEach(d => {
      d.timestamp = new Date(d.timestamp);
      d.value = parseFloat(d.value);
    });

    const filteredData = data.filter(d => !isNaN(d.value));

    const x = d3.scaleTime()
      .domain(d3.extent(filteredData, d => d.timestamp))
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(filteredData, d => d.value) || 1])
      .range([height - margin.bottom, margin.top]);

    const format = localeEs.format("%a %d");

    // Ejes
    svg.append("g")
      .attr("class", "x-axis")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickFormat(format));

    svg.append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

    // Línea
    svg.append("path")
      .datum(filteredData)
      .attr("class", "line-path")
      .attr("fill", "none")
      .attr("stroke", color)
      .attr("stroke-width", 2)
      .attr("d", d3.line()
        .x(d => x(d.timestamp))
        .y(d => y(d.value)));

    // Puntos
    svg.selectAll("circle")
      .data(filteredData)
      .enter().append("circle")
      .attr("cx", d => x(d.timestamp))
      .attr("cy", d => y(d.value))
      .attr("r", 4)
      .attr("fill", color)
      .on("mouseover", (event, d) => {
        tooltip
          .style("display", "block")
          .html(`📅 ${localeEs.format("%d/%m/%Y")(d.timestamp)}<br>🔹 ${label}: ${d.value}`);
      })
      .on("mousemove", event => {
        const bounds = chartCard.getBoundingClientRect();
        tooltip
          .style("left", `${event.clientX - bounds.left + 10}px`)
          .style("top", `${event.clientY - bounds.top - 40}px`);
      })
      .on("mouseout", () => {
        tooltip.style("display", "none");
      });

    // Zoom
    const zoom = d3.zoom()
      .scaleExtent([1, 10])
      .translateExtent([[0, 0], [width, height]])
      .on("zoom", (event) => {
        const newX = event.transform.rescaleX(x);
        const newLine = d3.line()
          .x(d => newX(d.timestamp))
          .y(d => y(d.value));

        svg.select(".x-axis").call(d3.axisBottom(newX).tickFormat(format));
        svg.select(".line-path").attr("d", newLine(filteredData));
        svg.selectAll("circle").attr("cx", d => newX(d.timestamp));
      });

    svg.call(zoom);
  }

  onDestroy(() => {
  if (resizeObserver) resizeObserver.disconnect();
  window.removeEventListener("resize", drawChart);
});

</script>

<div bind:this={chartCard} class="grafico-card">
  <svg bind:this={svgContainer}></svg>
  <div
    class="tooltip"
    id={"tooltip-" + label.replace(/\s+/g, '-')}
  ></div>
</div>

<style>
  .grafico-card {
  width: 100%;
  min-width: 600px; /* 👈 Asegura que el gráfico no quede demasiado angosto */
  position: relative;
  padding: 0.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}


  svg {
    width: 100%;
    height: auto;
    display: block;
  }

  .tooltip {
    position: absolute;
    display: none;
    background: #fff;
    border: 1px solid #ccc;
    padding: 6px;
    pointer-events: none;
    font-size: 0.85rem;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    z-index: 9999;
  }
</style>
