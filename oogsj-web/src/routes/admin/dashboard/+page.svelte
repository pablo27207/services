<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore, type AdminUser } from '$lib/stores/auth';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';

  // ── tipos ────────────────────────────────────────────────
  type Stats = {
    mediciones:          { total: number; ultimas_24h: number; ultima_hora: number; ultima_ts: string | null };
    plataformas_activas: number;
    avisos:              { total: number; ultimos_30d: number; ultimo: { numero: string; fecha: string; scraped_at: string } | null };
    documentos:          number;
  };

  type Plataforma = {
    id: number; nombre: string; tipo: string; sensores: number;
    ultima_transmision: string | null; horas_sin_datos: number | null;
    total_mediciones: number; mediciones_24h: number;
    estado: 'ok' | 'alerta' | 'sin_datos';
  };

  // ── estado ───────────────────────────────────────────────
  let user: AdminUser | null = null;
  let stats: Stats | null    = null;
  let plats: Plataforma[]    = [];
  let cargando               = true;
  let errorMsg               = '';

  const unsub = authStore.subscribe(s => { user = s.user; });

  async function cargarDatos() {
    cargando = true; errorMsg = '';
    try {
      const [r1, r2] = await Promise.all([
        fetch('/api/admin/stats',       { credentials: 'include' }),
        fetch('/api/admin/plataformas', { credentials: 'include' }),
      ]);
      if (r1.status === 401 || r2.status === 401) { goto('/login'); return; }
      stats = await r1.json();
      const d2 = await r2.json();
      plats = d2.plataformas ?? [];
    } catch {
      errorMsg = 'No se pudieron cargar los datos del sistema.';
    } finally {
      cargando = false;
    }
  }

  // ── helpers ──────────────────────────────────────────────
  function fmtNum(n: number | undefined | null): string {
    if (n == null) return '—';
    return n.toLocaleString('es-AR');
  }

  function fmtTs(iso: string | null): string {
    if (!iso) return 'Sin datos';
    const d = new Date(iso);
    return d.toLocaleString('es-AR', { day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' });
  }

  function fmtHoras(h: number | null): string {
    if (h == null) return '—';
    if (h < 1) return `${Math.round(h * 60)} min`;
    if (h < 24) return `${h.toFixed(0)} h`;
    return `${(h / 24).toFixed(1)} días`;
  }

  onMount(() => { cargarDatos(); });
  onDestroy(() => unsub());
</script>

<div class="admin-shell">

  <!-- ══ Sidebar ══ -->
  <AdminSidebar {user} />

  <!-- ══ Main ══ -->
  <main class="main-content">

    <header class="main-header">
      <div>
        <h1>Dashboard</h1>
        <p>Observatorio Oceanográfico del Golfo San Jorge</p>
      </div>
      <div class="header-actions">
        <button class="btn-refresh" on:click={cargarDatos} disabled={cargando} title="Actualizar">
          <svg class:girando={cargando} width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M23 4v6h-6"/><path d="M1 20v-6h6"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          Actualizar
        </button>
        <div class="status-badge">
          <span class="status-dot"></span>
          Sistema operativo
        </div>
      </div>
    </header>

    {#if errorMsg}
      <div class="error-banner">{errorMsg}</div>
    {/if}

    {#if cargando}
      <div class="loading-grid">
        {#each Array(4) as _}
          <div class="skeleton-card"></div>
        {/each}
      </div>
    {:else}

      <!-- ── Stat cards ── -->
      <div class="cards-grid">
        <div class="stat-card">
          <div class="stat-icon">🗄️</div>
          <div class="stat-body">
            <span class="stat-label">Total mediciones</span>
            <span class="stat-value">{fmtNum(stats?.mediciones.total)}</span>
            <span class="stat-sub">Desde {stats?.mediciones.ultima_ts ? new Date(stats.mediciones.ultima_ts).getFullYear() - 1 : '—'}</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">📥</div>
          <div class="stat-body">
            <span class="stat-label">Últimas 24 h</span>
            <span class="stat-value">{fmtNum(stats?.mediciones.ultimas_24h)}</span>
            <span class="stat-sub">{fmtNum(stats?.mediciones.ultima_hora)} en la última hora</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">📡</div>
          <div class="stat-body">
            <span class="stat-label">Plataformas activas</span>
            <span class="stat-value">{stats?.plataformas_activas ?? '—'}</span>
            <span class="stat-sub">Con datos en DB</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⚠️</div>
          <div class="stat-body">
            <span class="stat-label">Avisos navegante</span>
            <span class="stat-value">{fmtNum(stats?.avisos.ultimos_30d)}</span>
            <span class="stat-sub">Últimos 30 días · {fmtNum(stats?.avisos.total)} total</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-body">
            <span class="stat-label">Documentos</span>
            <span class="stat-value">{fmtNum(stats?.documentos)}</span>
            <span class="stat-sub">En biblioteca científica</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">🕐</div>
          <div class="stat-body">
            <span class="stat-label">Última medición</span>
            <span class="stat-value-sm">{fmtTs(stats?.mediciones.ultima_ts ?? null)}</span>
            <span class="stat-sub">Timestamp más reciente</span>
          </div>
        </div>
      </div>

      <!-- ── Plataformas ── -->
      <section class="seccion">
        <h2 class="seccion-titulo">
          <span>📡</span> Estado de plataformas
          <span class="seccion-sub">Última transmisión por plataforma</span>
        </h2>

        <div class="plats-table-wrap">
          <table class="plats-table">
            <thead>
              <tr>
                <th>Plataforma</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Última transmisión</th>
                <th>Tiempo sin datos</th>
                <th>Últ. 24 h</th>
                <th>Total</th>
                <th>Sensores</th>
              </tr>
            </thead>
            <tbody>
              {#each plats as p}
                <tr>
                  <td class="plat-nombre">{p.nombre}</td>
                  <td class="plat-tipo">{p.tipo}</td>
                  <td>
                    <span class="estado-badge estado-{p.estado}">
                      {#if p.estado === 'ok'}        ● Activa
                      {:else if p.estado === 'alerta'} ● Alerta
                      {:else}                           ● Sin datos
                      {/if}
                    </span>
                  </td>
                  <td class="ts-cell">{fmtTs(p.ultima_transmision)}</td>
                  <td class="td-right {p.estado !== 'ok' ? 'texto-alerta' : ''}">
                    {fmtHoras(p.horas_sin_datos)}
                  </td>
                  <td class="td-right">{fmtNum(p.mediciones_24h)}</td>
                  <td class="td-right">{fmtNum(p.total_mediciones)}</td>
                  <td class="td-right">{p.sensores}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </section>

      <!-- ── Último aviso ── -->
      {#if stats?.avisos.ultimo}
        <section class="seccion">
          <h2 class="seccion-titulo">
            <span>📋</span> Último aviso al navegante scrapeado
          </h2>
          <div class="aviso-card">
            <div class="aviso-row">
              <span class="aviso-label">Número</span>
              <span class="aviso-val">{stats.avisos.ultimo.numero}</span>
            </div>
            <div class="aviso-row">
              <span class="aviso-label">Fecha del aviso</span>
              <span class="aviso-val">{fmtTs(stats.avisos.ultimo.fecha)}</span>
            </div>
            <div class="aviso-row">
              <span class="aviso-label">Scrapeado en</span>
              <span class="aviso-val">{fmtTs(stats.avisos.ultimo.scraped_at)}</span>
            </div>
          </div>
        </section>
      {/if}

    {/if}
  </main>
</div>

<style>
  /* ── Shell ── */
  .admin-shell {
    display: flex;
    min-height: 100vh;
    background: #f2f6f9;
    font-family: system-ui, sans-serif;
  }

  /* ── Main ── */
  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.75rem;
    padding: 2rem;
    min-width: 0;
  }

  /* ── Header ── */
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

  .header-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

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
    transition: background 0.2s, border-color 0.2s;
  }

  .btn-refresh:hover:not(:disabled) { background: #eef6fb; border-color: #0d6ea8; color: #0d6ea8; }
  .btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }

  .btn-refresh svg { transition: transform 0.6s linear; }
  .btn-refresh .girando { animation: girar 0.8s linear infinite; }
  @keyframes girar { to { transform: rotate(360deg); } }

  .status-badge {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    color: #2ecc71;
    font-weight: 600;
    background: rgba(46,204,113,0.1);
    border: 1px solid rgba(46,204,113,0.25);
    border-radius: 99px;
    padding: 0.35rem 0.85rem;
  }

  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #2ecc71;
    animation: pulso 2s ease infinite;
  }

  @keyframes pulso { 0%,100%{opacity:1} 50%{opacity:0.35} }

  .error-banner {
    background: #fdf0ef;
    border: 1px solid #f5c6c2;
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    color: #9b2020;
    font-size: 0.88rem;
  }

  /* ── Skeleton loader ── */
  .loading-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
  }

  .skeleton-card {
    height: 96px;
    border-radius: 18px;
    background: linear-gradient(90deg, #e8eef2 25%, #f4f8fb 50%, #e8eef2 75%);
    background-size: 200% 100%;
    animation: shimmer 1.2s infinite;
  }

  @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

  /* ── Stat cards ── */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .stat-card {
    background: white;
    border-radius: 18px;
    padding: 1.2rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 2px 12px rgba(9,38,58,0.06);
    border: 1px solid rgba(9,38,58,0.06);
  }

  .stat-icon { font-size: 1.75rem; flex-shrink: 0; }

  .stat-body {
    display: flex;
    flex-direction: column;
    gap: 0.12rem;
    min-width: 0;
  }

  .stat-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
  }

  .stat-value {
    font-size: 1.55rem;
    font-weight: 800;
    color: #09263a;
    line-height: 1;
  }

  .stat-value-sm {
    font-size: 0.92rem;
    font-weight: 700;
    color: #09263a;
    line-height: 1.3;
  }

  .stat-sub { font-size: 0.72rem; color: #9aafba; }

  /* ── Secciones ── */
  .seccion {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .seccion-titulo {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 0;
    font-size: 1rem;
    font-weight: 700;
    color: #09263a;
  }

  .seccion-sub {
    font-size: 0.8rem;
    font-weight: 400;
    color: #8a9ba5;
    margin-left: 0.25rem;
  }

  /* ── Tabla plataformas ── */
  .plats-table-wrap {
    background: white;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(9,38,58,0.06);
    border: 1px solid rgba(9,38,58,0.06);
    overflow-x: auto;
  }

  .plats-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }

  .plats-table thead tr {
    border-bottom: 1.5px solid #edf2f5;
  }

  .plats-table th {
    padding: 0.85rem 1rem;
    text-align: left;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
    white-space: nowrap;
  }

  .plats-table tbody tr {
    border-bottom: 1px solid #f0f5f8;
    transition: background 0.15s;
  }

  .plats-table tbody tr:last-child { border-bottom: none; }
  .plats-table tbody tr:hover      { background: #f8fbfd; }

  .plats-table td {
    padding: 0.85rem 1rem;
    color: #2a3f4f;
    vertical-align: middle;
  }

  .plat-nombre { font-weight: 600; color: #09263a; }
  .plat-tipo   { font-size: 0.8rem; color: #6a8090; }
  .ts-cell     { font-size: 0.82rem; color: #4f6575; font-family: monospace; }
  .td-right    { text-align: right; font-variant-numeric: tabular-nums; }
  .texto-alerta { color: #c0392b; font-weight: 600; }

  /* Estado badges */
  .estado-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 99px;
    padding: 0.25rem 0.65rem;
    white-space: nowrap;
  }

  .estado-ok        { background: #d4f5e4; color: #1a7a4a; }
  .estado-alerta    { background: #fef3cd; color: #8a5a00; }
  .estado-sin_datos { background: #f0f0f0; color: #6a6a6a; }

  /* ── Último aviso ── */
  .aviso-card {
    background: white;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 12px rgba(9,38,58,0.06);
    border: 1px solid rgba(9,38,58,0.06);
    display: flex;
    flex-wrap: wrap;
    gap: 1rem 2rem;
  }

  .aviso-row { display: flex; flex-direction: column; gap: 0.2rem; }
  .aviso-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
  }
  .aviso-val { font-size: 0.95rem; font-weight: 600; color: #09263a; }

  /* ── Responsive ── */
  @media (max-width: 1100px) {
    .cards-grid { grid-template-columns: repeat(2, 1fr); }
  }

  @media (max-width: 700px) {
    .admin-shell  { flex-direction: column; }
    .cards-grid   { grid-template-columns: 1fr 1fr; }
    .main-content { padding: 1rem; gap: 1.25rem; }
  }

  @media (max-width: 480px) {
    .cards-grid { grid-template-columns: 1fr; }
  }
</style>
