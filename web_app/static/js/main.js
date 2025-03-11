document.addEventListener("DOMContentLoaded", function () {
    const width = 800,
        height = 400,
        margin = { top: 20, right: 30, bottom: 40, left: 50 };

    const variables = [
        { id: "mareograph_chart", api: "/api/mareograph", key: "level", label: "Nivel del Mareógrafo" },
        { id: "tide_forecast_chart", api: "/api/tide_forecast", key: "level", label: "Nivel de Marea Estimada" },
        { id: "altura_olas_chart", api: "/api/buoy", key: "altura_olas", label: "Altura de Olas" },
        { id: "periodo_olas_chart", api: "/api/buoy", key: "periodo_olas", label: "Período de Olas" },
        { id: "direccion_olas_chart", api: "/api/buoy", key: "direccion_olas", label: "Dirección de Olas" },
        { id: "velocidad_corriente_chart", api: "/api/buoy", key: "velocidad_corriente", label: "Velocidad de la Corriente" },
        { id: "direccion_corriente_chart", api: "/api/buoy", key: "direccion_corriente", label: "Dirección de la Corriente" },
        { id: "radiacion_par_chart", api: "/api/buoy", key: "radiacion_par", label: "Radiación PAR" },
        { id: "bateria_chart", api: "/api/buoy", key: "bateria", label: "Batería" }
    ];


    function plotGraph(svgId, data, label) {
        const svg = d3.select("#" + svgId)
            .attr("width", width)
            .attr("height", height)
            .html("");  // Limpiar contenido previo
    
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
            if (d.value !== null && !isNaN(d.value)) {
                d.value = +d.value; // Convertir a número
            } else {
                d.value = d.level;
            }
        });
    
        // Escalas
        const x = d3.scaleTime()
            .domain(d3.extent(data, d => d.timestamp))
            .range([margin.left, width - margin.right]);
    
        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
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
            .y(d => y(d.value));
    
        const path = svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("d", line);
    
        // Tooltip
        const tooltip = d3.select("#tooltip");
    
        const points = svg.selectAll("circle")
            .data(data)
            .enter().append("circle")
            .attr("cx", d => x(d.timestamp))
            .attr("cy", d => y(d.value))
            .attr("r", 4)
            .attr("fill", "steelblue")
            .on("mouseover", (event, d) => {
                tooltip.style("display", "block")
                    .html(`📅 ${d3.utcFormat("%d/%m/%Y %H:%M")(d.timestamp)}<br>🔹 ${label}: ${d.value}`);
            })
            .on("mousemove", event => {
                tooltip.style("top", (event.pageY - 10) + "px")
                    .style("left", (event.pageX + 10) + "px");
            })
            .on("mouseout", () => tooltip.style("display", "none"));
    
        // Zoom & Pan
        const zoom = d3.zoom()
            .scaleExtent([1, 10])  // Permitir hacer zoom entre 1x y 10x
            .translateExtent([[0, 0], [width, height]])  // Restringir el área de zoom
            .on("zoom", zoomed);
    
        svg.call(zoom);
    
        function zoomed(event) {
            const newX = event.transform.rescaleX(x);
            gX.call(d3.axisBottom(newX));
            path.attr("d", line.x(d => newX(d.timestamp)));
            points.attr("cx", d => newX(d.timestamp));
        }
    }
    

    variables.forEach(variable => {
        d3.json(variable.api).then(data => {
            if (variable.id === "mareograph_chart" || variable.id === "tide_forecast_chart") {
                plotGraph(variable.id, data, variable.label);
            } else if (data[variable.key]) {
                plotGraph(variable.id, data[variable.key], variable.label);
            } else {
                console.warn(`❌ No se encontraron datos para ${variable.label}`);
            }
        }).catch(error => {
            console.error(`❌ Error al obtener los datos de ${variable.label}:`, error);
        });
    });
});
