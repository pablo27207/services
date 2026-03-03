<script>
  import { onMount } from 'svelte';

  export let endpoint = '';
  export let titulo = 'Nombre de la Plataforma';
  export let iconosVariables = {};
  export let ordenVariables = [];

  let loading = true;
  let ultimaFecha = '';
  let variables = [];

  function formatearFecha(fechaStr) {
    if (!fechaStr) return '';
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

      const claves = ordenVariables.length > 0
        ? ordenVariables
        : Object.keys(data);

      if (claves.length > 0 && data[claves[0]]) {
        ultimaFecha = formatearFecha(data[claves[0]].timestamp);

        variables = claves.map(nombre => ({
          nombre,
          unidad: data[nombre]?.unit ?? '',
          valor: data[nombre]?.value ?? null,
          icono: iconosVariables[nombre] ?? null
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
    <div class="estado">
      <em>Cargando datos...</em>
      <span class="spinner"></span>
    </div>
  {:else if ultimaFecha}
    <p class="fecha">
      📅 Última medición: <strong>{ultimaFecha}</strong>
    </p>
  {:else}
    <p class="estado">
      <em>No hay datos disponibles actualmente.</em>
    </p>
  {/if}

  <div class="cards-container">
    {#each variables as variable}
      <div class="variable-card tooltip-wrapper">

        {#if variable.icono}
          {#if variable.icono.startsWith('/')}
            <img
              class="icon-img"
              src={variable.icono}
              alt={variable.nombre}
            />
          {:else}
            <span class="icon">{variable.icono}</span>
          {/if}
        {:else}
          <span class="icon">❓</span>
        {/if}

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
    min-width: 120px; /* Aumentamos ligeramente para acomodar iconos grandes */
    max-width: 160px; /* Aumentamos ligeramente para acomodar iconos grandes */
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px; /* Un poco más de espacio entre elementos */
    position: relative;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1); /* Sombra suave para las tarjetas */
  }

  /* 👇 MODIFICADO: Estilo para iconos de texto/emoji más grandes */
  .icon {
    font-size: 3rem; /* Aumentado considerablemente */
  }

  /* 👇 MODIFICADO: Estilo para imágenes de iconos más grandes y eficaces */
  .icon-img {
    width: 64px; /* Aumentado de 36px a 64px */
    height: 64px; /* Aumentado de 36px a 64px */
    object-fit: contain;
  }

  /* 👇 MODIFICADO: Estilo para el valor un poco más grande para acompañar */
  .valor {
    font-size: 1.5rem; /* Aumentado de 1.3rem */
    font-weight: 600;
    color: #333;
  }

  .unidad {
    font-size: 0.9rem;
    color: #666;
  }

  .tooltip-wrapper {
    position: relative;
  }

  /* 👇 MODIFICADO: Mejor posicionamiento y diseño del tooltip */
  .tooltip {
    position: absolute;
    bottom: 110%; /* Posicionado por encima de la tarjeta */
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0, 0, 0, 0.85); /* Un fondo un poco más oscuro */
    color: #fff;
    padding: 6px 12px; /* Un poco más de padding */
    border-radius: 6px; /* Bordes un poco más redondeados */
    font-size: 0.85rem; /* Fuente ligeramente más grande */
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease-in-out, transform 0.2s ease-in-out;
    z-index: 10; /* Asegurar que se superpone */
    box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* Sombra para el tooltip */
  }

  /* 👇 MODIFICADO: Añadimos una animación sutil al hover */
  .tooltip-wrapper:hover .tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(-5px); /* Pequeño movimiento hacia arriba */
  }
</style>