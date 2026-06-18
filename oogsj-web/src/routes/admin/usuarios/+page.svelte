<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore, type AdminUser, type AdminRole } from '$lib/stores/auth';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';

  type UsuarioAdmin = {
    id:         number;
    first_name: string;
    last_name:  string;
    email:      string;
    admin_role: AdminRole;
    created_at: string | null;
  };

  let user: AdminUser | null = null;
  let usuarios: UsuarioAdmin[] = [];
  let cargando   = true;
  let errorMsg   = '';

  // Formulario
  let form = { first_name: '', last_name: '', email: '', password: '', admin_role: 'viewer' as AdminRole };
  let formError   = '';
  let formSuccess = '';
  let enviando    = false;
  let eliminando: number | null = null;

  const unsub = authStore.subscribe(s => { user = s.user; });

  async function cargarUsuarios() {
    cargando = true; errorMsg = '';
    try {
      const res = await fetch('/api/admin/users/', { credentials: 'include' });
      if (res.status === 401 || res.status === 403) { goto('/admin/dashboard'); return; }
      const data = await res.json();
      usuarios = data.users ?? [];
    } catch {
      errorMsg = 'No se pudieron cargar los usuarios.';
    } finally {
      cargando = false;
    }
  }

  async function crearUsuario() {
    formError = ''; formSuccess = '';
    if (!form.first_name.trim() || !form.last_name.trim()) {
      formError = 'Nombre y apellido son obligatorios.'; return;
    }
    if (!form.email.trim()) {
      formError = 'El email es obligatorio.'; return;
    }
    if (form.password.length < 8) {
      formError = 'La contraseña debe tener al menos 8 caracteres.'; return;
    }
    enviando = true;
    try {
      const res = await fetch('/api/admin/users/', {
        method:      'POST',
        credentials: 'include',
        headers:     { 'Content-Type': 'application/json' },
        body:        JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) { formError = data.error ?? 'Error al crear el usuario.'; return; }
      formSuccess = `Usuario ${data.user.first_name} ${data.user.last_name} creado correctamente.`;
      form = { first_name: '', last_name: '', email: '', password: '', admin_role: 'viewer' };
      await cargarUsuarios();
    } catch {
      formError = 'Error de conexión.';
    } finally {
      enviando = false;
    }
  }

  async function eliminarUsuario(u: UsuarioAdmin) {
    if (!confirm(`¿Eliminar a ${u.first_name} ${u.last_name}? Esta acción no se puede deshacer.`)) return;
    eliminando = u.id;
    try {
      const res = await fetch(`/api/admin/users/${u.id}`, {
        method:      'DELETE',
        credentials: 'include',
      });
      if (!res.ok) {
        const data = await res.json();
        alert(data.error ?? 'No se pudo eliminar el usuario.');
        return;
      }
      usuarios = usuarios.filter(x => x.id !== u.id);
    } finally {
      eliminando = null;
    }
  }

  function fmtDate(iso: string | null): string {
    if (!iso) return '—';
    return new Date(iso).toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }

  onMount(() => { cargarUsuarios(); });
  onDestroy(() => unsub());
</script>

<div class="admin-shell">
  <AdminSidebar {user} />

  <main class="main-content">

    <header class="main-header">
      <div>
        <h1>Gestión de Usuarios</h1>
        <p>Creá y administrá las cuentas de acceso al panel</p>
      </div>
    </header>

    <!-- ── Formulario nuevo usuario ── -->
    <section class="seccion">
      <h2 class="seccion-titulo"><span>➕</span> Nuevo usuario</h2>

      <div class="form-card">
        {#if formError}
          <div class="form-msg error">{formError}</div>
        {/if}
        {#if formSuccess}
          <div class="form-msg success">{formSuccess}</div>
        {/if}

        <div class="form-grid">
          <div class="form-field">
            <label for="fn">Nombre</label>
            <input id="fn" type="text" bind:value={form.first_name} placeholder="Nombre" maxlength="120" />
          </div>
          <div class="form-field">
            <label for="ln">Apellido</label>
            <input id="ln" type="text" bind:value={form.last_name} placeholder="Apellido" maxlength="120" />
          </div>
          <div class="form-field form-field-wide">
            <label for="em">Email</label>
            <input id="em" type="email" bind:value={form.email} placeholder="usuario@ejemplo.com" />
          </div>
          <div class="form-field">
            <label for="pw">Contraseña</label>
            <input id="pw" type="password" bind:value={form.password} placeholder="Mínimo 8 caracteres" />
          </div>
          <div class="form-field">
            <label for="rol">Rol</label>
            <select id="rol" bind:value={form.admin_role}>
              <option value="viewer">Viewer — Solo lectura</option>
              <option value="master">Master — Acceso completo</option>
            </select>
          </div>
        </div>

        <div class="role-info">
          {#if form.admin_role === 'viewer'}
            <span class="role-pill viewer">Viewer:</span> puede ver el dashboard y estadísticas, pero no puede modificar nada ni crear usuarios.
          {:else}
            <span class="role-pill master">Master:</span> acceso completo al panel — puede crear y eliminar usuarios, modificar noticias, plataformas y más.
          {/if}
        </div>

        <button class="btn-crear" on:click={crearUsuario} disabled={enviando}>
          {#if enviando}Creando...{:else}Crear usuario{/if}
        </button>
      </div>
    </section>

    <!-- ── Lista de usuarios ── -->
    <section class="seccion">
      <h2 class="seccion-titulo">
        <span>👥</span> Usuarios registrados
        <span class="seccion-sub">{usuarios.length} cuenta{usuarios.length !== 1 ? 's' : ''}</span>
      </h2>

      {#if errorMsg}
        <div class="form-msg error">{errorMsg}</div>
      {/if}

      {#if cargando}
        <div class="skeleton-table">
          {#each Array(3) as _}
            <div class="skeleton-row"></div>
          {/each}
        </div>
      {:else}
        <div class="users-table-wrap">
          <table class="users-table">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Email</th>
                <th>Rol</th>
                <th>Creado</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {#each usuarios as u}
                <tr class:self-row={u.id === user?.id}>
                  <td class="td-nombre">
                    <div class="user-avatar-sm">{u.first_name[0]}{u.last_name[0]}</div>
                    <span>{u.first_name} {u.last_name}</span>
                    {#if u.id === user?.id}
                      <span class="tag-tu">Tú</span>
                    {/if}
                  </td>
                  <td class="td-email">{u.email}</td>
                  <td>
                    <span class="rol-badge rol-{u.admin_role}">
                      {u.admin_role === 'master' ? 'Master' : 'Viewer'}
                    </span>
                  </td>
                  <td class="td-fecha">{fmtDate(u.created_at)}</td>
                  <td class="td-acciones">
                    {#if u.id !== user?.id}
                      <button
                        class="btn-eliminar"
                        disabled={eliminando === u.id}
                        on:click={() => eliminarUsuario(u)}
                        title="Eliminar usuario"
                      >
                        {eliminando === u.id ? '...' : 'Eliminar'}
                      </button>
                    {:else}
                      <span class="sin-accion">—</span>
                    {/if}
                  </td>
                </tr>
              {/each}

              {#if usuarios.length === 0}
                <tr>
                  <td colspan="5" class="td-empty">No hay usuarios registrados.</td>
                </tr>
              {/if}
            </tbody>
          </table>
        </div>
      {/if}
    </section>

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
    gap: 1.75rem;
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

  /* Sección */
  .seccion { display: flex; flex-direction: column; gap: 0.85rem; }

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

  /* Form */
  .form-card {
    background: white;
    border-radius: 18px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 2px 12px rgba(9,38,58,0.06);
    border: 1px solid rgba(9,38,58,0.06);
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .form-msg {
    padding: 0.7rem 1rem;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 500;
  }

  .form-msg.error   { background: #fdf0ef; border: 1px solid #f5c6c2; color: #9b2020; }
  .form-msg.success { background: #edf7f0; border: 1px solid #a3d9b4; color: #1a6a35; }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.85rem;
  }

  .form-field-wide { grid-column: span 2; }

  .form-field { display: flex; flex-direction: column; gap: 0.35rem; }

  .form-field label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
  }

  .form-field input,
  .form-field select {
    padding: 0.55rem 0.85rem;
    border-radius: 10px;
    border: 1.5px solid #d5e3ec;
    background: #f8fbfd;
    color: #09263a;
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.2s;
    font-family: inherit;
  }

  .form-field input:focus,
  .form-field select:focus { border-color: #0d6ea8; background: white; }

  .role-info {
    font-size: 0.83rem;
    color: #5a7a90;
    background: #f4f8fb;
    border-radius: 10px;
    padding: 0.65rem 1rem;
    line-height: 1.5;
  }

  .role-pill {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    margin-right: 0.25rem;
  }

  .role-pill.viewer { background: rgba(143,211,255,0.15); color: #0d6ea8; }
  .role-pill.master { background: rgba(249,115,22,0.15);  color: #c2410c; }

  .btn-crear {
    align-self: flex-start;
    padding: 0.6rem 1.5rem;
    border-radius: 10px;
    border: none;
    background: #0d6ea8;
    color: white;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-crear:hover:not(:disabled) { background: #0a5a8e; }
  .btn-crear:disabled { opacity: 0.6; cursor: not-allowed; }

  /* Tabla usuarios */
  .users-table-wrap {
    background: white;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(9,38,58,0.06);
    border: 1px solid rgba(9,38,58,0.06);
    overflow-x: auto;
  }

  .users-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }

  .users-table thead tr { border-bottom: 1.5px solid #edf2f5; }

  .users-table th {
    padding: 0.85rem 1rem;
    text-align: left;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #8a9ba5;
    white-space: nowrap;
  }

  .users-table tbody tr {
    border-bottom: 1px solid #f0f5f8;
    transition: background 0.15s;
  }

  .users-table tbody tr:last-child { border-bottom: none; }
  .users-table tbody tr:hover { background: #f4f9fc; }
  .self-row { background: #f0f9ff !important; }

  .users-table td {
    padding: 0.85rem 1rem;
    color: #2a3f4f;
    vertical-align: middle;
  }

  .td-nombre {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-weight: 600;
    color: #09263a;
    white-space: nowrap;
  }

  .user-avatar-sm {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #0d6ea8;
    color: white;
    font-size: 0.68rem;
    font-weight: 700;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    text-transform: uppercase;
  }

  .tag-tu {
    font-size: 0.68rem;
    font-weight: 700;
    background: #dbeafe;
    color: #1d4ed8;
    border-radius: 4px;
    padding: 0.1rem 0.35rem;
  }

  .td-email { color: #4f6575; font-size: 0.83rem; }
  .td-fecha { color: #8a9ba5; font-size: 0.82rem; white-space: nowrap; }
  .td-acciones { text-align: right; white-space: nowrap; }

  .rol-badge {
    display: inline-block;
    font-size: 0.73rem;
    font-weight: 700;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .rol-master { background: rgba(249,115,22,0.12); color: #c2410c; }
  .rol-viewer { background: rgba(13,110,168,0.1);  color: #0d6ea8; }

  .btn-eliminar {
    padding: 0.28rem 0.75rem;
    border-radius: 99px;
    border: 1.5px solid rgba(231,76,60,0.3);
    background: rgba(231,76,60,0.07);
    color: #c0392b;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.18s;
  }

  .btn-eliminar:hover:not(:disabled) {
    background: rgba(231,76,60,0.15);
    border-color: #e74c3c;
  }

  .btn-eliminar:disabled { opacity: 0.5; cursor: not-allowed; }

  .sin-accion { color: #c0d0da; font-size: 0.85rem; }

  .td-empty {
    text-align: center;
    color: #9aafba;
    font-style: italic;
    padding: 2rem !important;
  }

  /* Skeleton */
  .skeleton-table { display: flex; flex-direction: column; gap: 0.5rem; }

  .skeleton-row {
    height: 56px;
    border-radius: 12px;
    background: linear-gradient(90deg, #e8eef2 25%, #f4f8fb 50%, #e8eef2 75%);
    background-size: 200% 100%;
    animation: shimmer 1.2s infinite;
  }

  @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

  @media (max-width: 700px) {
    .admin-shell { flex-direction: column; }
    .main-content { padding: 1rem; gap: 1.25rem; }
    .form-grid { grid-template-columns: 1fr; }
    .form-field-wide { grid-column: span 1; }
  }
</style>
