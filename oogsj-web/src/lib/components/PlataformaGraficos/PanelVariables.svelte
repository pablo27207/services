<script>
  import { onMount } from 'svelte';

  export let endpoint = '';
  export let titulo = 'Nombre de la Plataforma';
  export let iconosVariables = {};
  export let ordenVariables = [];

  let loading = true;
  let ultimaFecha = '';
  let variables = [];

  // =========================================================
  // HELPERS DE FECHA
  // =========================================================

  // Formatea una fecha completa para mostrar arriba del panel.
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

  // =========================================================
  // HELPERS DE VARIABLES
  // =========================================================

  // Limpia los nombres técnicos para mostrar algo más humano.
  function obtenerNombreVisible(nombreTecnico) {
    if (!nombreTecnico) return 'Variable';

    return nombreTecnico
      .replace(/^Sensor de\s*/i, '')
      .replace(/^Sensor\s*/i, '')
      .replace(/\s*-\s*CIDMAR-\d+/i, '')
      .trim();
  }

  // Detecta si la variable es direccional.
  function esVariableDireccional(nombreTecnico) {
    if (!nombreTecnico) return false;

    const nombre = nombreTecnico.toLowerCase();

    return nombre.includes('dirección') || nombre.includes('direccion');
  }

  // Convierte grados a punto cardinal de 8 direcciones.
  function gradosACardinal(grados) {
    if (grados === null || grados === undefined || isNaN(Number(grados))) return '';

    const valor = ((Number(grados) % 360) + 360) % 360;

    const puntos = ['Norte', 'Noreste', 'Este', 'Sudeste', 'Sur', 'Suroeste', 'Oeste', 'Noroeste'];
    const indice = Math.round(valor / 45) % 8;

    return puntos[indice];
  }

  // Permite definir decimales según la variable.
  function obtenerDecimales(nombreTecnico) {
    if (!nombreTecnico) return 1;

    const nombre = nombreTecnico.toLowerCase();

    if (nombre.includes('altura')) return 2;
    if (nombre.includes('periodo') || nombre.includes('período')) return 1;
    if (nombre.includes('bater')) return 2;
    if (nombre.includes('radiación') || nombre.includes('radiacion')) return 0;
    if (nombre.includes('dirección') || nombre.includes('direccion')) return 0;

    return 1;
  }

  // Formatea el valor principal que se verá grande en la card.
  function formatearValor(nombreTecnico, valor) {
    if (valor === null || valor === undefined || valor === '') return '–';

    const numero = Number(valor);

    if (Number.isNaN(numero)) return '–';

    const decimales = obtenerDecimales(nombreTecnico);

    return numero.toFixed(decimales);
  }

  // Permite limpiar o normalizar unidades si hiciera falta.
  // Por ahora respetamos la unidad que viene del endpoint.
  function obtenerUnidadVisible(unidad) {
    if (!unidad) return '';

    return unidad.trim();
  }

  // Texto secundario para direcciones: muestra el cardinal.
  function obtenerTextoSecundario(nombreTecnico, valor) {
    if (!esVariableDireccional(nombreTecnico)) return '';

    const numero = Number(valor);
    if (Number.isNaN(numero)) return '';

    return gradosACardinal(numero);
  }

  // =========================================================
  // CARGA DE DATOS
  // =========================================================

  onMount(async () => {
    try {
      const res = await fetch(endpoint);
      const data = await res.json();

      // Si hay un orden manual, lo respetamos.
      // Si no, usamos las claves que lleguen del endpoint.
      const claves = ordenVariables.length > 0 ? ordenVariables : Object.keys(data);

      // Tomamos la primera fecha válida disponible.
      const primerTimestampValido = claves
        .map((clave) => data[clave]?.timestamp)
        .find((timestamp) => timestamp);

      ultimaFecha = formatearFecha(primerTimestampValido);

      // Transformamos la data técnica en una estructura más lista para UI.
      variables = claves.map((nombreTecnico) => {
        const dato = data[nombreTecnico] ?? {};
        const valorCrudo = dato.value ?? null;

        return {
          nombreTecnico,
          nombreVisible: obtenerNombreVisible(nombreTecnico),
          unidad: obtenerUnidadVisible(dato.unit ?? ''),
          valorCrudo,
          valorVisible: formatearValor(nombreTecnico, valorCrudo),
          textoSecundario: obtenerTextoSecundario(nombreTecnico, valorCrudo),
          icono: iconosVariables[nombreTecnico] ?? null
        };
      });
    } catch (err) {
      console.error('Error al obtener datos:', err);
      variables = [];
      ultimaFecha = '';
    } finally {
      loading = false;
    }
  });
</script>

<div class="contenedor-principal">
  <h2 class="nombre">{titulo}</h2>

  {#if loading}
    <div class="estado estado-loading">
      <em>Cargando datos...</em>
      <span class="spinner"></span>
    </div>
  {:else if ultimaFecha}
    <p class="fecha">
      Última medición: <strong>{ultimaFecha}</strong>
    </p>
  {:else}
    <p class="estado">
      <em>No hay datos disponibles actualmente.</em>
    </p>
  {/if}

  <div class="cards-container">
    {#each variables as variable}
      <article
        class="variable-card"
        title={variable.nombreTecnico}
        aria-label={variable.nombreVisible}
      >
        <!-- Nombre visible de la variable -->
        <h3 class="variable-nombre">{variable.nombreVisible}</h3>

        <!-- Ícono -->
        {#if variable.icono}
          {#if variable.icono.startsWith('/')}
            <img
              class="icon-img"
              src={variable.icono}
              alt={variable.nombreVisible}
            />
          {:else}
            <span class="icon" aria-hidden="true">{variable.icono}</span>
          {/if}
        {:else}
          <span class="icon" aria-hidden="true">❓</span>
        {/if}

        <!-- Valor principal -->
        <div class="valor-bloque">
          <span class="valor">{variable.valorVisible}</span>

          {#if variable.unidad}
            <span class="unidad">{variable.unidad}</span>
          {/if}
        </div>

        <!-- Texto secundario para variables direccionales -->
        {#if variable.textoSecundario}
          <span class="texto-secundario">{variable.textoSecundario}</span>
        {/if}
      </article>
    {/each}
  </div>
</div>

<style>
  .contenedor-principal {
    background-color: #f9f9f9;
    padding: 1.25rem;
    border-radius: 1rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .nombre {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    color: #1f2937;
  }

  .fecha,
  .estado {
    font-size: 0.95rem;
    color: #5f6b7a;
    margin: 0.25rem 0 0.8rem 0;
  }

  .estado-loading {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
  }

  .spinner {
    border: 3px solid #e5e7eb;
    border-top: 3px solid #555;
    border-radius: 50%;
    width: 14px;
    height: 14px;
    display: inline-block;
    animation: spin 1s linear infinite;
    vertical-align: middle;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Grid responsive real para cards */
  .cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 0.9rem;
    margin-top: 1rem;
  }

  .variable-card {
    background: #f4f4f4;
    padding: 0.95rem 0.85rem;
    border-radius: 0.85rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    gap: 0.55rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    min-height: 200px;
  }

  /* Nombre de variable visible siempre */
  .variable-nombre {
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.2;
    color: #1f2937;
    margin: 0;
    min-height: 2.4em;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .icon {
    font-size: 2.4rem;
    line-height: 1;
  }

  .icon-img {
    width: 52px;
    height: 52px;
    object-fit: contain;
  }

  .valor-bloque {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.15rem;
  }

  .valor {
    font-size: 1.55rem;
    font-weight: 700;
    line-height: 1.1;
    color: #111827;
  }

  .unidad {
    font-size: 0.92rem;
    color: #6b7280;
  }

  .texto-secundario {
    font-size: 0.92rem;
    font-weight: 600;
    color: #374151;
  }

  /* Ajustes para pantallas pequeñas */
  @media (max-width: 640px) {
    .contenedor-principal {
      padding: 1rem;
    }

    .nombre {
      font-size: 1.25rem;
    }

    .fecha,
    .estado {
      font-size: 0.9rem;
    }

    .cards-container {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.75rem;
    }

    .variable-card {
      padding: 0.85rem 0.7rem;
      min-height: 185px;
    }

    .variable-nombre {
      font-size: 0.88rem;
      min-height: 2.6em;
    }

    .icon {
      font-size: 2rem;
    }

    .icon-img {
      width: 44px;
      height: 44px;
    }

    .valor {
      font-size: 1.35rem;
    }

    .unidad,
    .texto-secundario {
      font-size: 0.84rem;
    }
  }

  @media (max-width: 420px) {
    .cards-container {
      grid-template-columns: 1fr 1fr;
    }

    .variable-card {
      min-height: 175px;
    }
  }
</style>