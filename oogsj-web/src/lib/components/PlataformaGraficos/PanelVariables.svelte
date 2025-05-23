<script>
  import { onMount } from 'svelte';
  export let endpoint = '';
  export let titulo = 'Nombre de la Plataforma';
  export let iconosVariables = {};
  export let ordenVariables = []; // 🆕 ORDEN MANUAL

  let loading = true;
  let ultimaFecha = '';
  let variables = [];

  function formatearFecha(fechaStr) {
    const fecha = new Date(fechaStr);
    const dia = String(fecha.getDate()).padStart(2, '0');
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const anio = fecha.getFullYear();
    const horas = String(fecha.getHours()).padStart(2, '0');
    const minutos = String(fecha.getMinutes()).padStart(2, '0');
    return `${dia}/${mes}/${anio} ${horas}:${minutos}`;
  }

  onMount(async () => {
    try {
      const res = await fetch(endpoint);
      const data = await res.json();
      console.log("Datos recibidos:", data);

      const claves = ordenVariables.length > 0
        ? ordenVariables
        : Object.keys(data);

      if (claves.length > 0) {
        const primera = data[claves[0]];
        ultimaFecha = formatearFecha(primera.timestamp);

        variables = claves.map(nombre => ({
          nombre,
          unidad: data[nombre]?.unit ?? '',
          valor: data[nombre]?.value ?? null,
          icono: iconosVariables[nombre] ?? '❓'
        }));
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
      <div class="estado"><em>Cargando datos...</em> <span class="spinner"></span></div>
    {:else if ultimaFecha}
      <p class="fecha">📅 Última medición: <strong>{ultimaFecha}</strong></p>
    {:else}
      <p class="estado"><em>No hay datos disponibles actualmente.</em></p>
    {/if}
  
    <div class="cards-container">
      {#each variables as variable}
        <div class="variable-card tooltip-wrapper">
          <span class="icon">{variable.icono}</span>
          <span class="tooltip">{variable.nombre}</span>
          <span class="valor">{variable.valor ?? '–'}</span>
          <span class="unidad">{variable.unidad}</span>
        </div>
      {/each}
    </div>
  </div>
  
  <style>
    .contenedor-principal {
      background-color: #f9f9f9;
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
      margin: 0.3rem 0 0.8rem 0;
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
      min-width: 100px;
      max-width: 150px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 5px;
      position: relative;
    }
  
    .icon {
      font-size: 1.6rem;
    }
  
    .valor {
      font-size: 1.3rem;
      font-weight: 600;
      color: #333;
    }
  
    .unidad {
      font-size: 0.9rem;
      color: #666;
    }
  
    .tooltip-wrapper {
      position: relative;
      display: inline-flex;
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
  