<script lang="ts">
  import { onMount } from "svelte";
  import GraficoMareografo from '$lib/components/datos/GraficosEstandar/GraficoMareografo.svelte';

  // Serie observada del mareógrafo
  let mareographData: { timestamp: string; level: number }[] = [];

  // Serie de referencia / predicción de marea
  let tideForecastData: { timestamp: string; level: number }[] = [];

  // Estado de carga y error para una UI más clara
  let loading = true;
  let error = false;

  // =========================================================
  // HELPERS
  // =========================================================

  function formatearNivel(valor: number | null | undefined): string {
    const numero = Number(valor);
    if (Number.isNaN(numero)) return '–';
    return `${numero.toFixed(2)} m`;
  }

  function formatearFechaHora(fechaStr: string | undefined): string {
    if (!fechaStr) return '–';

    const fecha = new Date(fechaStr);
    if (isNaN(fecha.getTime())) return '–';

    return fecha.toLocaleString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  }

  function obtenerUltimoDato(data: { timestamp: string; level: number }[]) {
    if (!data?.length) return null;
    return data[data.length - 1];
  }

  function obtenerDiferencia(
    observado: { timestamp: string; level: number } | null,
    referencia: { timestamp: string; level: number } | null
  ): string {
    if (!observado || !referencia) return '–';

    const diferencia = Number(observado.level) - Number(referencia.level);
    if (Number.isNaN(diferencia)) return '–';

    const signo = diferencia > 0 ? '+' : '';
    return `${signo}${diferencia.toFixed(2)} m`;
  }

  // =========================================================
  // CARGA DE DATOS
  // =========================================================

  const fetchData = async () => {
    loading = true;
    error = false;

    try {
      const mareographResponse = await fetch("/api/mareograph");
      mareographData = await mareographResponse.json();

      const tideResponse = await fetch("/api/tide_forecast");
      tideForecastData = await tideResponse.json();
    } catch (err) {
      console.error("❌ Error al obtener datos:", err);
      error = true;
      mareographData = [];
      tideForecastData = [];
    } finally {
      loading = false;
    }
  };

  onMount(fetchData);

  // =========================================================
  // DATOS DERIVADOS PARA EL RESUMEN
  // =========================================================

  $: ultimoMareografo = obtenerUltimoDato(mareographData);
  $: ultimaReferencia = obtenerUltimoDato(tideForecastData);
  $: diferenciaActual = obtenerDiferencia(ultimoMareografo, ultimaReferencia);
  $: ultimaActualizacion = ultimoMareografo?.timestamp
    ? formatearFechaHora(ultimoMareografo.timestamp)
    : '–';
</script>

<div class="chart-container">
  <!--
    Encabezado interno más liviano.
    Ya no compite con el título principal del modal.
  -->
  <div class="chart-header">
    <div class="titulo-bloque">
      <p class="subtitulo-seccion">Comparación con referencia naval</p>
      <p class="descripcion">
        La línea azul representa la medición real del mareógrafo y la línea roja punteada muestra
        la referencia de marea para comparar el comportamiento del nivel del mar.
      </p>
    </div>
  </div>

  <!-- Resumen superior -->
  <div class="resumen-grid">
    <article class="resumen-card">
      <span class="resumen-label">Nivel actual</span>
      <strong class="resumen-valor">{formatearNivel(ultimoMareografo?.level)}</strong>
      <span class="resumen-extra">Mareógrafo observado</span>
    </article>

    <article class="resumen-card">
      <span class="resumen-label">Referencia naval</span>
      <strong class="resumen-valor">{formatearNivel(ultimaReferencia?.level)}</strong>
      <span class="resumen-extra">Serie comparativa</span>
    </article>

    <article class="resumen-card">
      <span class="resumen-label">Diferencia</span>
      <strong class="resumen-valor">{diferenciaActual}</strong>
      <span class="resumen-extra">Observado vs referencia</span>
    </article>

    <article class="resumen-card">
      <span class="resumen-label">Última actualización</span>
      <strong class="resumen-valor resumen-valor-fecha">{ultimaActualizacion}</strong>
      <span class="resumen-extra">Hora del dato observado</span>
    </article>
  </div>

  <!-- Estado de carga / error / contenido -->
  {#if loading}
    <p class="estado">Cargando datos del mareógrafo...</p>
  {:else if error}
    <p class="estado error">No se pudieron cargar los datos del mareógrafo en este momento.</p>
  {:else if mareographData.length || tideForecastData.length}
    <GraficoMareografo {mareographData} {tideForecastData} />
  {:else}
    <p class="estado">No hay datos disponibles actualmente.</p>
  {/if}

  <!-- Leyenda -->
  <div class="legend-container">
    <div class="legend-item">
      <div class="legend-color azul"></div>
      <span><strong>Medición real</strong></span>
    </div>

    <div class="legend-item">
      <div class="legend-color roja"></div>
      <span><strong>Referencia naval</strong></span>
    </div>
  </div>
</div>

<style>
  .chart-container {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    width: 100%;
    margin: auto;
    padding: 1rem;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: visible;
  }

  .chart-header {
    width: 100%;
    margin-bottom: 0.9rem;
  }

  .titulo-bloque {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .subtitulo-seccion {
    margin: 0;
    font-size: 0.98rem;
    font-weight: 700;
    color: #1f2937;
  }

  .descripcion {
    margin: 0;
    font-size: 0.93rem;
    color: #4b5563;
    line-height: 1.45;
  }

  .resumen-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.85rem;
    margin-bottom: 1rem;
  }

  .resumen-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.85rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .resumen-label {
    font-size: 0.85rem;
    color: #6b7280;
  }

  .resumen-valor {
    font-size: 1.15rem;
    color: #111827;
  }

  .resumen-valor-fecha {
    font-size: 1rem;
  }

  .resumen-extra {
    font-size: 0.8rem;
    color: #6b7280;
  }

  .estado {
    margin: 1rem 0;
    text-align: center;
    font-size: 0.95rem;
    color: #4b5563;
  }

  .estado.error {
    color: #b91c1c;
  }

  .legend-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 0.75rem;
    justify-content: flex-start;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f4f4f4;
    padding: 6px 10px;
    border-radius: 6px;
  }

  .legend-color {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    flex-shrink: 0;
  }

  .legend-color.azul {
    background: #2563eb;
  }

  .legend-color.roja {
    background: #dc2626;
  }

  @media (max-width: 640px) {
    .chart-container {
      padding: 0.85rem;
    }

    .subtitulo-seccion {
      font-size: 0.92rem;
    }

    .descripcion {
      font-size: 0.86rem;
    }

    .resumen-grid {
      grid-template-columns: 1fr 1fr;
      gap: 0.7rem;
    }

    .resumen-card {
      padding: 0.75rem;
    }

    .resumen-label {
      font-size: 0.8rem;
    }

    .resumen-valor {
      font-size: 1rem;
    }

    .resumen-valor-fecha {
      font-size: 0.92rem;
    }

    .resumen-extra {
      font-size: 0.76rem;
    }

    .legend-container {
      gap: 0.6rem;
    }

    .legend-item {
      font-size: 0.85rem;
    }
  }

  @media (max-width: 420px) {
    .resumen-grid {
      grid-template-columns: 1fr;
    }
  }
</style>