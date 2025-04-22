document.addEventListener("DOMContentLoaded", function () {

    const apiEndpoints = {
        mareograph: "/api/mareograph",
        tide_forecast: "/api/tide_forecast",
        buoy: "/api/buoy"
    };

    const buoyVariables = {
        "Altura de Olas": "altura_olas_chart",
        "Periodo de Olas": "periodo_olas_chart",
        "Dirección de Olas": "direccion_olas_chart",
        "Velocidad de Corriente": "velocidad_corriente_chart",
        "Dirección de la Corriente": "direccion_corriente_chart",
        "Radiación PAR": "radiacion_par_chart",
        "Batería": "bateria_chart"
    };

    function plotGraph(svgId, datasets, labels, colors, isTide = false) {
        const svgElement = document.getElementById(svgId);
        const width = svgElement?.clientWidth || 800;
        const height = svgElement?.clientHeight || 400;
        const margin = { top: 20, right: 30, bottom: 40, left: 50 };
        const svg = d3.select("#" + svgId)
            .attr("width", width)
            .attr("height", height)
            .html("");  // Limpiar contenido previo
    
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
        
                const valorOriginal = isTide ? d.level : d.value;
                const valorParseado = parseFloat(valorOriginal);
        
                d.value = isNaN(valorParseado) ? null : valorParseado;
            });
        });
        
        datasets = datasets.map(data => data.filter(d => d.value !== null));
        
        // Escalas
        const x = d3.scaleTime()
            .domain(d3.extent(datasets.flat(), d => d.timestamp))
            .range([margin.left, width - margin.right]);
    
        const y = d3.scaleLinear()
            .domain([0, d3.max(datasets.flat(), d => d.value) || 1])
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
    
        // Líneas
        const paths = datasets.map((data, i) => 
            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", colors[i])
                .attr("stroke-width", 2)
                .attr("d", d3.line()
                    .x(d => x(d.timestamp))
                    .y(d => y(d.value))
                )
        );
    
        // Tooltip
        const tooltip = d3.select("#tooltip");
    
        const points = datasets.map((data, i) =>
            svg.selectAll(`circle-${i}`)
                .data(data)
                .enter().append("circle")
                .attr("cx", d => x(d.timestamp))
                .attr("cy", d => y(d.value))
                .attr("r", 4)
                .attr("fill", colors[i])
                .on("mouseover", (event, d) => {
                    tooltip.style("display", "block")
                        .html(`📅 ${d3.utcFormat("%d/%m/%Y %H:%M")(d.timestamp)}<br>🔹 ${labels[i]}: ${d.value}`);
                })
                .on("mousemove", event => {
                    tooltip.style("top", (event.pageY - 10) + "px")
                        .style("left", (event.pageX + 10) + "px");
                })
                .on("mouseout", () => tooltip.style("display", "none"))
        );
    
        // Zoom & Pan
        const zoom = d3.zoom()
            .scaleExtent([1, 10])
            .translateExtent([[0, 0], [width, height]])
            .on("zoom", event => {
                const newX = event.transform.rescaleX(x);
                gX.call(d3.axisBottom(newX));
    
                paths.forEach(path => 
                    path.attr("d", d3.line()
                        .x(d => newX(d.timestamp))
                        .y(d => y(d.value))
                    )
                );
    
                points.forEach(point => 
                    point.attr("cx", d => newX(d.timestamp))
                );
            });
    
        svg.call(zoom);
    }
    
    

    function plotPolarGraph(svgId, data, label) {
        const svgElement = document.getElementById(svgId);
        const width = svgElement?.clientWidth || 400;
        const height = svgElement?.clientHeight || 400;
        const margin = 50;
        const radius = Math.min(width, height) / 2 - margin;
    
        // Establecer tamaño directamente sobre el elemento SVG
        svgElement.setAttribute("width", width);
        svgElement.setAttribute("height", height);
    
        const svg = d3.select("#" + svgId)
            .html("") // Limpiar el SVG
            .append("g")
            .attr("transform", `translate(${width / 2}, ${height / 2})`);
    
        if (!data || !data.length) {
            svg.append("text")
                .attr("text-anchor", "middle")
                .text("No hay datos disponibles");
            return;
        }
    
        // Convertir y filtrar datos válidos
        data.forEach(d => {
            d.timestamp = new Date(d.timestamp);
            d.value = parseFloat(d.value);
            if (isNaN(d.value)) d.value = null;
        });
    
        data = data.filter(d => d.value !== null);
    
        // Agrupar en intervalos de 10 grados
        const binSize = 10;
        const bins = d3.range(0, 360 + binSize, binSize).map(d => ({ angle: d, count: 0 }));
    
        data.forEach(d => {
            const binIndex = Math.floor(d.value / binSize);
            bins[binIndex].count += 1;
        });
    
        const angleScale = d3.scaleLinear().domain([0, 360]).range([0, 2 * Math.PI]);
        const rScale = d3.scaleLinear().domain([0, d3.max(bins, d => d.count) || 1]).range([0, radius]);
    
        const arc = d3.arc()
            .innerRadius(0)
            .outerRadius(d => rScale(d.count))
            .startAngle(d => angleScale(d.angle))
            .endAngle(d => angleScale(d.angle + binSize));
    
        svg.selectAll("path")
            .data(bins)
            .enter().append("path")
            .attr("d", arc)
            .attr("fill", "steelblue")
            .attr("stroke", "white")
            .attr("stroke-width", 1)
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
    

    Promise.all([
        fetch(apiEndpoints.mareograph).then(r => r.text()),
        fetch(apiEndpoints.tide_forecast).then(r => r.text())
    ]).then(([mareographText, tideText]) => {
    
        // Corrigiendo JSON inválido antes de parsearlo
        const fixNaN = texto => JSON.parse(texto.replace(/\bNaN\b/g, 'null'));
    
        const mareographData = fixNaN(mareographText);
        const tideData = fixNaN(tideText);
    
        plotGraph(
            "mareograph_chart",
            [mareographData, tideData],
            ["Mareógrafo", "Predicción de Marea"],
            ["steelblue", "red"],
            true
        );
    
    }).catch(err => console.error("Error:", err));
    

// Obtener datos de la boya y graficar cada variable correctamente
    d3.json(apiEndpoints.buoy).then(buoyData => {
        Object.keys(buoyVariables).forEach(variable => {
            if (variable === "Dirección de Olas" || variable === "Dirección de la Corriente") {
                plotPolarGraph(buoyVariables[variable], buoyData[variable], variable);
            } else {
                plotGraph(buoyVariables[variable], [buoyData[variable]], [variable], ["steelblue"]);
            }
        });
    }).catch(error => {
        console.error("Error al obtener los datos de la boya:", error);
    }); 
});
function forzarActualizacion(taskName) {
    const statusDiv = document.getElementById("estado-actualizacion");
    statusDiv.innerText = `Enviando solicitud de actualización para "${taskName}"...`;

    fetch(`/update/${taskName}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            statusDiv.innerText = `${taskName}: ${data.status} (ID: ${data.task_id})`;
        } else {
            statusDiv.innerText = `Error: ${JSON.stringify(data)}`;
        }
    })
    .catch(err => {
        statusDiv.innerText = ` Error al actualizar "${taskName}": ${err}`;
    });
}
function actualizarEstadoBackend() {
    fetch("/status")
      .then(res => {
        if (!res.ok) throw new Error("Respuesta no válida");
        return res.json();
      })
      .then(status => {
        document.getElementById("estado-db").innerText =
          status.database === "ok" ? "✔ OK" : "❌ Error";
        document.getElementById("estado-db").className =
          status.database === "ok" ? "text-green-600 font-bold" : "text-red-600 font-bold";
  
        document.getElementById("estado-celery").innerText =
          status.celery === "ok" ? "✔ OK" : "❌ Error";
        document.getElementById("estado-celery").className =
          status.celery === "ok" ? "text-green-600 font-bold" : "text-red-600 font-bold";
  
        document.getElementById("estado-redis").innerText =
          status.redis === "ok" ? "✔ OK" : "❌ Error";
        document.getElementById("estado-redis").className =
          status.redis === "ok" ? "text-green-600 font-bold" : "text-red-600 font-bold";
  
        const lista = document.getElementById("lista-tareas");
        lista.innerHTML = ""; // Limpiar anterior
  
        for (const [task, fecha] of Object.entries(status.last_runs)) {
          const li = document.createElement("li");
          li.textContent = `${task}: ${fecha || "❌ Sin ejecución reciente"}`;
          li.className = fecha ? "text-gray-700" : "text-red-600";
          lista.appendChild(li);
        }
      })
      .catch(err => {
        console.error("❌ Error al consultar /status", err);
        // Opción: mostrar mensaje de error visual
      });
  }
  
  // Llamar al cargar la página
  document.addEventListener("DOMContentLoaded", actualizarEstadoBackend);
  
  // Y cada 60 segundos para monitoreo activo
  setInterval(actualizarEstadoBackend, 60000);
  