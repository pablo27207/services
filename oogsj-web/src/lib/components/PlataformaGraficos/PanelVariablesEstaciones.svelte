<script>
  import { onMount } from 'svelte';

  export let endpoint = '';
  export let titulo = 'Nombre de la Estación';

  // Nuevo: íconos configurables desde afuera
  export let iconosVariables = {};

  // Nuevo: lista de claves técnicas que sí querés mostrar
  export let variablesVisibles = [];

  let loading = true;
  let ultimaFecha = '';
  let variables = [];
  let error = '';

  function formatearFecha(fechaStr) {
    if (!fechaStr) return '';

    const fecha = new Date(fechaStr);
    if (isNaN(fecha.getTime())) return '';

    const dia = String(fecha.getDate()).padStart(2, '0');
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const anio = fecha.getFullYear();
    const horas = String(fecha.getHours()).padStart(2, '0');
    const minutos = String(fecha.getMinutes()).padStart(2, '0');

    return `${dia}/${mes}/${anio} ${horas}:${minutos}`;
  }

  function formatearValor(valor) {
    if (valor === null || valor === undefined || valor === '') return '–';

    const numero = Number(valor);
    if (Number.isNaN(numero)) return valor;

    return Number.isInteger(numero) ? numero : numero.toFixed(2);
  }

  function normalizarVariables(data) {
    if (!data || typeof data !== 'object') return [];

    const variablesObj = data.variables;
    if (!variablesObj || typeof variablesObj !== 'object') return [];

    let lista = Object.entries(variablesObj).map(([clave, item]) => ({
      clave,
      nombre: item?.label ?? clave,
      unidad: item?.unit ?? '',
      valor: item?.value,
      timestamp: item?.timestamp ?? data.timestamp ?? '',
      sensor: item?.sensor ?? '',
      sensorId: item?.sensor_id ?? null,
      icono: iconosVariables[clave] ?? '❓'
    }));

    // Si variablesVisibles tiene datos, filtra y respeta ese orden
    if (Array.isArray(variablesVisibles) && variablesVisibles.length > 0) {
      lista = variablesVisibles
        .map((claveVisible) => lista.find((v) => v.clave === claveVisible))
        .filter(Boolean);
    }

    return lista;
  }

  onMount(async () => {
    loading = true;
    error = '';
    variables = [];
    ultimaFecha = '';

    try {
      const res = await fetch(endpoint);

      if (!res.ok) {
        throw new Error(`Error HTTP ${res.status}`);
      }

      const data = await res.json();

      ultimaFecha = formatearFecha(data?.timestamp);
      variables = normalizarVariables(data);
    } catch (err) {
      console.error('Error al obtener datos:', err);
      error = 'No se pudieron cargar los datos de la estación.';
    } finally {
      loading = false;
    }
  });
</script>

<div class="contenedor-principal">
  <h2 class="nombre">{titulo}</h2>

  {#if loading}
    <div class="estado">
      <em>Cargando datos...</em>
      <span class="spinner"></span>
    </div>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else if ultimaFecha}
    <p class="fecha">📅 Última medición: <strong>{ultimaFecha}</strong></p>
  {:else}
    <p class="estado"><em>No hay datos disponibles actualmente.</em></p>
  {/if}

  {#if !loading && variables.length > 0}
    <div class="cards-container">
      {#each variables as variable}
        <div class="variable-card tooltip-wrapper">
          <span class="unidad">{variable.unidad || '—'}</span>

          {#if variable.icono && typeof variable.icono === 'string' && variable.icono.startsWith('/')}
            <img class="icon-img" src={variable.icono} alt={variable.nombre} />
          {:else}
            <span class="icon">{variable.icono}</span>
          {/if}

          <span class="tooltip">
            {variable.nombre}
            {#if variable.sensor}
              <br />
              <small>{variable.sensor}</small>
            {/if}
          </span>

          <span class="valor">{formatearValor(variable.valor)}</span>
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

  .fecha,
  .estado {
    font-size: 0.95rem;
    color: #666;
    margin: 0.3rem 0 0.8rem;
  }

  .error {
    color: #b00020;
    font-weight: 600;
  }

  .spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #555;
    border-radius: 50%;
    width: 14px;
    height: 14px;
    display: inline-block;
    animation: spin 1s linear infinite;
    margin-left: 0.5rem;
    vertical-align: middle;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
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
    min-width: 110px;
    max-width: 160px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    position: relative;
  }

  .unidad {
    font-size: 0.9rem;
    color: #666;
  }

  .icon {
    font-size: 1.8rem;
  }

  .icon-img {
    width: 64px;
    height: 64px;
    object-fit: contain;
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
    background-color: rgba(0, 0, 0, 0.82);
    color: #fff;
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease-in-out;
    z-index: 10;
    line-height: 1.3;
  }

  .tooltip small {
    font-size: 0.68rem;
    color: #ddd;
  }

  .tooltip-wrapper:hover .tooltip {
    opacity: 1;
  }
</style>