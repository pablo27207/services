<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore, type AdminUser } from '$lib/stores/auth';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';

  type Noticia = {
    id: number; titulo: string; contenido: string;
    categoria: string | null; imagen_url: string | null;
    publicado: boolean; created_at: string | null; updated_at: string | null;
  };

  let user: AdminUser | null = null;
  let noticias: Noticia[]    = [];
  let cargando               = true;
  let errorMsg               = '';

  // Modal estado
  let modal: 'none' | 'crear' | 'editar' | 'borrar' = 'none';
  let guardando  = false;
  let modalError = '';
  let editando: Noticia | null = null;

  // Form fields
  let fTitulo    = '';
  let fContenido = '';
  let fCategoria = '';
  let fImagenUrl = '';
  let fPublicado = false;

  const CATEGORIAS = ['General', 'Investigación', 'Monitoreo', 'Eventos', 'Institucional'];

  const unsub = authStore.subscribe(s => { user = s.user; });

  async function cargar() {
    cargando = true; errorMsg = '';
    try {
      const res = await fetch('/api/noticias/admin', { credentials: 'include' });
      if (!res.ok) throw new Error();
      const data = await res.json();
      noticias = data.noticias ?? [];
    } catch {
      errorMsg = 'No se pudieron cargar las noticias.';
    } finally {
      cargando = false;
    }
  }

  function abrirCrear() {
    fTitulo = ''; fContenido = ''; fCategoria = ''; fImagenUrl = ''; fPublicado = false;
    editando = null; modalError = ''; modal = 'crear';
  }

  function abrirEditar(n: Noticia) {
    editando   = n;
    fTitulo    = n.titulo;
    fContenido = n.contenido;
    fCategoria = n.categoria ?? '';
    fImagenUrl = n.imagen_url ?? '';
    fPublicado = n.publicado;
    modalError = ''; modal = 'editar';
  }

  function abrirBorrar(n: Noticia) {
    editando = n; modal = 'borrar';
  }

  function cerrar() { modal = 'none'; editando = null; modalError = ''; }

  async function guardar() {
    if (!fTitulo.trim())    { modalError = 'El título es obligatorio.'; return; }
    if (!fContenido.trim()) { modalError = 'El contenido es obligatorio.'; return; }
    guardando = true; modalError = '';

    const body = {
      titulo:    fTitulo.trim(),
      contenido: fContenido.trim(),
      categoria: fCategoria.trim() || null,
      imagen_url: fImagenUrl.trim() || null,
      publicado: fPublicado,
    };

    const url    = modal === 'editar' ? `/api/noticias/admin/${editando!.id}` : '/api/noticias/admin';
    const method = modal === 'editar' ? 'PUT' : 'POST';

    try {
      const res = await fetch(url, {
        method, credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!res.ok) { const d = await res.json(); throw new Error(d.error); }
      cerrar();
      await cargar();
    } catch (e: any) {
      modalError = e?.message ?? 'Error al guardar';
    } finally {
      guardando = false;
    }
  }

  async function eliminar() {
    guardando = true;
    try {
      const res = await fetch(`/api/noticias/admin/${editando!.id}`, {
        method: 'DELETE', credentials: 'include',
      });
      if (!res.ok) throw new Error();
      cerrar();
      await cargar();
    } catch {
      modalError = 'Error al eliminar.';
    } finally {
      guardando = false;
    }
  }

  async function togglePublicado(n: Noticia) {
    await fetch(`/api/noticias/admin/${n.id}`, {
      method: 'PUT', credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ publicado: !n.publicado }),
    });
    await cargar();
  }

  function fmtFecha(iso: string | null) {
    if (!iso) return '—';
    return new Date(iso).toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }

  onMount(() => cargar());
  onDestroy(() => unsub());
</script>

<div class="admin-shell">
  <AdminSidebar {user} />

  <main class="main-content">
    <header class="main-header">
      <div>
        <h1>Noticias y novedades</h1>
        <p>{noticias.length} noticia{noticias.length !== 1 ? 's' : ''} · {noticias.filter(n => n.publicado).length} publicada{noticias.filter(n => n.publicado).length !== 1 ? 's' : ''}</p>
      </div>
      <button class="btn-primary" on:click={abrirCrear}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Nueva noticia
      </button>
    </header>

    {#if errorMsg}<div class="error-banner">{errorMsg}</div>{/if}

    {#if cargando}
      <div class="skeletons">{#each Array(4) as _}<div class="skeleton"></div>{/each}</div>
    {:else if noticias.length === 0}
      <div class="vacio"><span>📰</span><p>No hay noticias todavía.</p></div>
    {:else}
      <div class="cards">
        {#each noticias as n (n.id)}
          <div class="card" class:borrador={!n.publicado}>
            <div class="card-top">
              <div class="card-meta">
                {#if n.categoria}<span class="badge-cat">{n.categoria}</span>{/if}
                <span class="badge-estado" class:publicado={n.publicado}>
                  {n.publicado ? '● Publicada' : '● Borrador'}
                </span>
              </div>
              <span class="card-fecha">{fmtFecha(n.created_at)}</span>
            </div>
            <h3 class="card-titulo">{n.titulo}</h3>
            <p class="card-preview">{n.contenido.slice(0, 140)}{n.contenido.length > 140 ? '…' : ''}</p>
            <div class="card-actions">
              <button class="btn-toggle" on:click={() => togglePublicado(n)}>
                {n.publicado ? 'Despublicar' : 'Publicar'}
              </button>
              <button class="btn-edit" on:click={() => abrirEditar(n)}>Editar</button>
              <button class="btn-del"  on:click={() => abrirBorrar(n)}>Eliminar</button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </main>
</div>

<!-- ══ Modal crear / editar ══ -->
{#if modal === 'crear' || modal === 'editar'}
  <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
  <div class="dlg-overlay" on:click|self={cerrar}>
    <div class="dlg">
      <div class="dlg-header">
        <h2>{modal === 'crear' ? 'Nueva noticia' : 'Editar noticia'}</h2>
        <button class="btn-x" on:click={cerrar} aria-label="Cerrar">✕</button>
      </div>

      {#if modalError}<div class="dlg-error">{modalError}</div>{/if}

      <form on:submit|preventDefault={guardar} class="form">
        <label class="field">
          <span>Título <em>*</em></span>
          <input type="text" bind:value={fTitulo} disabled={guardando} placeholder="Título de la noticia" />
        </label>

        <div class="row-2">
          <label class="field">
            <span>Categoría</span>
            <select bind:value={fCategoria} disabled={guardando}>
              <option value="">Sin categoría</option>
              {#each CATEGORIAS as c}<option value={c}>{c}</option>{/each}
            </select>
          </label>
          <label class="field check-field">
            <span>Estado</span>
            <label class="toggle">
              <input type="checkbox" bind:checked={fPublicado} disabled={guardando} />
              <span class="toggle-track"></span>
              <span class="toggle-label">{fPublicado ? 'Publicada' : 'Borrador'}</span>
            </label>
          </label>
        </div>

        <label class="field">
          <span>URL de imagen <small>(opcional)</small></span>
          <input type="url" bind:value={fImagenUrl} disabled={guardando} placeholder="https://..." />
        </label>

        <label class="field">
          <span>Contenido <em>*</em></span>
          <textarea bind:value={fContenido} disabled={guardando} rows="8" placeholder="Escribí el contenido de la noticia..."></textarea>
        </label>

        <div class="dlg-actions">
          <button type="button" class="btn-cancel" on:click={cerrar} disabled={guardando}>Cancelar</button>
          <button type="submit" class="btn-save" disabled={guardando}>
            {#if guardando}<span class="spin"></span> Guardando...{:else}Guardar{/if}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}

<!-- ══ Modal confirmar borrado ══ -->
{#if modal === 'borrar'}
  <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
  <div class="dlg-overlay" on:click|self={cerrar}>
    <div class="dlg dlg-sm">
      <h2>¿Eliminar noticia?</h2>
      <p class="confirm-txt">Se eliminará permanentemente <strong>"{editando?.titulo}"</strong>.</p>
      {#if modalError}<div class="dlg-error">{modalError}</div>{/if}
      <div class="dlg-actions">
        <button class="btn-cancel" on:click={cerrar} disabled={guardando}>Cancelar</button>
        <button class="btn-danger" on:click={eliminar} disabled={guardando}>
          {#if guardando}<span class="spin"></span>{/if} Eliminar
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .admin-shell { display: flex; min-height: 100vh; background: #f2f6f9; font-family: system-ui, sans-serif; }
  .main-content { flex: 1; display: flex; flex-direction: column; gap: 1.75rem; padding: 2rem; min-width: 0; }

  .main-header { display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
  .main-header h1 { margin: 0 0 0.2rem; font-size: 1.65rem; color: #09263a; font-weight: 800; }
  .main-header p  { margin: 0; color: #6a8090; font-size: 0.88rem; }

  .btn-primary { display: flex; align-items: center; gap: 0.5rem; padding: 0.55rem 1.1rem; border-radius: 10px; border: none; background: #0d6ea8; color: white; font-size: 0.88rem; font-weight: 700; cursor: pointer; transition: background 0.2s; }
  .btn-primary:hover { background: #0a5a8a; }

  .error-banner { background: #fdf0ef; border: 1px solid #f5c6c2; border-radius: 12px; padding: 0.85rem 1.1rem; color: #9b2020; font-size: 0.88rem; }

  .skeletons { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
  .skeleton  { height: 180px; border-radius: 16px; background: linear-gradient(90deg, #e8eef2 25%, #f4f8fb 50%, #e8eef2 75%); background-size: 200% 100%; animation: shimmer 1.2s infinite; }
  @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

  .vacio { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; padding: 4rem; color: #6a8090; }
  .vacio span { font-size: 2.5rem; }

  /* Cards grid */
  .cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }

  .card { background: white; border-radius: 18px; padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; box-shadow: 0 2px 12px rgba(9,38,58,0.06); border: 1.5px solid rgba(9,38,58,0.06); transition: box-shadow 0.2s; }
  .card:hover { box-shadow: 0 6px 20px rgba(9,38,58,0.1); }
  .card.borrador { border-color: #e0e8ef; opacity: 0.85; }

  .card-top   { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; }
  .card-meta  { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }
  .card-fecha { font-size: 0.78rem; color: #9aafba; }

  .badge-cat { font-size: 0.72rem; font-weight: 700; background: #e8f4fc; color: #0d6ea8; border-radius: 99px; padding: 0.2rem 0.6rem; }
  .badge-estado { font-size: 0.72rem; font-weight: 700; border-radius: 99px; padding: 0.2rem 0.6rem; background: #f0f0f0; color: #6a6a6a; }
  .badge-estado.publicado { background: #d4f5e4; color: #1a7a4a; }

  .card-titulo  { margin: 0; font-size: 1rem; font-weight: 700; color: #09263a; line-height: 1.3; }
  .card-preview { margin: 0; font-size: 0.85rem; color: #5a6d7b; line-height: 1.6; flex: 1; }

  .card-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; padding-top: 0.5rem; border-top: 1px solid #f0f5f8; }

  .btn-toggle { padding: 0.35rem 0.8rem; border-radius: 8px; border: 1.5px solid #c8dce8; background: white; color: #3a5060; font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: background 0.15s; }
  .btn-toggle:hover { background: #eef6fb; }
  .btn-edit   { padding: 0.35rem 0.8rem; border-radius: 8px; border: none; background: #eef6fb; color: #0d6ea8; font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: background 0.15s; }
  .btn-edit:hover { background: #d8ecf8; }
  .btn-del    { padding: 0.35rem 0.8rem; border-radius: 8px; border: none; background: #fdf0ef; color: #c0392b; font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: background 0.15s; margin-left: auto; }
  .btn-del:hover { background: #f9d2ce; }

  /* Modal */
  .dlg-overlay { position: fixed; inset: 0; background: rgba(6,18,29,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; backdrop-filter: blur(2px); }
  .dlg { background: white; border-radius: 20px; padding: 2rem; width: 100%; max-width: 620px; max-height: 90vh; overflow-y: auto; box-shadow: 0 32px 80px rgba(0,0,0,0.3); display: flex; flex-direction: column; gap: 1.25rem; }
  .dlg-sm { max-width: 420px; }
  .dlg-header { display: flex; align-items: center; justify-content: space-between; }
  .dlg-header h2 { margin: 0; font-size: 1.15rem; color: #09263a; font-weight: 700; }
  .dlg h2 { margin: 0; font-size: 1.1rem; color: #09263a; font-weight: 700; }
  .btn-x { background: none; border: none; cursor: pointer; color: #8a9ba5; font-size: 1rem; padding: 0.25rem 0.4rem; border-radius: 6px; }
  .btn-x:hover { background: #f0f5f8; color: #09263a; }

  .dlg-error { background: #fdf0ef; border: 1px solid #f5c6c2; border-radius: 10px; padding: 0.7rem 1rem; color: #9b2020; font-size: 0.88rem; }

  .form { display: flex; flex-direction: column; gap: 0.9rem; }
  .field { display: flex; flex-direction: column; gap: 0.35rem; flex: 1; }
  .field span { font-size: 0.82rem; font-weight: 600; color: #3a5060; }
  .field span em { color: #c0392b; font-style: normal; margin-left: 0.15rem; }
  .field small { font-weight: 400; color: #8a9ba5; }
  .field input, .field select, .field textarea { border: 1.5px solid #d4e2ea; border-radius: 10px; padding: 0.6rem 0.85rem; font-size: 0.93rem; color: #09263a; outline: none; background: #f8fbfd; transition: border-color 0.2s, box-shadow 0.2s; font-family: inherit; }
  .field input:focus, .field select:focus, .field textarea:focus { border-color: #0d6ea8; box-shadow: 0 0 0 3px rgba(13,110,168,0.1); background: white; }
  .field textarea { resize: vertical; min-height: 140px; }
  .field input:disabled, .field select:disabled, .field textarea:disabled { opacity: 0.6; cursor: not-allowed; }

  .row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }

  .check-field { justify-content: flex-start; }
  .toggle { display: flex; align-items: center; gap: 0.6rem; cursor: pointer; }
  .toggle input { position: absolute; opacity: 0; width: 0; height: 0; }
  .toggle-track { width: 38px; height: 22px; background: #d4e2ea; border-radius: 99px; position: relative; transition: background 0.2s; flex-shrink: 0; }
  .toggle input:checked ~ .toggle-track { background: #0d6ea8; }
  .toggle-track::after { content: ''; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; background: white; border-radius: 50%; transition: transform 0.2s; }
  .toggle input:checked ~ .toggle-track::after { transform: translateX(16px); }
  .toggle-label { font-size: 0.85rem; color: #3a5060; font-weight: 500; }

  .confirm-txt { margin: 0; color: #4f6575; font-size: 0.93rem; line-height: 1.6; }

  .dlg-actions { display: flex; justify-content: flex-end; gap: 0.75rem; padding-top: 0.5rem; border-top: 1px solid #edf2f5; }
  .btn-cancel { padding: 0.6rem 1.1rem; border-radius: 10px; border: 1.5px solid #c8dce8; background: white; color: #3a5060; font-size: 0.88rem; font-weight: 600; cursor: pointer; }
  .btn-cancel:hover:not(:disabled) { background: #f0f7fb; }
  .btn-save   { display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1.25rem; border-radius: 10px; border: none; background: #0d6ea8; color: white; font-size: 0.88rem; font-weight: 700; cursor: pointer; }
  .btn-save:hover:not(:disabled) { background: #0a5a8a; }
  .btn-danger { display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1.25rem; border-radius: 10px; border: none; background: #e74c3c; color: white; font-size: 0.88rem; font-weight: 700; cursor: pointer; }
  .btn-danger:hover:not(:disabled) { background: #c0392b; }
  .btn-cancel:disabled, .btn-save:disabled, .btn-danger:disabled { opacity: 0.65; cursor: not-allowed; }

  .spin { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.35); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  @media (max-width: 900px) { .cards { grid-template-columns: 1fr; } }
  @media (max-width: 700px) { .admin-shell { flex-direction: column; } .main-content { padding: 1rem; } .row-2 { grid-template-columns: 1fr; } }
</style>
