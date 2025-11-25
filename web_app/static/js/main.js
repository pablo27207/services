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

    // Mapeo correcto basado en los nombres de variables en la BD (v.name)
    const puertoVariables = {
        "Temperatura Exterior": "puerto_temp_chart",
        "Velocidad del Viento": "puerto_wind_chart",
        "Presión Barométrica": "puerto_pressure_chart",
        "Humedad Exterior": "puerto_hum_chart"
    };

    const muelleVariables = {
        "Temp Out": "muelle_temp_chart",
        "Velocidad del Viento": "muelle_wind_chart",
        "Dirección del Viento": "muelle_wind_dir_chart",
        "Bar": "muelle_pressure_chart",
        "Punto de Rocío": "muelle_dew_chart",
        "Wind Chill": "muelle_chill_chart",
        "Índice de Calor": "muelle_heat_chart",
        "Tasa de Lluvia": "muelle_rain_chart"
    };

    // Configuración de unidades y conversiones (Imperial -> Métrico)
    const variableSettings = {
        // Temperatura (Ya viene en °C)
        "Temperatura Exterior": { unit: "°C", convert: val => val },

        // Temperatura Muelle CC (Viene en F -> Convertir a C)
        "Temp Out": { unit: "°C", convert: val => (val - 32) * 5 / 9, startAtZero: false },
        "Sensación Térmica": { unit: "°C", convert: val => (val - 32) * 5 / 9, startAtZero: false },
        "Wind Chill": { unit: "°C", convert: val => (val - 32) * 5 / 9, startAtZero: false },
        "Índice de Calor": { unit: "°C", convert: val => (val - 32) * 5 / 9, startAtZero: false },
        "Punto de Rocío": { unit: "°C", convert: val => (val - 32) * 5 / 9, startAtZero: false },

        // Velocidad (Ya viene en km/h)
        "Velocidad del Viento": { unit: "km/h", convert: val => val },

        // Presión (Ya viene en hPa)
        "Presión Barométrica": { unit: "hPa", convert: val => val, startAtZero: false },
        "Bar": { unit: "hPa", convert: val => val, startAtZero: false },

        // Lluvia (Ya viene en mm)
        "Tasa de Lluvia": { unit: "mm/h", convert: val => val },

        // Otros (sin conversión, solo unidad)
        "Humedad Exterior": { unit: "%", convert: val => val },
        "Altura de Olas": { unit: "m", convert: val => val },
        "Periodo de Olas": { unit: "s", convert: val => val },
        "Dirección de Olas": { unit: "°", convert: val => val },
        "Velocidad de Corriente": { unit: "m/s", convert: val => val },
        "Dirección de la Corriente": { unit: "°", convert: val => val },
        "Radiación PAR": { unit: "µE", convert: val => val },
        "Batería": { unit: "V", convert: val => val, startAtZero: false },
        "Mareógrafo": { unit: "m", convert: val => val },
        "Predicción de Marea": { unit: "m", convert: val => val }
    };

    function getSettings(variableName) {
        return variableSettings[variableName] || { unit: "", convert: val => val, startAtZero: true };
    }

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

        // Procesar datos y aplicar conversiones
        datasets.forEach((data, i) => {
            const label = labels[i];
            const settings = getSettings(label);

            // Regex for Naive ISO 8601: YYYY-MM-DDTHH:mm:ss(.sss)? (end of string)
            const naiveIsoRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$/;

            data.forEach(d => {
                // Only append Z if it matches naive ISO
                const ts = (typeof d.timestamp === 'string' && naiveIsoRegex.test(d.timestamp))
                    ? d.timestamp + "Z"
                    : d.timestamp;
                d.timestamp = new Date(ts);

                const valorOriginal = isTide ? d.level : d.value;
                let valorParseado = parseFloat(valorOriginal);

                if (!isNaN(valorParseado)) {
                    // Aplicar conversión si existe
                    d.value = settings.convert(valorParseado);
                } else {
                    d.value = null;
                }
            });
        });

        datasets = datasets.map(data => data.filter(d => d.value !== null));

        // Escalas
        const x = d3.scaleTime()
            .domain(d3.extent(datasets.flat(), d => d.timestamp))
            .range([margin.left, width - margin.right]);

        const y = d3.scaleLinear()
            .range([height - margin.bottom, margin.top]);

        if (datasets.some((_, i) => getSettings(labels[i]).startAtZero === false)) {
            // Dynamic domain if any dataset requests it
            const allValues = datasets.flat().map(d => d.value);
            const minVal = d3.min(allValues);
            const maxVal = d3.max(allValues);
            const padding = (maxVal - minVal) * 0.1 || 1; // 10% padding
            y.domain([minVal - padding, maxVal + padding]);
        } else {
            // Default 0-based domain with 10% top padding
            const maxVal = d3.max(datasets.flat(), d => d.value) || 1;
            y.domain([0, maxVal * 1.1]);
        }

        // Ejes
        const xAxis = d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat("%H:%M")); // Hora local
        const yAxis = d3.axisLeft(y);

        const gX = svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(xAxis);

        const gY = svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(yAxis);

        // Definir Clip Path para evitar que la gráfica se salga de los ejes al hacer zoom
        svg.append("defs").append("clipPath")
            .attr("id", `clip-${svgId}`)
            .append("rect")
            .attr("x", margin.left)
            .attr("y", margin.top)
            .attr("width", width - margin.left - margin.right)
            .attr("height", height - margin.top - margin.bottom);

        // Líneas
        const paths = datasets.map((data, i) =>
            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", colors[i])
                .attr("stroke-width", 2)
                .attr("clip-path", `url(#clip-${svgId})`) // Aplicar clip-path
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
                .attr("clip-path", `url(#clip-${svgId})`) // Aplicar clip-path también a los puntos
                .on("mouseover", (event, d) => {
                    const settings = getSettings(labels[i]);
                    // Usar d3.timeFormat para hora local
                    tooltip.style("display", "block")
                        .html(`📅 ${d3.timeFormat("%d/%m/%Y %H:%M")(d.timestamp)}<br>🔹 ${labels[i]}: ${d.value.toFixed(2)} ${settings.unit}`);
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
                gX.call(d3.axisBottom(newX).tickFormat(d3.timeFormat("%H:%M")));

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

        // Regex for Naive ISO 8601
        const naiveIsoRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$/;

        // Convertir y filtrar datos válidos
        data.forEach(d => {
            // Only append Z if it matches naive ISO
            const ts = (typeof d.timestamp === 'string' && naiveIsoRegex.test(d.timestamp))
                ? d.timestamp + "Z"
                : d.timestamp;
            d.timestamp = new Date(ts);
            d.value = parseFloat(d.value);
            if (isNaN(d.value)) d.value = null;
        });

        data = data.filter(d => d.value !== null);

        // Agrupar en intervalos de 10 grados
        const binSize = 10;
        const bins = d3.range(0, 360 + binSize, binSize).map(d => ({ angle: d, count: 0 }));

        data.forEach(d => {
            const binIndex = Math.floor(d.value / binSize);
            if (bins[binIndex]) bins[binIndex].count += 1;
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
            .attr("opacity", 0.8)
            .append("title") // Tooltip simple nativo para polar
            .text(d => `${d.angle}° - ${d.angle + binSize}°: ${d.count} registros`);


        svg.selectAll(".angle-line")
            .data(d3.range(0, 360, 45))
            .enter().append("line")
            .attr("x1", 0)
            .attr("y1", 0)
            // Subtract PI/2 to rotate 0 to Top
            .attr("x2", d => rScale(d3.max(bins, d => d.count)) * Math.cos(angleScale(d) - Math.PI / 2))
            .attr("y2", d => rScale(d3.max(bins, d => d.count)) * Math.sin(angleScale(d) - Math.PI / 2))
            .attr("stroke", "#999")
            .attr("stroke-width", 1);

        const cardinalDirections = {
            0: "N", 45: "NE", 90: "E", 135: "SE",
            180: "S", 225: "SO", 270: "O", 315: "NO"
        };

        svg.selectAll(".angle-label")
            .data(d3.range(0, 360, 45))
            .enter().append("text")
            // Subtract PI/2 to rotate 0 to Top
            .attr("x", d => (radius + 15) * Math.cos(angleScale(d) - Math.PI / 2))
            .attr("y", d => (radius + 15) * Math.sin(angleScale(d) - Math.PI / 2))
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .attr("font-size", "12px")
            .attr("font-weight", "bold")
            .attr("fill", "#333")
            .text(d => cardinalDirections[d] || d);

        // Etiqueta central con la variable
        svg.append("text")
            .attr("y", height / 2 - 10)
            .attr("text-anchor", "end")
            .attr("font-size", "10px")
            .attr("fill", "#666")
            .text(label);
    }

    function loadDashboard() {
        Promise.all([
            fetch(apiEndpoints.mareograph).then(r => r.text()),
            fetch(apiEndpoints.tide_forecast).then(r => r.text())
        ]).then(([mareographText, tideText]) => {
            const fixNaN = texto => JSON.parse(texto.replace(/\bNaN\b/g, 'null'));
            const mareographData = fixNaN(mareographText);
            const tideData = fixNaN(tideText);
            plotGraph("mareograph_chart", [mareographData, tideData], ["Mareógrafo", "Predicción de Marea"], ["steelblue", "red"], true);
        }).catch(err => console.error("Error:", err));

        d3.json(apiEndpoints.buoy).then(buoyData => {
            Object.keys(buoyVariables).forEach(variable => {
                if (buoyData[variable]) {
                    if (variable === "Dirección de Olas" || variable === "Dirección de la Corriente") {
                        plotPolarGraph(buoyVariables[variable], buoyData[variable], variable);
                    } else {
                        plotGraph(buoyVariables[variable], [buoyData[variable]], [variable], ["steelblue"]);
                    }
                }
            });
        }).catch(error => console.error("Error Boya:", error));

        d3.json("/api/appcr/puerto/history").then(data => {
            console.log("Datos Puerto CR:", data);
            Object.keys(puertoVariables).forEach(variable => {
                // Ahora buscamos coincidencia exacta con el nombre de la variable
                if (data[variable]) {
                    plotGraph(puertoVariables[variable], [data[variable].data], [variable], ["#10b981"]);
                }
            });
        }).catch(err => console.error("Error Puerto CR:", err));

        d3.json("/api/appcr/muelle_cc/history").then(data => {
            console.log("Datos Muelle CC:", data);
            Object.keys(muelleVariables).forEach(variable => {
                // Ahora buscamos coincidencia exacta con el nombre de la variable
                if (data[variable]) {
                    if (variable === "Dirección del Viento") {
                        plotPolarGraph(muelleVariables[variable], data[variable].data, variable);
                    } else {
                        plotGraph(muelleVariables[variable], [data[variable].data], [variable], ["#f59e0b"]);
                    }
                }
            });
        }).catch(err => console.error("Error Muelle CC:", err));
    }

    loadDashboard();
    window.reloadDashboard = loadDashboard;
});

function formatRelativeTime(isoDateString) {
    if (!isoDateString) return "❌ Sin ejecución reciente";
    const date = new Date(isoDateString);
    const now = new Date();
    const diffMs = now - date;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHour = Math.floor(diffMin / 60);

    if (diffSec < 60) return "hace unos segundos";
    if (diffMin < 60) return `hace ${diffMin} min`;
    if (diffHour < 24) {
        if (date.getDate() === now.getDate()) {
            return `hoy a las ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
        }
        return `hace ${diffHour} horas`;
    }
    return date.toLocaleString([], { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function forzarActualizacion(taskName) {
    const statusDiv = document.getElementById("estado-actualizacion");
    statusDiv.innerText = `Enviando solicitud de actualización para "${taskName}"...`;

    fetch(`/update/${taskName}`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                statusDiv.innerText = `${taskName}: ${data.status} (ID: ${data.task_id})`;
                statusDiv.className = "mt-4 p-4 bg-green-100 text-green-700 rounded shadow";
            } else {
                statusDiv.innerText = `Error: ${data.error}`;
                statusDiv.className = "mt-4 p-4 bg-red-100 text-red-700 rounded shadow";
            }
        })
        .catch(error => {
            statusDiv.innerText = `Error de red: ${error}`;
            statusDiv.className = "mt-4 p-4 bg-red-100 text-red-700 rounded shadow";
        });
}

function actualizarEstadoBackend() {
    fetch("/status")
        .then(r => r.json())
        .then(data => {
            // Actualizar indicadores de estado individuales
            const dbStatus = document.getElementById("estado-db");
            const redisStatus = document.getElementById("estado-redis");
            const celeryStatus = document.getElementById("estado-celery");
            const listaTareas = document.getElementById("lista-tareas");

            if (dbStatus) dbStatus.innerText = data.database === 'ok' ? '✅ Conectado' : '❌ Error';
            if (redisStatus) redisStatus.innerText = data.redis === 'ok' ? '✅ Conectado' : '❌ Error';
            if (celeryStatus) celeryStatus.innerText = data.celery === 'ok' ? '✅ Operativo' : '❌ Error';

            // Actualizar lista de últimas ejecuciones
            if (listaTareas) {
                let html = "";
                for (const [key, val] of Object.entries(data.last_runs)) {
                    html += `<li><strong>${key}:</strong> ${formatRelativeTime(val)}</li>`;
                }
                listaTareas.innerHTML = html;
            }
        })
        .catch(err => console.error("Error obteniendo estado:", err));
}

// Actualizar estado cada 30 segundos
setInterval(actualizarEstadoBackend, 30000);
actualizarEstadoBackend();
