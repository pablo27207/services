document.addEventListener("DOMContentLoaded", function () {
    const width = 800,
        height = 400,
        margin = { top: 20, right: 30, bottom: 40, left: 50 };

    const svg = d3.select("#chart")
        .attr("width", width)
        .attr("height", height);

    d3.json("/api/mareograph").then(data => {
        if (!data.length) {
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", height / 2)
                .attr("text-anchor", "middle")
                .text("No hay datos disponibles");
            return;
        }

        data.forEach(d => {
            d.timestamp = new Date(d.timestamp); // Convertir a Date
            d.level = +d.level; // Convertir a número
        });

        // Escalas
        const x = d3.scaleTime()
            .domain(d3.extent(data, d => d.timestamp))
            .range([margin.left, width - margin.right]);

        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.level)])
            .range([height - margin.bottom, margin.top]);

        // Ejes
        const xAxis = d3.axisBottom(x).ticks(5);
        const yAxis = d3.axisLeft(y);

        const gX = svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(xAxis);

        const gY = svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(yAxis);

        // Línea
        const line = d3.line()
            .x(d => x(d.timestamp))
            .y(d => y(d.level));

        const path = svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("d", line);

        // Tooltip
        const tooltip = d3.select("body").append("div")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("background", "#fff")
            .style("border", "1px solid #ddd")
            .style("padding", "5px")
            .style("border-radius", "5px");

        svg.selectAll("circle")
            .data(data)
            .enter().append("circle")
            .attr("cx", d => x(d.timestamp))
            .attr("cy", d => y(d.level))
            .attr("r", 4)
            .attr("fill", "steelblue")
            .on("mouseover", (event, d) => {
                tooltip.style("visibility", "visible")
                    .html(`📅 ${d3.utcFormat("%d/%m/%Y %H:%M")(d.timestamp)}<br>🌊 Nivel: ${d.level}m`);
            })
            .on("mousemove", event => {
                tooltip.style("top", (event.pageY - 10) + "px")
                    .style("left", (event.pageX + 10) + "px");
            })
            .on("mouseout", () => tooltip.style("visibility", "hidden"));

        // Zoom & Pan
        const zoom = d3.zoom()
            .scaleExtent([1, 10])
            .translateExtent([[0, 0], [width, height]])
            .on("zoom", zoomed);

        svg.call(zoom);

        function zoomed(event) {
            const newX = event.transform.rescaleX(x);
            gX.call(d3.axisBottom(newX));
            path.attr("d", line.x(d => newX(d.timestamp)));
            svg.selectAll("circle").attr("cx", d => newX(d.timestamp));
        }

        // Slider
        const slider = d3.select("#slider")
            .attr("type", "range")
            .attr("min", 0)
            .attr("max", data.length - 1)
            .attr("value", data.length - 1)
            .on("input", function () {
                const index = this.value;
                const newData = data.slice(0, +index + 1);

                const newX = d3.scaleTime()
                    .domain(d3.extent(newData, d => d.timestamp))
                    .range([margin.left, width - margin.right]);

                gX.call(d3.axisBottom(newX));
                path.datum(newData).attr("d", line.x(d => newX(d.timestamp)));
                svg.selectAll("circle")
                    .data(newData)
                    .attr("cx", d => newX(d.timestamp))
                    .attr("cy", d => y(d.level));
            });
    }).catch(error => {
        console.error("❌ Error al obtener los datos:", error);
    });
});
