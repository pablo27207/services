<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore, type AdminUser } from '$lib/stores/auth';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';

  type ExportFile = {
    filename: string;
    format: 'csv' | 'txt';
    year: number;
    month: number;
    month_name: string;
    size_human: string;
    generated_at: string;
    download_url: string;
  };

  type Platform = { slug: string; files: ExportFile[] };

  let user: AdminUser | null = null;
  let platforms: Platform[]  = [];
  let totalFiles             = 0;
  let cargando               = true;
  let errorMsg               = '';
  let filtroAnio             = '';
  let filtroPlat             = '';
  let expandedSlug: string | null = null;

  const unsub = authStore.subscribe(s => { user = s.user; });

  async function cargar() {
    cargando = true; errorMsg = '';
    try {
      const params = new URLSearchParams();
      if (filtroAnio) params.set('year', filtroAnio);
      if (filtroPlat) params.set('platform', filtroPlat);
      const res = await fetch(`/api/exports/?${params}`, { credentials: 'include' });
      if (!res.ok) throw new Error();
      const data = await res.json();
      platforms  = data.platforms ?? [];
      totalFiles = data.total_files ?? 0;
    } catch {
      errorMsg = 'No se pudieron cargar los archivos de exportación.';
    } finally {
      cargando = false;
    }
  }

  function fmtFecha(iso: string): string {
    if (!iso) return '—';
    return new Date(iso).toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }

  function slugLabel(slug: string): string {
    return slug.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  }

  function togglePlatform(slug: string) {
    expandedSlug = expandedSlug === slug ? null : slug;
  }

  $: anios = [...new Set(platforms.flatMap(p => p.files.map(f => f.year)))].sort((a, b) => b - a);

  onMount(() => { cargar(); });
  onDestroy(() => unsub());
</script>

<div class="admin-shell">
  <AdminSidebar {user} />

  <main class="main-content">

    <header class="main-header">
      <div>
        <h1>Archivos de Exportación</h1>
        <p>Descarga de datos históricos por plataforma y mes · {totalFiles} archivos disponibles</p>
      </div>
      <button class="btn-refresh" on:click={cargar} disabled={cargando}>
        <svg class:girando={cargando} width="16" height="16" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M23 4v6h-6"/><path d="M1 20v-6h6"/>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
        </svg>
        Actualizar
      </button>
    </header>

    {#if errorMsg}
      <div class="error-banner">{errorMsg}</div>
    {/if}

    <!-- Filtros -->
    <div class="filtros">
      <label class="filtro-item">
        <span>Año</span>
        <select bind:value={filtroAnio} on:change={cargar}>
          <option value="">Todos</option>
          {#each anios as anio}
            <option value={String(anio)}>{anio}</option>
          {/each}
        </select>
      </label>
      <label class="filtro-item">
        <span>Plataforma</span>
        <select bind:value={filtroPlat} on:change={cargar}>
          <option value="">Todas</option>
          {#each platforms as p}
            <option value={p.slug}>{slugLabel(p.slug)}</option>
          {/each}
        </select>
      </label>
    </div>

    {#if cargando}
      <div class="skeletons">
        {#each Array(4) as _}
          <div class="skeleton-bloque"></div>
        {/each}
      </div>

    {:else if platforms.length === 0}
      <div class="vacio">
        <span>📁</span>
        <p>No hay archivos de exportación disponibles.</p>
      </div>

    {:else}
      <div class="plataformas-lista">
        {#each platforms as p}
          {@const abierto = expandedSlug === p.slug}
          <div class="plat-bloque" class:abierto>

            <!-- Encabezado del grupo -->
            <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
            <div class="plat-header" on:click={() => togglePlatform(p.slug)}>
              <div class="plat-header-left">
                <span class="plat-arrow" class:open={abierto}>▶</span>
                <span class="plat-nombre">{slugLabel(p.slug)}</span>
                <span class="plat-count">{p.files.length} archivos</span>
              </div>
              <div class="plat-header-right">
                {#each [...new Set(p.files.map(f => f.year))].sort((a,b) => b-a).slice(0,3) as y}
                  <span class="year-chip">{y}</span>
                {/each}
              </div>
            </div>

            <!-- Lista de archivos -->
            {#if abierto}
              <div class="archivos-tabla-wrap">
                <table class="archivos-tabla">
                  <thead>
                    <tr>
                      <th>Período</th>
                      <th>Archivo</th>
                      <th>Formato</th>
                      <th>Tamaño</th>
                      <th>Generado</th>
                      <th>Descargar</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each [...p.files].reverse() as f}
                      <tr>
                        <td class="td-periodo">{f.month_name} {f.year}</td>
                        <td class="td-filename">{f.filename}</td>
                        <td>
                          <span class="fmt-badge fmt-{f.format}">{f.format.toUpperCase()}</span>
                        </td>
                        <td class="td-size">{f.size_human}</td>
                        <td class="td-fecha">{fmtFecha(f.generated_at)}</td>
                        <td>
                          <a href={f.download_url} class="btn-download" download>
                            ↓ Descargar
                          </a>
                        </td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
            {/if}

          </div>
        {/each}
      </div>
    {/if}

  </main>
</div>

<style>
  .admin-shell {
    display: flex;
    min-height: 100vh;
    background: #f2f6f9;
    font-family: system-ui, sans-serif;
  }

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 2rem;
    min-width: 0;
  }

  .main-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .main-header h1 {
    margin: 0 0 0.2rem;
    font-size: 1.65rem;
    color: #09263a;
    font-weight: 800;
  }

  .main-header p { margin: 0; color: #6a8090; font-size: 0.88rem; }

  .btn-refresh {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 0.9rem;
    border-radius: 99px;
    border: 1.5px solid #c8dce8;
    background: white;
    color: #3a5060;
    font-size: 0.83rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-refresh:hover:not(:disabled) { background: #eef6fb; border-color: #0d6ea8; color: #0d6ea8; }
  .btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-refresh svg { transition: transform 0.6s; }
  .btn-refresh .girando { animation: girar 0.8s linear infinite; }
  @keyframes girar { to { transform: rotate(360deg); } }

  .error-banner {
    background: #fdf0ef;
    border: 1px solid #f5c6c2;
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    color: #9b2020;
    font-size: 0.88rem;
  }

  /* Filtros */
  .filtros {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .filtro-item {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .filtro-item span {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
  }

  .filtro-item select {
    border: 1.5px solid #d4e2ea;
    border-radius: 10px;
    padding: 0.45rem 0.85rem;
    font-size: 0.88rem;
    color: #09263a;
    background: white;
    cursor: pointer;
    outline: none;
    transition: border-color 0.2s;
    min-width: 160px;
  }

  .filtro-item select:focus { border-color: #0d6ea8; }

  /* Skeleton */
  .skeletons { display: flex; flex-direction: column; gap: 0.75rem; }

  .skeleton-bloque {
    height: 64px;
    border-radius: 14px;
    background: linear-gradient(90deg, #e8eef2 25%, #f4f8fb 50%, #e8eef2 75%);
    background-size: 200% 100%;
    animation: shimmer 1.2s infinite;
  }

  @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

  /* Vacío */
  .vacio {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    padding: 4rem;
    color: #6a8090;
  }

  .vacio span { font-size: 2.5rem; }

  /* Plataformas */
  .plataformas-lista { display: flex; flex-direction: column; gap: 0.75rem; }

  .plat-bloque {
    background: white;
    border: 1.5px solid rgba(9,38,58,0.07);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(9,38,58,0.05);
  }

  .plat-bloque.abierto { border-color: #0d6ea8; }

  .plat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.25rem;
    cursor: pointer;
    transition: background 0.15s;
    flex-wrap: wrap;
  }

  .plat-header:hover { background: #f4f9fc; }

  .plat-header-left {
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .plat-arrow {
    font-size: 0.6rem;
    color: #8a9ba5;
    transition: transform 0.2s;
    flex-shrink: 0;
  }

  .plat-arrow.open { transform: rotate(90deg); color: #0d6ea8; }

  .plat-nombre {
    font-size: 0.95rem;
    font-weight: 700;
    color: #09263a;
  }

  .plat-count {
    font-size: 0.78rem;
    color: #8a9ba5;
    background: #f0f5f8;
    border-radius: 99px;
    padding: 0.15rem 0.55rem;
  }

  .plat-header-right { display: flex; gap: 0.4rem; flex-wrap: wrap; }

  .year-chip {
    font-size: 0.72rem;
    font-weight: 700;
    color: #0d6ea8;
    background: #e8f4fc;
    border-radius: 99px;
    padding: 0.15rem 0.5rem;
  }

  /* Tabla archivos */
  .archivos-tabla-wrap {
    overflow-x: auto;
    border-top: 1px solid #edf2f5;
  }

  .archivos-tabla {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }

  .archivos-tabla thead tr { border-bottom: 1px solid #edf2f5; }

  .archivos-tabla th {
    padding: 0.65rem 1rem;
    text-align: left;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
    white-space: nowrap;
    background: #f8fbfd;
  }

  .archivos-tabla tbody tr {
    border-bottom: 1px solid #f0f5f8;
    transition: background 0.12s;
  }

  .archivos-tabla tbody tr:last-child { border-bottom: none; }
  .archivos-tabla tbody tr:hover { background: #f4f9fc; }

  .archivos-tabla td {
    padding: 0.7rem 1rem;
    color: #2a3f4f;
    vertical-align: middle;
  }

  .td-periodo { font-weight: 600; color: #09263a; white-space: nowrap; }
  .td-filename { font-family: monospace; font-size: 0.78rem; color: #4f6575; }
  .td-size { font-variant-numeric: tabular-nums; color: #6a8090; }
  .td-fecha { white-space: nowrap; color: #7a8f9b; font-size: 0.8rem; }

  .fmt-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    border-radius: 6px;
    padding: 0.15rem 0.5rem;
  }

  .fmt-csv { background: #e8f8ef; color: #1a7a4a; }
  .fmt-txt { background: #eef0fb; color: #3a4aaa; }

  .btn-download {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.3rem 0.75rem;
    border-radius: 8px;
    background: #eef6fb;
    color: #0d6ea8;
    font-size: 0.8rem;
    font-weight: 700;
    text-decoration: none;
    transition: background 0.2s;
    white-space: nowrap;
  }

  .btn-download:hover { background: #d8eef8; }

  @media (max-width: 700px) {
    .admin-shell  { flex-direction: column; }
    .main-content { padding: 1rem; gap: 1.25rem; }
  }
</style>
