<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import { timeFormatLocale } from "d3";

    export let mareographData: { timestamp: string; level: number }[] = [];
    export let tideForecastData: { timestamp: string; level: number }[] = [];

    let svg: SVGSVGElement | null = null;
    let tooltip: HTMLDivElement | null = null;

    const width = 600, height = 300;
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

    onMount(() => drawChart());

    const drawChart = () => {
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

        d3.select(svg).selectAll("*").remove();

        const svgEl = d3.select(svg)
            .attr("width", width)
            .attr("height", height);

        const datasets = [
            { data: mareographData, color: "steelblue", label: "Mareógrafo", dashed: false },
            { data: tideForecastData, color: "red", label: "Predicción-de-Marea", dashed: true }
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
                    tooltip!.innerHTML = `📅 ${formatoFechaTooltip(new Date(d.timestamp))}<br> 🔹 ${label.replace(/-/g, " ")}: ${d.level}`;
                    const { offsetX, offsetY } = event;
                    tooltip!.style.top = `${offsetY - 30}px`;
                    tooltip!.style.left = `${offsetX - 20}px`;
                })
                .on("mouseout", () => tooltip!.style.display = "none");
        });

        svgEl.append("g")
            .attr("class", "x-axis")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x).tickFormat(formatoFechaEje));

        svgEl.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));

        const zoom = d3.zoom()
            .scaleExtent([1, 10])
            .translateExtent([[0, 0], [width, height]])
            .on("zoom", (event) => {
                const newX = event.transform.rescaleX(x);

                const newLine = d3.line<{ timestamp: string; level: number }>()
                    .x(d => newX(new Date(d.timestamp)))
                    .y(d => y(d.level));

                svgEl.select(".x-axis").call(d3.axisBottom(newX).tickFormat(formatoFechaEje));

                svgEl.select(".linea-Mareógrafo").attr("d", newLine(mareographData));
                svgEl.select(".linea-Predicción-de-Marea").attr("d", newLine(tideForecastData));

                svgEl.selectAll(".point-Mareógrafo")
                    .attr("cx", d => newX(new Date(d.timestamp)));

                svgEl.selectAll(".point-Predicción-de-Marea")
                    .attr("cx", d => newX(new Date(d.timestamp)));
            });

        svgEl.call(zoom);
    };
</script>

<svg bind:this={svg}></svg>
<div bind:this={tooltip} class="tooltip"></div>

<style>
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
    }
</style>
