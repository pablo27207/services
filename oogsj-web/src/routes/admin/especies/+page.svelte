<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore, type AdminUser } from '$lib/stores/auth';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';

  type Especie = {
    id: number; nombre_comun: string; nombre_cientifico: string | null;
    descripcion: string | null; categoria: string | null;
    imagen_url: string | null; created_at: string | null;
  };

  let user: AdminUser | null = null;
  let especies: Especie[]    = [];
  let filtradas: Especie[]   = [];
  let busqueda               = '';
  let cargando               = true;
  let errorMsg               = '';

  let modal: 'none' | 'crear' | 'editar' | 'borrar' = 'none';
  let guardando  = false;
  let modalError = '';
  let editando: Especie | null = null;

  let fNombreComun      = '';
  let fNombreCientifico = '';
  let fDescripcion      = '';
  let fCategoria        = '';
  let fImagenUrl        = '';

  const CATEGORIAS = ['Peces', 'Mamíferos marinos', 'Aves costeras', 'Invertebrados', 'Algas', 'Reptiles', 'Otro'];

  const unsub = authStore.subscribe(s => { user = s.user; });

  $: filtradas = busqueda.trim()
    ? especies.filter(e =>
        e.nombre_comun.toLowerCase().includes(busqueda.toLowerCase()) ||
        (e.nombre_cientifico ?? '').toLowerCase().includes(busqueda.toLowerCase()) ||
        (e.categoria ?? '').toLowerCase().includes(busqueda.toLowerCase()))
    : especies;

  async function cargar() {
    cargando = true; errorMsg = '';
    try {
      const res = await fetch('/api/especies/', { credentials: 'include' });
      if (!res.ok) throw new Error();
      const data = await res.json();
      especies = data.especies ?? [];
    } catch {
      errorMsg = 'No se pudieron cargar las especies.';
    } finally {
      cargando = false;
    }
  }

  function abrirCrear() {
    fNombreComun = ''; fNombreCientifico = ''; fDescripcion = ''; fCategoria = ''; fImagenUrl = '';
    editando = null; modalError = ''; modal = 'crear';
  }

  function abrirEditar(e: Especie) {
    editando          = e;
    fNombreComun      = e.nombre_comun;
    fNombreCientifico = e.nombre_cientifico ?? '';
    fDescripcion      = e.descripcion ?? '';
    fCategoria        = e.categoria ?? '';
    fImagenUrl        = e.imagen_url ?? '';
    modalError = ''; modal = 'editar';
  }

  function abrirBorrar(e: Especie) { editando = e; modal = 'borrar'; }
  function cerrar() { modal = 'none'; editando = null; modalError = ''; }

  async function guardar() {
    if (!fNombreComun.trim()) { modalError = 'El nombre común es obligatorio.'; return; }
    guardando = true; modalError = '';

    const body = {
      nombre_comun:      fNombreComun.trim(),
      nombre_cientifico: fNombreCientifico.trim() || null,
      descripcion:       fDescripcion.trim() || null,
      categoria:         fCategoria || null,
      imagen_url:        fImagenUrl.trim() || null,
    };

    const url    = modal === 'editar' ? `/api/especies/admin/${editando!.id}` : '/api/especies/admin';
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
      const res = await fetch(`/api/especies/admin/${editando!.id}`, {
        method: 'DELETE', credentials: 'include',
      });
      if (!res.ok) throw new Error();
      cerrar(); await cargar();
    } catch {
      modalError = 'Error al eliminar.';
    } finally {
      guardando = false;
    }
  }

  onMount(() => cargar());
  onDestroy(() => unsub());
</script>

<div class="admin-shell">
  <AdminSidebar {user} />

  <main class="main-content">
    <header class="main-header">
      <div>
        <h1>Catálogo de especies</h1>
        <p>{especies.length} especie{especies.length !== 1 ? 's' : ''} registrada{especies.length !== 1 ? 's' : ''}</p>
      </div>
      <button class="btn-primary" on:click={abrirCrear}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Nueva especie
      </button>
    </header>

    <!-- Buscador -->
    <div class="buscador-wrap">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8a9ba5" stroke-width="2" stroke-linecap="round" class="search-icon">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <input class="buscador" type="search" placeholder="Buscar por nombre o categoría..." bind:value={busqueda} />
    </div>

    {#if errorMsg}<div class="error-banner">{errorMsg}</div>{/if}

    {#if cargando}
      <div class="skeletons">{#each Array(6) as _}<div class="skeleton"></div>{/each}</div>
    {:else if filtradas.length === 0}
      <div class="vacio">
        <span>🐟</span>
        <p>{busqueda ? 'Sin resultados para "' + busqueda + '"' : 'No hay especies registradas todavía.'}</p>
      </div>
    {:else}
      <div class="grid">
        {#each filtradas as e (e.id)}
          <div class="card">
            {#if e.imagen_url}
              <img src={e.imagen_url} alt={e.nombre_comun} class="card-img" />
            {:else}
              <div class="card-img-placeholder">🐟</div>
            {/if}
            <div class="card-body">
              {#if e.categoria}<span class="badge-cat">{e.categoria}</span>{/if}
              <h3 class="card-nombre">{e.nombre_comun}</h3>
              {#if e.nombre_cientifico}<p class="card-cientifico"><em>{e.nombre_cientifico}</em></p>{/if}
              {#if e.descripcion}<p class="card-desc">{e.descripcion.slice(0, 100)}{e.descripcion.length > 100 ? '…' : ''}</p>{/if}
              <div class="card-actions">
                <button class="btn-edit" on:click={() => abrirEditar(e)}>Editar</button>
                <button class="btn-del"  on:click={() => abrirBorrar(e)}>Eliminar</button>
              </div>
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
        <h2>{modal === 'crear' ? 'Nueva especie' : 'Editar especie'}</h2>
        <button class="btn-x" on:click={cerrar} aria-label="Cerrar">✕</button>
      </div>

      {#if modalError}<div class="dlg-error">{modalError}</div>{/if}

      <form on:submit|preventDefault={guardar} class="form">
        <div class="row-2">
          <label class="field">
            <span>Nombre común <em>*</em></span>
            <input type="text" bind:value={fNombreComun} disabled={guardando} placeholder="Ej: Merluza" />
          </label>
          <label class="field">
            <span>Nombre científico</span>
            <input type="text" bind:value={fNombreCientifico} disabled={guardando} placeholder="Ej: Merluccius hubbsi" />
          </label>
        </div>

        <div class="row-2">
          <label class="field">
            <span>Categoría</span>
            <select bind:value={fCategoria} disabled={guardando}>
              <option value="">Sin categoría</option>
              {#each CATEGORIAS as c}<option value={c}>{c}</option>{/each}
            </select>
          </label>
          <label class="field">
            <span>URL de imagen <small>(opcional)</small></span>
            <input type="url" bind:value={fImagenUrl} disabled={guardando} placeholder="https://..." />
          </label>
        </div>

        <label class="field">
          <span>Descripción</span>
          <textarea bind:value={fDescripcion} disabled={guardando} rows="5" placeholder="Características, hábitat, importancia ecológica..."></textarea>
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

<!-- ══ Modal borrar ══ -->
{#if modal === 'borrar'}
  <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
  <div class="dlg-overlay" on:click|self={cerrar}>
    <div class="dlg dlg-sm">
      <h2>¿Eliminar especie?</h2>
      <p class="confirm-txt">Se eliminará permanentemente <strong>"{editando?.nombre_comun}"</strong>.</p>
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

  .buscador-wrap { position: relative; max-width: 400px; }
  .search-icon   { position: absolute; left: 0.85rem; top: 50%; transform: translateY(-50%); pointer-events: none; }
  .buscador { width: 100%; padding: 0.6rem 0.85rem 0.6rem 2.5rem; border: 1.5px solid #d4e2ea; border-radius: 10px; font-size: 0.93rem; color: #09263a; background: white; outline: none; box-sizing: border-box; }
  .buscador:focus { border-color: #0d6ea8; box-shadow: 0 0 0 3px rgba(13,110,168,0.1); }

  .error-banner { background: #fdf0ef; border: 1px solid #f5c6c2; border-radius: 12px; padding: 0.85rem 1.1rem; color: #9b2020; font-size: 0.88rem; }

  .skeletons { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
  .skeleton  { height: 220px; border-radius: 16px; background: linear-gradient(90deg, #e8eef2 25%, #f4f8fb 50%, #e8eef2 75%); background-size: 200% 100%; animation: shimmer 1.2s infinite; }
  @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

  .vacio { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; padding: 4rem; color: #6a8090; }
  .vacio span { font-size: 2.5rem; }

  .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }

  .card { background: white; border-radius: 18px; overflow: hidden; box-shadow: 0 2px 12px rgba(9,38,58,0.06); border: 1.5px solid rgba(9,38,58,0.06); display: flex; flex-direction: column; transition: box-shadow 0.2s; }
  .card:hover { box-shadow: 0 6px 20px rgba(9,38,58,0.1); }

  .card-img { width: 100%; height: 160px; object-fit: cover; }
  .card-img-placeholder { width: 100%; height: 120px; background: linear-gradient(135deg, #dff4ff, #eef9ff); display: grid; place-items: center; font-size: 2.5rem; }

  .card-body { padding: 1rem 1.1rem; display: flex; flex-direction: column; gap: 0.4rem; flex: 1; }

  .badge-cat { font-size: 0.7rem; font-weight: 700; background: #e8f4fc; color: #0d6ea8; border-radius: 99px; padding: 0.2rem 0.55rem; align-self: flex-start; }

  .card-nombre    { margin: 0; font-size: 0.98rem; font-weight: 700; color: #09263a; line-height: 1.3; }
  .card-cientifico{ margin: 0; font-size: 0.8rem; color: #6a8090; }
  .card-desc      { margin: 0; font-size: 0.82rem; color: #5a6d7b; line-height: 1.55; flex: 1; }

  .card-actions { display: flex; gap: 0.5rem; padding-top: 0.65rem; border-top: 1px solid #f0f5f8; margin-top: auto; }
  .btn-edit { padding: 0.3rem 0.75rem; border-radius: 7px; border: none; background: #eef6fb; color: #0d6ea8; font-size: 0.78rem; font-weight: 600; cursor: pointer; }
  .btn-edit:hover { background: #d8ecf8; }
  .btn-del  { padding: 0.3rem 0.75rem; border-radius: 7px; border: none; background: #fdf0ef; color: #c0392b; font-size: 0.78rem; font-weight: 600; cursor: pointer; margin-left: auto; }
  .btn-del:hover { background: #f9d2ce; }

  /* Modal */
  .dlg-overlay { position: fixed; inset: 0; background: rgba(6,18,29,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; backdrop-filter: blur(2px); }
  .dlg { background: white; border-radius: 20px; padding: 2rem; width: 100%; max-width: 600px; max-height: 90vh; overflow-y: auto; box-shadow: 0 32px 80px rgba(0,0,0,0.3); display: flex; flex-direction: column; gap: 1.25rem; }
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
  .field textarea { resize: vertical; min-height: 110px; }
  .field input:disabled, .field select:disabled, .field textarea:disabled { opacity: 0.6; cursor: not-allowed; }

  .row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }

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

  @media (max-width: 1100px) { .grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 700px)  { .admin-shell { flex-direction: column; } .main-content { padding: 1rem; } .grid { grid-template-columns: 1fr; } .row-2 { grid-template-columns: 1fr; } }
</style>
