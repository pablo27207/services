<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import { timeFormatLocale } from "d3";

    export let mareographData: { timestamp: string; level: number }[] = [];
    export let tideForecastData: { timestamp: string; level: number }[] = [];

    let svg: SVGSVGElement | null = null;
    let tooltip: HTMLDivElement | null = null;
    let container: HTMLDivElement | null = null;

    const height = 300; //aca modifcamos el tamaño de la altura
    const margin = { top: 20, right: 60, bottom: 40, left: 50 };

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

    const formatoFechaEje = localeEs.format("%a %d");
    const formatoFechaTooltip = localeEs.format("%d/%m/%Y %H:%M");

    onMount(() => {
        if (container) {
            const width = container.clientWidth;
            drawChart(width);
        }
    });

    const drawChart = (width: number) => {
        if (!svg || !tooltip) return;

        const x = d3.scaleTime()
            .domain(d3.extent([...mareographData, ...tideForecastData], d => new Date(d.timestamp)) as [Date, Date])
            .range([margin.left, width - margin.right]);

        const y = d3.scaleLinear()
            .domain([0, d3.max([...mareographData, ...tideForecastData], d => d.level) ?? 1])
            .range([height - margin.bottom, margin.top]);

        const line = d3.line<{ timestamp: string; level: number }>()
            .x(d => x(new Date(d.timestamp)))
            .y(d => y(d.level));

        const svgEl = d3.select(svg)
            .attr("viewBox", `0 0 ${width} ${height}`)
            .attr("preserveAspectRatio", "xMidYMid meet");

        svgEl.selectAll("*").remove();

        const datasets = [
            { data: mareographData, color: "steelblue", label: "mareografo", dashed: false },
            { data: tideForecastData, color: "red", label: "prediccion", dashed: true }
        ];

        datasets.forEach(({ data, color, label, dashed }) => {
            svgEl.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", color)
                .attr("stroke-width", 2)
                .attr("d", line)
                .attr("stroke-dasharray", dashed ? "4,4" : "none")
                .attr("class", `linea-${label}`);
        });

        datasets.forEach(({ data, color, label }) => {
            svgEl.selectAll(`.point-${label}`)
                .data(data)
                .enter().append("circle")
                .attr("cx", d => x(new Date(d.timestamp)))
                .attr("cy", d => y(d.level))
                .attr("r", 4)
                .attr("fill", color)
                .attr("class", `point-${label}`)
                .on("mouseover", (event, d) => {
                    tooltip!.style.display = "block";
                    tooltip!.innerHTML = `
                        📅 ${formatoFechaTooltip(new Date(d.timestamp))}<br>
                        🔹 ${label === "mareografo" ? "Mareógrafo" : "Predicción"}: ${d.level}`;
                    tooltip!.style.top = `${event.offsetY - 30}px`;
                    tooltip!.style.left = `${event.offsetX - 20}px`;
                })
                .on("mouseout", () => tooltip!.style.display = "none");
        });

        // Eje X
        const xAxis = d3.axisBottom(x)
            .tickFormat(formatoFechaEje)
            .ticks(Math.floor(width / 90));

        svgEl.append("g")
            .attr("class", "x-axis")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(xAxis)
            .selectAll("text")
            .attr("transform", "rotate(-45)")
            .style("text-anchor", "end");

        // Eje Y
        svgEl.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));

        // Zoom
        const zoom = d3.zoom()
            .scaleExtent([1, 10])
            .translateExtent([[0, 0], [width, height]])
            .on("zoom", (event) => {
                const newX = event.transform.rescaleX(x);

                const newLine = d3.line<{ timestamp: string; level: number }>()
                    .x(d => newX(new Date(d.timestamp)))
                    .y(d => y(d.level));

                svgEl.select(".x-axis")
                    .call(d3.axisBottom(newX).tickFormat(formatoFechaEje)
                        .ticks(Math.floor(width / 90)))
                    .selectAll("text")
                    .attr("transform", "rotate(-45)")
                    .style("text-anchor", "end");

                svgEl.select(".linea-mareografo").attr("d", newLine(mareographData));
                svgEl.select(".linea-prediccion").attr("d", newLine(tideForecastData));

                svgEl.selectAll(".point-mareografo")
                    .attr("cx", d => newX(new Date(d.timestamp)));

                svgEl.selectAll(".point-prediccion")
                    .attr("cx", d => newX(new Date(d.timestamp)));
            });

        svgEl.call(zoom);

        // Zoom inicial automático a la predicción
       const inicioPrediccion = tideForecastData?.[0]?.timestamp;
if (inicioPrediccion) {
    const prediccionX = x(new Date(inicioPrediccion));
    const centroZoom = (width - margin.left - margin.right) / 2;

    const t = d3.zoomIdentity
        .translate(centroZoom - prediccionX, 0)
        .scale(4); // podés ajustar este valor

    svgEl.call(zoom.transform, t);
}

    };
</script>

<div class="grafico-wrapper" bind:this={container}>
    <svg bind:this={svg}></svg>
    <div bind:this={tooltip} class="tooltip"></div>
</div>

<style>
.grafico-wrapper {
  width: 100%;
  max-width: 100%;
  min-width: 500px;
  height: auto;
  overflow-x: auto;
  position: relative;
  margin-top: 1rem;
}


svg {
    width: 100%;
    height: auto;
    min-height: 400px;
}

.tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 6px 10px;
    border-radius: 5px;
    font-size: 12px;
    display: none;
    pointer-events: none;
    transform: translate(-50%, -120%);
    z-index: 10;
}
</style>
