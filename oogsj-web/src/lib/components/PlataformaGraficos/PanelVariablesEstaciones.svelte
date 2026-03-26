<script>
  import { onMount } from 'svelte';

  export let endpoint = '';
  export let titulo = 'Nombre de la Estación';

  // Íconos configurables desde el componente padre
  export let iconosVariables = {};

  // Lista de claves técnicas visibles y en el orden deseado
  export let variablesVisibles = [];

  let loading = true;
  let ultimaFecha = '';
  let variables = [];
  let error = '';

  // =========================================================
  // HELPERS DE FECHA
  // =========================================================

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

  // Nombre visible más humano según la clave técnica
  function obtenerNombreVisible(clave, label) {
    const mapa = {
      barometric_pressure: 'Presión atmosférica',
      outdoor_humidity: 'Humedad exterior',
      outdoor_temperature: 'Temperatura exterior',
      wind_speed: 'Velocidad del viento',
      wind_speed_avg: 'Velocidad del viento',
      wind_direction: 'Dirección del viento',
      rainfall: 'Lluvia',
      solar_radiation: 'Radiación solar'
    };

    return mapa[clave] ?? label ?? clave;
  }

  // Cantidad de decimales por variable
  function obtenerDecimales(clave) {
    const mapa = {
      barometric_pressure: 1,
      outdoor_humidity: 0,
      outdoor_temperature: 1,
      wind_speed: 1,
      wind_speed_avg: 1,
      wind_direction: 0,
      rainfall: 1,
      solar_radiation: 0
    };

    return mapa[clave] ?? 1;
  }

  // Formato principal del valor
  function formatearValor(clave, valor) {
    if (valor === null || valor === undefined || valor === '') return '–';

    const numero = Number(valor);
    if (Number.isNaN(numero)) return valor;

    return numero.toFixed(obtenerDecimales(clave));
  }

  function obtenerUnidadVisible(unidad) {
    if (!unidad) return '—';
    return String(unidad).trim();
  }

  // Detecta si la variable es direccional
  function esVariableDireccional(clave) {
    return clave === 'wind_direction';
  }

  // Convierte grados a cardinal de 8 sectores
  function gradosACardinal(grados) {
    const numero = Number(grados);
    if (Number.isNaN(numero)) return '';

    const valor = ((numero % 360) + 360) % 360;

    const puntos = [
      'Norte',
      'Noreste',
      'Este',
      'Sudeste',
      'Sur',
      'Suroeste',
      'Oeste',
      'Noroeste'
    ];

    const indice = Math.round(valor / 45) % 8;
    return puntos[indice];
  }

  // Texto secundario para variables direccionales
  function obtenerTextoSecundario(clave, valor) {
    if (!esVariableDireccional(clave)) return '';

    const numero = Number(valor);
    if (Number.isNaN(numero)) return '';

    return gradosACardinal(numero);
  }

  function normalizarVariables(data) {
    if (!data || typeof data !== 'object') return [];

    const variablesObj = data.variables;
    if (!variablesObj || typeof variablesObj !== 'object') return [];

    let lista = Object.entries(variablesObj).map(([clave, item]) => ({
      clave,
      nombreVisible: obtenerNombreVisible(clave, item?.label),
      nombreTecnico: item?.label ?? clave,
      unidad: obtenerUnidadVisible(item?.unit),
      valorCrudo: item?.value,
      valorVisible: formatearValor(clave, item?.value),
      textoSecundario: obtenerTextoSecundario(clave, item?.value),
      timestamp: item?.timestamp ?? data.timestamp ?? '',
      sensor: item?.sensor ?? '',
      sensorId: item?.sensor_id ?? null,
      icono: iconosVariables[clave] ?? '❓'
    }));

    // Respetar el orden visible definido desde el padre
    if (Array.isArray(variablesVisibles) && variablesVisibles.length > 0) {
      lista = variablesVisibles
        .map((claveVisible) => lista.find((v) => v.clave === claveVisible))
        .filter(Boolean);
    }

    return lista;
  }

  // =========================================================
  // CARGA DE DATOS
  // =========================================================

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
    <p class="fecha">Última medición: <strong>{ultimaFecha}</strong></p>
  {:else}
    <p class="estado"><em>No hay datos disponibles actualmente.</em></p>
  {/if}

  {#if !loading && variables.length > 0}
    <div class="cards-container">
      {#each variables as variable}
        <article
          class="variable-card"
          title={variable.nombreTecnico}
          aria-label={variable.nombreVisible}
        >
          <!-- Nombre visible -->
          <h3 class="variable-nombre">{variable.nombreVisible}</h3>

          <!-- Ícono -->
          {#if variable.icono && typeof variable.icono === 'string' && variable.icono.startsWith('/')}
            <img class="icon-img" src={variable.icono} alt={variable.nombreVisible} />
          {:else}
            <span class="icon" aria-hidden="true">{variable.icono}</span>
          {/if}

          <!-- Valor principal -->
          <div class="valor-bloque">
            <span class="valor">{variable.valorVisible}</span>
            <span class="unidad">{variable.unidad}</span>
          </div>

          <!-- Texto secundario para dirección del viento -->
          {#if variable.textoSecundario}
            <span class="texto-secundario">{variable.textoSecundario}</span>
          {/if}
        </article>
      {/each}
    </div>
  {/if}
</div>

<style>
  .contenedor-principal {
    background: #fdfdfd;
    padding: 1.25rem;
    border-radius: 1rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .nombre {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.45rem;
    color: #111827;
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
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 0.9rem;
    margin-top: 1rem;
  }

  .variable-card {
    background: #f4f4f4;
    padding: 0.95rem 0.85rem;
    border-radius: 8px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.55rem;
    min-height: 190px;
  }

  .variable-nombre {
    margin: 0;
    min-height: 2.4em;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.2;
    color: #1f2937;
  }

  .icon {
    font-size: 2rem;
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
    font-size: 1.45rem;
    font-weight: 700;
    color: #111827;
    line-height: 1.1;
  }

  .unidad {
    font-size: 0.9rem;
    color: #6b7280;
  }

  .texto-secundario {
    font-size: 0.9rem;
    font-weight: 600;
    color: #374151;
  }

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
      min-height: 180px;
    }

    .variable-nombre {
      font-size: 0.88rem;
      min-height: 2.6em;
    }

    .icon {
      font-size: 1.8rem;
    }

    .icon-img {
      width: 44px;
      height: 44px;
    }

    .valor {
      font-size: 1.25rem;
    }

    .unidad,
    .texto-secundario {
      font-size: 0.82rem;
    }
  }

  @media (max-width: 420px) {
    .cards-container {
      grid-template-columns: 1fr 1fr;
    }
  }
</style>