<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore, type AdminUser } from '$lib/stores/auth';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';

  // ── tipos ────────────────────────────────────────────────
  type Documento = {
    id:           number;
    title:        string;
    year:         number | null;
    venue:        string | null;
    citations:    number;
    doi:          string | null;
    url:          string | null;
    storage_path: string | null;
    created_at:   string | null;
  };

  // ── estado ───────────────────────────────────────────────
  let user: AdminUser | null = null;
  let docs: Documento[]      = [];
  let total                  = 0;
  let page                   = 1;
  const limit                = 20;
  let cargando               = true;
  let errorMsg               = '';

  // ── upload modal ─────────────────────────────────────────
  let modalAbierto = false;
  let uploading    = false;
  let uploadError  = '';
  let uploadOk     = false;

  let titulo   = '';
  let anio     = '';
  let venue    = '';
  let doi      = '';
  let url      = '';
  let autores  = '';
  let archivo: FileList | null = null;

  const unsub = authStore.subscribe(s => { user = s.user; });

  async function cargarDocs() {
    cargando = true; errorMsg = '';
    try {
      const offset = (page - 1) * limit;
      const res = await fetch(
        `/api/library/admin/list?page=${page}&limit=${limit}`,
        { credentials: 'include' }
      );
      if (!res.ok) throw new Error();
      const data = await res.json();
      docs  = data.items ?? [];
      total = data.total ?? docs.length;
    } catch {
      errorMsg = 'No se pudieron cargar los documentos.';
    } finally {
      cargando = false;
    }
  }

  async function subirDocumento() {
    if (!archivo || !archivo[0]) { uploadError = 'Seleccioná un archivo PDF.'; return; }
    if (!titulo.trim())           { uploadError = 'El título es obligatorio.'; return; }

    uploading = true; uploadError = '';
    const fd = new FormData();
    fd.append('file',    archivo[0]);
    fd.append('title',   titulo.trim());
    if (anio.trim())   fd.append('year',    anio.trim());
    if (venue.trim())  fd.append('venue',   venue.trim());
    if (doi.trim())    fd.append('doi',     doi.trim());
    if (url.trim())    fd.append('url',     url.trim());
    if (autores.trim()) fd.append('authors', autores.trim());

    try {
      const res = await fetch('/api/library/upload', {
        method: 'POST',
        credentials: 'include',
        body: fd,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? 'Error al subir');
      uploadOk = true;
      resetForm();
      await cargarDocs();
      setTimeout(() => { uploadOk = false; }, 3000);
    } catch (e: any) {
      uploadError = e?.message ?? 'Error al subir el documento';
    } finally {
      uploading = false;
    }
  }

  function resetForm() {
    titulo = ''; anio = ''; venue = ''; doi = ''; url = ''; autores = '';
    archivo = null;
    modalAbierto = false;
  }

  function prevPagina() { if (page > 1) { page--; cargarDocs(); } }
  function nextPagina() { if (page * limit < total) { page++; cargarDocs(); } }

  function fmtFecha(iso: string | null): string {
    if (!iso) return '—';
    return new Date(iso).toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }

  onMount(() => { cargarDocs(); });
  onDestroy(() => unsub());
</script>

<div class="admin-shell">
  <AdminSidebar {user} />

  <main class="main-content">

    <header class="main-header">
      <div>
        <h1>Biblioteca</h1>
        <p>Gestión de documentos científicos · {total} documento{total !== 1 ? 's' : ''}</p>
      </div>
      <button class="btn-subir" on:click={() => { modalAbierto = true; uploadError = ''; uploadOk = false; }}>
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Subir documento
      </button>
    </header>

    {#if errorMsg}
      <div class="error-banner">{errorMsg}</div>
    {/if}

    {#if cargando}
      <div class="skeleton-tabla">
        {#each Array(6) as _}
          <div class="skeleton-fila"></div>
        {/each}
      </div>
    {:else if docs.length === 0}
      <div class="vacio">
        <span>📚</span>
        <p>No hay documentos en la biblioteca.</p>
      </div>
    {:else}
      <div class="tabla-wrap">
        <table class="tabla">
          <thead>
            <tr>
              <th>ID</th>
              <th>Título</th>
              <th>Año</th>
              <th>Venue</th>
              <th>DOI</th>
              <th>Archivo</th>
              <th>Cargado</th>
            </tr>
          </thead>
          <tbody>
            {#each docs as doc (doc.id)}
              <tr>
                <td class="td-id">{doc.id}</td>
                <td class="td-titulo">
                  {#if doc.url}
                    <a href={doc.url} target="_blank" rel="noopener noreferrer">{doc.title}</a>
                  {:else}
                    {doc.title}
                  {/if}
                </td>
                <td class="td-center">{doc.year ?? '—'}</td>
                <td class="td-venue">{doc.venue ?? '—'}</td>
                <td class="td-doi">
                  {#if doc.doi}
                    <span class="badge-doi">{doc.doi.slice(0, 20)}{doc.doi.length > 20 ? '…' : ''}</span>
                  {:else}
                    <span class="sin-doi">—</span>
                  {/if}
                </td>
                <td class="td-center">
                  {#if doc.storage_path}
                    <a href="/api/library/file/{doc.id}" target="_blank" class="badge-pdf">PDF</a>
                  {:else}
                    <span class="sin-archivo">—</span>
                  {/if}
                </td>
                <td class="td-fecha">{fmtFecha(doc.created_at)}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>

      <!-- Paginación -->
      {#if total > limit}
        <div class="paginacion">
          <button class="btn-pag" on:click={prevPagina} disabled={page === 1}>← Anterior</button>
          <span class="pag-info">Página {page} de {Math.ceil(total / limit)}</span>
          <button class="btn-pag" on:click={nextPagina} disabled={page * limit >= total}>Siguiente →</button>
        </div>
      {/if}
    {/if}

  </main>
</div>

<!-- ══ Modal upload ══ -->
{#if modalAbierto}
  <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
  <div class="modal-overlay" on:click|self={resetForm}>
    <div class="modal">
      <div class="modal-header">
        <h2>Subir documento</h2>
        <button class="btn-cerrar" on:click={resetForm} aria-label="Cerrar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      {#if uploadOk}
        <div class="upload-ok">✓ Documento subido correctamente</div>
      {/if}

      {#if uploadError}
        <div class="upload-error">{uploadError}</div>
      {/if}

      <form on:submit|preventDefault={subirDocumento} class="modal-form">
        <label class="field">
          <span>Archivo PDF <em>*</em></span>
          <input type="file" accept=".pdf,application/pdf" bind:files={archivo} disabled={uploading} />
        </label>

        <label class="field">
          <span>Título <em>*</em></span>
          <input type="text" bind:value={titulo} placeholder="Título del documento" disabled={uploading} />
        </label>

        <div class="field-row">
          <label class="field">
            <span>Año</span>
            <input type="number" bind:value={anio} placeholder="2024" min="1900" max="2100" disabled={uploading} />
          </label>
          <label class="field">
            <span>Revista / Venue</span>
            <input type="text" bind:value={venue} placeholder="Journal of..." disabled={uploading} />
          </label>
        </div>

        <label class="field">
          <span>Autores <small>(separados por punto y coma)</small></span>
          <input type="text" bind:value={autores} placeholder="García, F.; López, M." disabled={uploading} />
        </label>

        <div class="field-row">
          <label class="field">
            <span>DOI</span>
            <input type="text" bind:value={doi} placeholder="10.1000/xyz123" disabled={uploading} />
          </label>
          <label class="field">
            <span>URL externa</span>
            <input type="url" bind:value={url} placeholder="https://..." disabled={uploading} />
          </label>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-cancelar" on:click={resetForm} disabled={uploading}>
            Cancelar
          </button>
          <button type="submit" class="btn-confirmar" disabled={uploading}>
            {#if uploading}
              <span class="spinner-sm"></span> Subiendo...
            {:else}
              Subir documento
            {/if}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}

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

  .btn-subir {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.55rem 1.1rem;
    border-radius: 10px;
    border: none;
    background: #0d6ea8;
    color: white;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-subir:hover { background: #0a5a8a; }

  /* ── Error ── */
  .error-banner {
    background: #fdf0ef;
    border: 1px solid #f5c6c2;
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    color: #9b2020;
    font-size: 0.88rem;
  }

  /* ── Skeleton ── */
  .skeleton-tabla {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .skeleton-fila {
    height: 52px;
    border-radius: 10px;
    background: linear-gradient(90deg, #e8eef2 25%, #f4f8fb 50%, #e8eef2 75%);
    background-size: 200% 100%;
    animation: shimmer 1.2s infinite;
  }

  @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

  /* ── Vacío ── */
  .vacio {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    padding: 4rem;
    color: #6a8090;
    font-size: 1rem;
  }

  .vacio span { font-size: 2.5rem; }

  /* ── Tabla ── */
  .tabla-wrap {
    background: white;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(9,38,58,0.06);
    border: 1px solid rgba(9,38,58,0.06);
    overflow-x: auto;
  }

  .tabla {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }

  .tabla thead tr { border-bottom: 1.5px solid #edf2f5; }

  .tabla th {
    padding: 0.85rem 1rem;
    text-align: left;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
    white-space: nowrap;
  }

  .tabla tbody tr {
    border-bottom: 1px solid #f0f5f8;
    transition: background 0.15s;
  }

  .tabla tbody tr:last-child { border-bottom: none; }
  .tabla tbody tr:hover      { background: #f8fbfd; }

  .tabla td {
    padding: 0.8rem 1rem;
    color: #2a3f4f;
    vertical-align: middle;
  }

  .td-id     { font-size: 0.8rem; color: #8a9ba5; font-variant-numeric: tabular-nums; }
  .td-titulo { font-weight: 500; color: #09263a; max-width: 340px; }
  .td-titulo a { color: #0d6ea8; text-decoration: none; }
  .td-titulo a:hover { text-decoration: underline; }
  .td-center { text-align: center; color: #4f6575; }
  .td-venue  { font-size: 0.82rem; color: #6a8090; max-width: 160px; }
  .td-doi    { font-size: 0.8rem; }
  .td-fecha  { font-size: 0.8rem; color: #7a8f9b; white-space: nowrap; }

  .badge-doi {
    background: #eef6fb;
    color: #0d6ea8;
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    font-family: monospace;
    font-size: 0.78rem;
  }

  .badge-pdf {
    background: #fdecea;
    color: #c0392b;
    border-radius: 6px;
    padding: 0.2rem 0.55rem;
    font-size: 0.75rem;
    font-weight: 700;
    text-decoration: none;
  }

  .badge-pdf:hover { background: #f9d2ce; }

  .sin-doi, .sin-archivo { color: #bcc8d0; font-size: 0.85rem; }

  /* ── Paginación ── */
  .paginacion {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.25rem;
  }

  .btn-pag {
    padding: 0.45rem 0.9rem;
    border-radius: 8px;
    border: 1.5px solid #c8dce8;
    background: white;
    color: #3a5060;
    font-size: 0.83rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s;
  }

  .btn-pag:hover:not(:disabled) { background: #eef6fb; border-color: #0d6ea8; color: #0d6ea8; }
  .btn-pag:disabled { opacity: 0.45; cursor: not-allowed; }

  .pag-info { font-size: 0.83rem; color: #6a8090; }

  /* ── Modal overlay ── */
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(6,18,29,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
    backdrop-filter: blur(2px);
  }

  .modal {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    width: 100%;
    max-width: 560px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 32px 80px rgba(0,0,0,0.3);
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.15rem;
    color: #09263a;
    font-weight: 700;
  }

  .btn-cerrar {
    background: none;
    border: none;
    cursor: pointer;
    color: #8a9ba5;
    display: grid;
    place-items: center;
    padding: 0.25rem;
    border-radius: 6px;
    transition: color 0.2s, background 0.2s;
  }

  .btn-cerrar:hover { color: #09263a; background: #f0f5f8; }

  /* ── Upload feedback ── */
  .upload-ok {
    background: #d4f5e4;
    border: 1px solid #a8e8c8;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    color: #1a7a4a;
    font-size: 0.88rem;
    font-weight: 600;
  }

  .upload-error {
    background: #fdf0ef;
    border: 1px solid #f5c6c2;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    color: #9b2020;
    font-size: 0.88rem;
  }

  /* ── Form ── */
  .modal-form {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    flex: 1;
  }

  .field span {
    font-size: 0.82rem;
    font-weight: 600;
    color: #3a5060;
  }

  .field span em {
    color: #c0392b;
    font-style: normal;
    margin-left: 0.15rem;
  }

  .field small { font-weight: 400; color: #8a9ba5; }

  .field input {
    border: 1.5px solid #d4e2ea;
    border-radius: 10px;
    padding: 0.6rem 0.85rem;
    font-size: 0.93rem;
    color: #09263a;
    outline: none;
    background: #f8fbfd;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .field input:focus {
    border-color: #0d6ea8;
    box-shadow: 0 0 0 3px rgba(13,110,168,0.1);
    background: white;
  }

  .field input:disabled { opacity: 0.6; cursor: not-allowed; }

  .field-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }

  /* ── Modal actions ── */
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    padding-top: 0.5rem;
    border-top: 1px solid #edf2f5;
  }

  .btn-cancelar {
    padding: 0.6rem 1.1rem;
    border-radius: 10px;
    border: 1.5px solid #c8dce8;
    background: white;
    color: #3a5060;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-cancelar:hover:not(:disabled) { background: #f0f7fb; }
  .btn-cancelar:disabled { opacity: 0.6; cursor: not-allowed; }

  .btn-confirmar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.25rem;
    border-radius: 10px;
    border: none;
    background: #0d6ea8;
    color: white;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-confirmar:hover:not(:disabled) { background: #0a5a8a; }
  .btn-confirmar:disabled { opacity: 0.7; cursor: not-allowed; }

  .spinner-sm {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255,255,255,0.35);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* ── Responsive ── */
  @media (max-width: 700px) {
    .admin-shell  { flex-direction: column; }
    .main-content { padding: 1rem; gap: 1.25rem; }
    .field-row    { grid-template-columns: 1fr; }
  }
</style>
