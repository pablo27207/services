<script>
  import { onMount } from 'svelte';

  let plataformas = [];
  let cargando    = true;
  let error       = false;
  let filtroAnio  = '';
  let aniosDisponibles = [];
  let expandidas  = {};

  const NOMBRES = {
    appcr_puerto_cr:                        'Estación Met. Puerto CR',
    appcr_muelle_cc:                        'Estación Met. Muelle CC',
    boya_cidmar_2:                          'Boya CIDMAR-2',
    mareografo_puerto_comodoro_rivadavia:   'Mareógrafo Puerto Comodoro Rivadavia',
    prediccion_de_marea_hidrografia_naval:  'Predicción de Marea – Hidrografía Naval',
    estacion_emac_caleta_cordova_cmd0:      'Estación EMAC – Caleta Córdova CMD0',
  };

  const MESES = [
    '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre',
  ];

  async function cargar() {
    cargando = true; error = false;
    try {
      const params = filtroAnio ? `?year=${filtroAnio}` : '';
      const res = await fetch(`/api/exports/${params}`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      plataformas = data.platforms ?? [];
      // Extraer años únicos de todos los archivos
      const todosAnios = new Set(plataformas.flatMap(p => p.files.map(f => f.year)));
      aniosDisponibles = [...todosAnios].sort((a, b) => b - a);
    } catch {
      error = true;
    } finally {
      cargando = false;
    }
  }

  function togglePlat(slug) {
    expandidas[slug] = !expandidas[slug];
    expandidas = { ...expandidas };
  }

  // Agrupar archivos de una plataforma por año y mes (pares csv+txt juntos)
  function agruparPorPeriodo(files) {
    const mapa = {};
    for (const f of files) {
      const key = `${f.year}-${String(f.month).padStart(2,'0')}`;
      if (!mapa[key]) mapa[key] = { year: f.year, month: f.month, mes: MESES[f.month], archivos: [] };
      mapa[key].archivos.push(f);
    }
    return Object.values(mapa).sort((a, b) => b.year - a.year || b.month - a.month);
  }

  onMount(cargar);
</script>

<section class="descargas">
  <div class="encabezado">
    <p class="sup">Datos abiertos · OOGSJ</p>
    <h2>Descarga de Datos</h2>
    <p class="desc">
      Series históricas mensuales de todas las plataformas del observatorio.
      Disponibles en formato TXT para lectura directa.
    </p>
  </div>

  <!-- Filtro año -->
  <div class="filtros">
    <span class="filtro-label">Filtrar por año:</span>
    {#each aniosDisponibles as anio}
      <button
        class="chip-anio"
        class:activo={filtroAnio === String(anio)}
        on:click={() => { filtroAnio = filtroAnio === String(anio) ? '' : String(anio); cargar(); }}
      >
        {anio}
      </button>
    {/each}
    {#if filtroAnio}
      <button class="chip-clear" on:click={() => { filtroAnio = ''; cargar(); }}>✕ Limpiar</button>
    {/if}
  </div>

  {#if cargando}
    <div class="loading-wrap">
      <div class="spinner"></div>
      <span>Cargando archivos...</span>
    </div>

  {:else if error}
    <div class="estado-msg error">
      <span>⚠️</span> No se pudieron cargar los archivos.
    </div>

  {:else if plataformas.length === 0}
    <div class="estado-msg">
      <span>📂</span> No hay archivos disponibles.
    </div>

  {:else}
    <div class="plats-grid">
      {#each plataformas as plat}
        {@const abierta = !!expandidas[plat.slug]}
        {@const periodos = agruparPorPeriodo(plat.files)}
        {@const nombre = NOMBRES[plat.slug] ?? plat.slug.replace(/_/g, ' ')}

        <div class="plat-card" class:abierta>
          <!-- Cabecera -->
          <button class="plat-header" on:click={() => togglePlat(plat.slug)}>
            <div class="plat-header-left">
              <span class="plat-icono">📡</span>
              <div class="plat-info">
                <span class="plat-nombre">{nombre}</span>
                <span class="plat-meta">{plat.files.length} archivo{plat.files.length !== 1 ? 's' : ''} · {[...new Set(plat.files.map(f => f.year))].sort().join(', ')}</span>
              </div>
            </div>
            <span class="chevron" class:open={abierta}>▾</span>
          </button>

          <!-- Lista de períodos -->
          {#if abierta}
            <div class="periodos">
              {#each periodos as p}
                <div class="periodo-fila">
                  <span class="periodo-label">{p.mes} {p.year}</span>
                  <div class="btns-descarga">
                    {#each p.archivos as f}
                      <a
                        href={f.download_url}
                        class="btn-dl fmt-{f.format}"
                        download
                        title="Descargar {f.filename} ({f.size_human})"
                      >
                        ↓ {f.format.toUpperCase()}
                        <span class="btn-size">{f.size_human}</span>
                      </a>
                    {/each}
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      {/each}
    </div>

    <p class="nota">
      Los datos son de libre uso con atribución al Observatorio Oceanográfico del Golfo San Jorge (OOGSJ).
    </p>
  {/if}
</section>

<style>
  .descargas {
    background: linear-gradient(180deg, #f2f7fb 0%, #ffffff 100%);
    padding: 4rem 1.5rem 5rem;
  }

  /* ── Encabezado ── */
  .encabezado {
    text-align: center;
    max-width: 700px;
    margin: 0 auto 2.5rem;
  }

  .sup {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #0d6ea8;
    margin: 0 0 0.6rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .sup::before,
  .sup::after {
    content: '';
    display: inline-block;
    width: 28px;
    height: 1.5px;
    background: #0d6ea8;
    opacity: 0.4;
  }

  h2 {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 900;
    color: #09263a;
    margin: 0 0 0.85rem;
    letter-spacing: -0.02em;
    line-height: 1.1;
  }

  .desc {
    color: #4f6575;
    font-size: 1rem;
    line-height: 1.7;
    margin: 0;
  }

  /* ── Filtros ── */
  .filtros {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin-bottom: 2rem;
  }

  .filtro-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #6a8090;
    margin-right: 0.25rem;
  }

  .chip-anio {
    padding: 0.3rem 0.8rem;
    border-radius: 99px;
    border: 1.5px solid #c8dce8;
    background: white;
    color: #3a5060;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .chip-anio:hover { background: #eef6fb; border-color: #0d6ea8; color: #0d6ea8; }
  .chip-anio.activo { background: #0d6ea8; border-color: #0d6ea8; color: white; }

  .chip-clear {
    padding: 0.3rem 0.75rem;
    border-radius: 99px;
    border: 1.5px solid #f5c6c2;
    background: #fdf0ef;
    color: #9b2020;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
  }

  .chip-clear:hover { background: #f5c6c2; }

  /* ── Loading / error ── */
  .loading-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 3rem;
    color: #6a8090;
  }

  .spinner {
    width: 28px; height: 28px;
    border: 3px solid #dde8f0;
    border-top-color: #0d6ea8;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .estado-msg {
    text-align: center;
    padding: 3rem;
    color: #6a8090;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .estado-msg.error { color: #9b2020; }

  /* ── Grid de plataformas ── */
  .plats-grid {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .plat-card {
    background: white;
    border: 1.5px solid rgba(9,38,58,0.08);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 2px 14px rgba(9,38,58,0.06);
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .plat-card.abierta {
    border-color: #0d6ea8;
    box-shadow: 0 6px 24px rgba(13,110,168,0.12);
  }

  /* Cabecera de plataforma */
  .plat-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1.1rem 1.4rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    transition: background 0.15s;
  }

  .plat-header:hover { background: #f4f9fc; }

  .plat-header-left {
    display: flex;
    align-items: center;
    gap: 0.85rem;
  }

  .plat-icono { font-size: 1.3rem; flex-shrink: 0; }

  .plat-info {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .plat-nombre {
    font-size: 0.97rem;
    font-weight: 700;
    color: #09263a;
    line-height: 1.2;
  }

  .plat-card.abierta .plat-nombre { color: #0d6ea8; }

  .plat-meta {
    font-size: 0.78rem;
    color: #8a9ba5;
  }

  .chevron {
    font-size: 1.1rem;
    color: #a0b1bd;
    transition: transform 0.25s ease, color 0.2s;
    flex-shrink: 0;
    line-height: 1;
  }

  .chevron.open { transform: rotate(180deg); color: #0d6ea8; }

  /* Períodos */
  .periodos {
    border-top: 1px solid #edf2f5;
    padding: 0.5rem 0;
  }

  .periodo-fila {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.55rem 1.4rem;
    transition: background 0.12s;
    flex-wrap: wrap;
  }

  .periodo-fila:hover { background: #f8fbfd; }

  .periodo-label {
    font-size: 0.88rem;
    font-weight: 600;
    color: #3a5060;
    min-width: 130px;
  }

  .btns-descarga {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .btn-dl {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.8rem;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 700;
    text-decoration: none;
    transition: background 0.15s;
    white-space: nowrap;
  }

  .fmt-csv { background: #e4f5ec; color: #1a7a4a; }
  .fmt-csv:hover { background: #c8edda; }

  .fmt-txt { background: #e8efff; color: #2a4aaa; }
  .fmt-txt:hover { background: #ccdaff; }

  .btn-size {
    font-weight: 400;
    opacity: 0.75;
    font-size: 0.72rem;
  }

  /* Nota legal */
  .nota {
    max-width: 1100px;
    margin: 1.75rem auto 0;
    padding: 0.9rem 1.25rem;
    background: #f0f7fb;
    border-radius: 12px;
    border-left: 3px solid #8fd3ff;
    font-size: 0.85rem;
    color: #4f6575;
    font-style: italic;
    line-height: 1.6;
  }

  /* ── Mobile ── */
  @media (max-width: 600px) {
    .descargas { padding: 3rem 1rem 4rem; }
    .plat-header { padding: 0.9rem 1rem; }
    .periodo-fila { padding: 0.55rem 1rem; }
    .periodo-label { min-width: unset; width: 100%; }
    .btns-descarga { width: 100%; }
  }
</style>
