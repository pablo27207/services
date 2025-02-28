document.addEventListener("DOMContentLoaded", function() {
    const width = 800, height = 400, margin = { top: 20, right: 30, bottom: 40, left: 50 };

    const svg = d3.select("#chart")
        .attr("width", width)
        .attr("height", height);

    d3.json("/api/mareograph").then(data => {
        console.log("📊 Datos obtenidos:", data); 

        if (!data.length) {
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", height / 2)
                .attr("text-anchor", "middle")
                .text("No hay datos disponibles");
            return;
        }

        // ✅ Convertir fecha correctamente
        data.forEach(d => {
            d.timestamp = new Date(d.timestamp); // <-- Convertimos RFC 2822 a Date()
            d.level = +d.level; // Convertir a número
        });

        console.log("📅 Fechas convertidas:", data.map(d => d.timestamp)); 
        console.log("📈 Niveles convertidos:", data.map(d => d.level)); 

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

        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(xAxis);

        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(yAxis);

        // Línea
        const line = d3.line()
            .x(d => x(d.timestamp))
            .y(d => y(d.level));

        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("d", line);
    }).catch(error => {
        console.error("❌ Error al obtener los datos:", error);
    });
});
