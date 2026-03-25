<script>
  import { onMount, onDestroy, tick } from 'svelte';
  import * as d3 from 'd3';
  import { timeFormatLocale } from 'd3';

  let resizeObserver;

  export let data = [];
  export let label = '';
  export let color = 'steelblue';
  export let height = 300;

  let svgContainer;
  let tooltip;
  let chartCard;

  // Márgenes internos del gráfico
  const margin = { top: 20, right: 20, bottom: 42, left: 55 };

  // Localización en español para fechas
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

  // =========================================================
  // HELPERS DE FORMATO
  // =========================================================

  // Detecta cuántos decimales conviene mostrar según la variable
  function obtenerDecimales(label) {
    const texto = (label || '').toLowerCase();

    if (texto.includes('altura')) return 2;
    if (texto.includes('periodo') || texto.includes('período')) return 1;
    if (texto.includes('bater')) return 2;
    if (texto.includes('radiación') || texto.includes('radiacion')) return 0;
    if (texto.includes('temperatura')) return 1;
    if (texto.includes('humedad')) return 0;
    if (texto.includes('velocidad')) return 1;

    return 1;
  }

  // Obtiene la primera unidad válida encontrada en la serie
  function obtenerUnidad(data) {
    const unidad = data.find(d => d?.unit)?.unit;
    return unidad ? String(unidad).trim() : '';
  }

  // Variable reactiva para mostrar la unidad arriba del gráfico
  $: unidadGrafico = obtenerUnidad(data);

  // Formatea valores para ejes y tooltip
  function formatearValor(label, valor) {
    const numero = Number(valor);
    if (Number.isNaN(numero)) return '–';

    const decimales = obtenerDecimales(label);
    return numero.toFixed(decimales);
  }

  // Define cuánto tiempo de separación consideramos "gap"
  // Si la diferencia entre puntos supera este valor, la línea se corta
  function obtenerGapMaximoMs(label) {
    const texto = (label || '').toLowerCase();

    if (texto.includes('bater')) return 12 * 60 * 60 * 1000;
    return 6 * 60 * 60 * 1000;
  }

  // Altura responsive según el ancho del contenedor
  function obtenerAlturaResponsive(width) {
    if (width < 420) return 240;
    if (width < 768) return 260;
    return height;
  }

  // Cantidad de ticks según ancho disponible
  function obtenerCantidadTicks(width) {
    if (width < 420) return 4;
    if (width < 768) return 5;
    return 7;
  }

  // =========================================================
  // CICLO DE VIDA
  // =========================================================

  onMount(async () => {
    await tick();

    tooltip = d3.select(`#tooltip-${label.replace(/\s+/g, '-')}`);
    drawChart();

    resizeObserver = new ResizeObserver(() => {
      drawChart();
    });

    if (chartCard) resizeObserver.observe(chartCard);

    window.addEventListener('resize', drawChart);
  });

  onDestroy(() => {
    if (resizeObserver) resizeObserver.disconnect();
    window.removeEventListener('resize', drawChart);
  });

  // =========================================================
  // FUNCIÓN PRINCIPAL DE DIBUJO
  // =========================================================

  function drawChart() {
    if (!chartCard || !svgContainer) return;

    const width = chartCard.clientWidth;
    const responsiveHeight = obtenerAlturaResponsive(width);
    const tickCount = obtenerCantidadTicks(width);

    const svg = d3.select(svgContainer)
      .attr('viewBox', `0 0 ${width} ${responsiveHeight}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .html('');

    // Estado vacío
    if (!data || data.length === 0) {
      svg.append('text')
        .attr('x', width / 2)
        .attr('y', responsiveHeight / 2)
        .attr('text-anchor', 'middle')
        .attr('fill', '#555')
        .text('No hay datos disponibles');
      return;
    }

    // Limpieza y normalización de datos
    const filteredData = data
      .filter(d => d && d.timestamp !== undefined && d.value !== undefined && d.value !== null && !isNaN(d.value))
      .map(d => ({
        ...d,
        timestamp: d.timestamp instanceof Date ? d.timestamp : new Date(d.timestamp),
        value: parseFloat(d.value)
      }))
      .filter(d => !isNaN(d.timestamp.getTime()) && !isNaN(d.value))
      .sort((a, b) => a.timestamp - b.timestamp);

    if (filteredData.length === 0) {
      svg.append('text')
        .attr('x', width / 2)
        .attr('y', responsiveHeight / 2)
        .attr('text-anchor', 'middle')
        .attr('fill', '#555')
        .text('No hay datos válidos para mostrar');
      return;
    }

    const unidad = obtenerUnidad(filteredData);

    // Escala X temporal
    const x = d3.scaleTime()
      .domain(d3.extent(filteredData, d => d.timestamp))
      .range([margin.left, width - margin.right]);

    // Escala Y con buffer visual
    const yMin = d3.min(filteredData, d => d.value);
    const yMax = d3.max(filteredData, d => d.value);

    if (yMin === undefined || yMax === undefined) return;

    let buffer;
    if (yMin === yMax) {
      buffer = Math.abs(yMax) * 0.05;
    } else {
      buffer = (yMax - yMin) * 0.1;
    }

    if (buffer === 0) buffer = 1;

    const y = d3.scaleLinear()
      .domain([yMin - buffer, yMax + buffer])
      .nice()
      .range([responsiveHeight - margin.bottom, margin.top]);

    // Formatos de fecha según ancho
    const formatoFechaEje = width < 520
      ? localeEs.format('%d/%m')
      : localeEs.format('%a %d');

    const formatoFechaTooltip = localeEs.format('%d/%m/%Y');
    const formatoHoraTooltip = localeEs.format('%H:%M');

    // =========================================================
    // GRID DE FONDO
    // =========================================================

    svg.append('g')
      .attr('class', 'grid-y')
      .attr('transform', `translate(${margin.left},0)`)
      .call(
        d3.axisLeft(y)
          .ticks(5)
          .tickSize(-(width - margin.left - margin.right))
          .tickFormat('')
      )
      .call(g => g.selectAll('line').attr('stroke', '#e5e7eb'))
      .call(g => g.select('path').remove());

    // =========================================================
    // EJES
    // =========================================================

    svg.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${responsiveHeight - margin.bottom})`)
      .call(
        d3.axisBottom(x)
          .ticks(tickCount)
          .tickFormat(formatoFechaEje)
      )
      .call(g => g.selectAll('text').attr('font-size', width < 520 ? '10px' : '11px'))
      .call(g => g.selectAll('line, path').attr('stroke', '#9ca3af'));

    svg.append('g')
      .attr('class', 'y-axis')
      .attr('transform', `translate(${margin.left},0)`)
      .call(
        d3.axisLeft(y)
          .ticks(5)
          .tickFormat(d => formatearValor(label, d))
      )
      .call(g => g.selectAll('text').attr('font-size', width < 520 ? '10px' : '11px'))
      .call(g => g.selectAll('line, path').attr('stroke', '#9ca3af'));

    // =========================================================
    // LÍNEA CON CORTE EN GAPS
    // =========================================================

    const gapMaximoMs = obtenerGapMaximoMs(label);

    const lineGenerator = d3.line()
      .defined((d, i, arr) => {
        if (i === 0) return true;
        const diferencia = d.timestamp - arr[i - 1].timestamp;
        return diferencia <= gapMaximoMs;
      })
      .x(d => x(d.timestamp))
      .y(d => y(d.value));

    svg.append('path')
      .datum(filteredData)
      .attr('class', 'line-path')
      .attr('fill', 'none')
      .attr('stroke', color)
      .attr('stroke-width', width < 520 ? 2 : 2.4)
      .attr('stroke-linejoin', 'round')
      .attr('stroke-linecap', 'round')
      .attr('d', lineGenerator);

    // =========================================================
    // PUNTOS
    // =========================================================

    const radioPunto = width < 520 ? 3 : 4;

    svg.selectAll('.data-point')
      .data(filteredData)
      .enter()
      .append('circle')
      .attr('class', 'data-point')
      .attr('cx', d => x(d.timestamp))
      .attr('cy', d => y(d.value))
      .attr('r', radioPunto)
      .attr('fill', color)
      .attr('opacity', 0.9)
      .on('mouseover', (event, d) => {
        const valorVisible = formatearValor(label, d.value);

        tooltip
          .style('display', 'block')
          .html(`
            <div><strong>${label}</strong></div>
            <div>Fecha: ${formatoFechaTooltip(d.timestamp)}</div>
            <div>Hora: ${formatoHoraTooltip(d.timestamp)}</div>
            <div>Valor: ${valorVisible}${unidad ? ` ${unidad}` : ''}</div>
          `);
      })
      .on('mousemove', (event) => {
        const bounds = chartCard.getBoundingClientRect();

        const tooltipNode = tooltip.node();
        const tooltipWidth = tooltipNode ? tooltipNode.offsetWidth : 180;
        const tooltipHeight = tooltipNode ? tooltipNode.offsetHeight : 80;

        let left = event.clientX - bounds.left + 12;
        let top = event.clientY - bounds.top - tooltipHeight - 10;

        // Si se pasa por la derecha, lo movemos hacia la izquierda
        if (left + tooltipWidth > bounds.width - 8) {
          left = bounds.width - tooltipWidth - 8;
        }

        // Si queda demasiado arriba, lo bajamos debajo del cursor
        if (top < 8) {
          top = event.clientY - bounds.top + 12;
        }

        // Evita que se salga por la izquierda
        if (left < 8) {
          left = 8;
        }

        tooltip
          .style('left', `${left}px`)
          .style('top', `${top}px`);
      })
      .on('mouseout', () => {
        tooltip.style('display', 'none');
      });

    // =========================================================
    // ZOOM
    // =========================================================

    const zoom = d3.zoom()
      .scaleExtent([1, 8])
      .translateExtent([[0, 0], [width, responsiveHeight]])
      .extent([[0, 0], [width, responsiveHeight]])
      .on('zoom', (event) => {
        const newX = event.transform.rescaleX(x);

        const newLine = d3.line()
          .defined((d, i, arr) => {
            if (i === 0) return true;
            const diferencia = d.timestamp - arr[i - 1].timestamp;
            return diferencia <= gapMaximoMs;
          })
          .x(d => newX(d.timestamp))
          .y(d => y(d.value));

        svg.select('.x-axis')
          .call(
            d3.axisBottom(newX)
              .ticks(tickCount)
              .tickFormat(formatoFechaEje)
          )
          .call(g => g.selectAll('text').attr('font-size', width < 520 ? '10px' : '11px'))
          .call(g => g.selectAll('line, path').attr('stroke', '#9ca3af'));

        svg.select('.line-path').attr('d', newLine(filteredData));

        svg.selectAll('.data-point')
          .attr('cx', d => newX(d.timestamp));
      });

    svg.call(zoom);
  }
</script>

<div bind:this={chartCard} class="grafico-card">
  {#if unidadGrafico}
    <p class="unidad-grafico">Unidad: {unidadGrafico}</p>
  {/if}

  <svg bind:this={svgContainer}></svg>

  <div
    class="tooltip"
    id={"tooltip-" + label.replace(/\s+/g, '-')}
  ></div>
</div>

<style>
  .grafico-card {
    width: 100%;
    position: relative;
    padding: 0.5rem;
    background: white;
    border-radius: 12px;
    margin-bottom: 1rem;
    box-sizing: border-box;
  }

  .unidad-grafico {
    margin: 0 0 0.4rem 0.4rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #4b5563;
    text-align: left;
  }

  svg {
    width: 100%;
    height: auto;
    display: block;
    overflow: visible;
  }

  .tooltip {
    position: absolute;
    display: none;
    background: #ffffff;
    border: 1px solid #d1d5db;
    padding: 8px 10px;
    pointer-events: none;
    font-size: 0.84rem;
    line-height: 1.35;
    border-radius: 8px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
    color: #111827;
    z-index: 9999;
    max-width: 220px;
  }

  @media (max-width: 640px) {
    .grafico-card {
      padding: 0.35rem;
      border-radius: 10px;
    }

    .unidad-grafico {
      font-size: 0.82rem;
      margin-left: 0.25rem;
    }

    .tooltip {
      font-size: 0.78rem;
      max-width: 190px;
      padding: 7px 8px;
    }
  }
</style>