<script>
    import { onMount } from 'svelte';

    export let endpoint = '';
    export let titulo = 'Nombre de la Estación';

    let loading = true;
    let ultimaFecha = '';
    let selectedCategoria = 'temperatura';
    let variablesPorCategoria = {
        temperatura: [],
        lluvia: [],
        viento: [],
        radiacion: [],
        presion: [],
        otros: []
    };

    const categorias = [
        { clave: 'temperatura', label: '🌡️ Temperatura' },
        { clave: 'lluvia', label: '🌧️ Lluvia' },
        { clave: 'viento', label: '💨 Viento' },
        { clave: 'radiacion', label: '☀️ Radiación' },
        { clave: 'presion', label: '📈 Presión' },
        { clave: 'otros', label: '🧪 Otros' }
    ];

    const mapaCategorias = {
        temperatura: ["temp_out", "temperatura"],
        lluvia: ["rain", "rainfall"],
        viento: ["wind", "vel", "velocidad"],
        radiacion: ["solar", "uv", "radiacion"],
        presion: ["bar", "press", "presion"],
        otros: ["humedad", "hum_out", "emc", "cloud", "deg_days"]
    };

    function clasificarVariable(nombre, unidad, valor) {
        const lower = nombre.toLowerCase();
        for (const [categoria, keywords] of Object.entries(mapaCategorias)) {
            if (keywords.some(keyword => lower.includes(keyword))) {
                // Redondea el valor a 2 decimales
                const valorRedondeado = valor !== null ? parseFloat(valor.toFixed(2)) : null;
                variablesPorCategoria[categoria].push({ nombre, unidad, valor: valorRedondeado, icono: getEmoji(nombre) });
                return;
            }
        }
        const valorRedondeado = valor !== null ? parseFloat(valor.toFixed(2)) : null;
        variablesPorCategoria.otros.push({ nombre, unidad, valor: valorRedondeado, icono: getEmoji(nombre) });
    }

    function getEmoji(nombre) {
        const n = nombre.toLowerCase();
        if (n.includes('temp') || n.includes('temperatura')) return '🌡️';
        if (n.includes('humedad') || n.includes('hum')) return '💧';
        if (n.includes('wind') || n.includes('viento') || n.includes('vel')) return '💨';
        if (n.includes('rain') || n.includes('lluvia')) return '🌧️';
        if (n.includes('uv') || n.includes('radiacion')) return '🌞';
        if (n.includes('solar')) return '🔆';
        if (n.includes('bar') || n.includes('press') || n.includes('presion')) return '📈';
        if (n.includes('emc')) return '🌾';
        if (n.includes('cloud')) return '☁️';
        return '❓';
    }

    function formatearFecha(fechaStr) {
        const fecha = new Date(fechaStr);
        return fecha.toLocaleString();
    }

    onMount(async () => {
        try {
            const res = await fetch(endpoint);
            const data = await res.json();
            
            if (data.length > 0) {
                // Agrupamos los datos por la propiedad 'variable'
                const datosAgrupados = {};
                data.forEach(item => {
                    const variableNombre = item.variable;
                    // Solo toma la última medición para el panel de variables
                    if (!datosAgrupados[variableNombre]) {
                        datosAgrupados[variableNombre] = item;
                    }
                });
                
                ultimaFecha = formatearFecha(Object.values(datosAgrupados)[0].timestamp);
                
                // Limpiamos las variablesPorCategoria para evitar datos duplicados
                for (const key in variablesPorCategoria) {
                    variablesPorCategoria[key] = [];
                }

                // Clasificamos las variables agrupadas
                Object.values(datosAgrupados).forEach(item => {
                    clasificarVariable(item.variable, item.unit, item.value);
                });
            }
        } catch (err) {
            console.error("Error al obtener datos:", err);
        } finally {
            loading = false;
        }
    });
</script>

<div class="contenedor-principal">
    <h2 class="nombre">{titulo}</h2>

    {#if loading}
        <div class="estado"><em>Cargando datos...</em></div>
    {:else}
        <p class="fecha">📅 Última medición: <strong>{ultimaFecha}</strong></p>

        <div class="tabs">
            {#each categorias as c}
                <button on:click={() => selectedCategoria = c.clave}
                        class:selected={selectedCategoria === c.clave}>
                    {c.label}
                </button>
            {/each}
        </div>

        <div class="cards-container">
            {#each variablesPorCategoria[selectedCategoria] as variable}
                <div class="variable-card tooltip-wrapper">
                    <span class="unidad-card">{variable.unidad}</span>
                    <span class="icon">{variable.icono}</span>
                    <span class="tooltip">{variable.nombre}</span>
                    <span class="valor">{variable.valor ?? '–'}</span>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .contenedor-principal {
        background: #fdfdfd;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    .nombre {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .fecha, .estado {
        font-size: 0.95rem;
        color: #666;
        margin: 0.3rem 0 0.8rem;
    }

    .tabs {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .tabs button {
        padding: 0.4rem 0.8rem;
        border: none;
        border-radius: 0.5rem;
        background: #eee;
        cursor: pointer;
        transition: none; /* Elimina la transición para un comportamiento estático */
    }

    .tabs button.selected {
        background: #007BFF;
        color: white;
    }

    .tabs button:hover {
        background: #e0e0e0;
    }

    .tabs button.selected:hover {
        background: #0056b3;
    }

    .cards-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }

    .variable-card {
        background: #f4f4f4;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        min-width: 100px;
        max-width: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        position: relative;
        transition: none; /* Elimina la transición para un comportamiento estático */
        cursor: default;
    }

    .unidad-card {
        font-size: 0.9rem;
        color: #666;
        order: -1; /* Mueve la unidad a la parte superior */
    }

    .icon {
        font-size: 1.6rem;
    }

    .valor {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
    }

    .tooltip-wrapper {
        position: relative;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .tooltip {
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.75);
        color: #fff;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s ease-in-out;
        z-index: 1;
    }

    .tooltip-wrapper:hover .tooltip {
        opacity: 1;
    }
</style>
