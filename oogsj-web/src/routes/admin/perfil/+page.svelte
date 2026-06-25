<script lang="ts">
  import { onDestroy } from 'svelte';
  import { authStore, type AdminUser } from '$lib/stores/auth';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';

  let user: AdminUser | null = null;
  const unsub = authStore.subscribe(s => { user = s.user; });
  onDestroy(() => unsub());

  const STORAGE_KEY = 'oogsj_remember';

  function tieneCredencialesGuardadas(): boolean {
    try {
      return !!localStorage.getItem(STORAGE_KEY);
    } catch { return false; }
  }

  function borrarCredenciales() {
    try {
      localStorage.removeItem(STORAGE_KEY);
      credencialesGuardadas = false;
    } catch { /* ignore */ }
  }

  let credencialesGuardadas = tieneCredencialesGuardadas();

  function rolLabel(role: string | null): string {
    if (role === 'master') return 'Master — acceso completo';
    if (role === 'viewer') return 'Viewer — solo lectura';
    return '—';
  }

  function rolColor(role: string | null): string {
    if (role === 'master') return 'master';
    if (role === 'viewer') return 'viewer';
    return '';
  }
</script>

<div class="admin-shell">
  <AdminSidebar {user} />

  <main class="main-content">
    <header class="main-header">
      <div>
        <h1>Mi perfil</h1>
        <p>Información de tu cuenta de acceso</p>
      </div>
    </header>

    {#if user}
      <div class="perfil-grid">

        <!-- Tarjeta principal -->
        <div class="card perfil-card">
          <div class="avatar-grande">
            {user.first_name[0]}{user.last_name[0]}
          </div>
          <div class="perfil-nombre-bloque">
            <h2 class="perfil-nombre">{user.first_name} {user.last_name}</h2>
            <span class="role-pill role-{rolColor(user.admin_role)}">
              {#if user.admin_role === 'master'}
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              {:else}
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              {/if}
              {rolLabel(user.admin_role)}
            </span>
          </div>
        </div>

        <!-- Datos de cuenta -->
        <div class="card datos-card">
          <h3 class="card-titulo">Datos de la cuenta</h3>
          <div class="datos-lista">
            <div class="dato-fila">
              <span class="dato-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                Nombre
              </span>
              <span class="dato-valor">{user.first_name}</span>
            </div>
            <div class="dato-fila">
              <span class="dato-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                Apellido
              </span>
              <span class="dato-valor">{user.last_name}</span>
            </div>
            <div class="dato-fila">
              <span class="dato-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                Correo
              </span>
              <span class="dato-valor correo">{user.email}</span>
            </div>
            <div class="dato-fila">
              <span class="dato-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                Rol
              </span>
              <span class="dato-valor">{rolLabel(user.admin_role)}</span>
            </div>
            <div class="dato-fila">
              <span class="dato-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                ID de usuario
              </span>
              <span class="dato-valor id-val">#{user.id}</span>
            </div>
          </div>
        </div>

        <!-- Sesión y credenciales -->
        <div class="card sesion-card">
          <h3 class="card-titulo">Sesión y dispositivo</h3>

          <div class="sesion-bloque">
            <div class="sesion-row">
              <div class="sesion-icon sesion-icon-ok">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              </div>
              <div>
                <p class="sesion-titulo">Sesión activa</p>
                <p class="sesion-desc">Estás autenticado mediante una sesión segura en el servidor.</p>
              </div>
            </div>

            <div class="divider"></div>

            <div class="sesion-row">
              <div class="sesion-icon {credencialesGuardadas ? 'sesion-icon-warn' : 'sesion-icon-neutral'}">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </div>
              <div class="sesion-cred-body">
                <p class="sesion-titulo">Credenciales guardadas</p>
                {#if credencialesGuardadas}
                  <p class="sesion-desc">Tus credenciales están guardadas en este dispositivo (función "Recordarme").</p>
                  <button class="btn-borrar-cred" on:click={borrarCredenciales}>
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
                    Borrar credenciales guardadas
                  </button>
                {:else}
                  <p class="sesion-desc">No hay credenciales guardadas en este dispositivo.</p>
                {/if}
              </div>
            </div>
          </div>
        </div>

      </div>
    {:else}
      <div class="sin-usuario">Cargando información del usuario...</div>
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
    gap: 1.75rem;
    padding: 2rem;
    min-width: 0;
  }

  .main-header h1 {
    margin: 0 0 0.2rem;
    font-size: 1.65rem;
    color: #09263a;
    font-weight: 800;
  }

  .main-header p { margin: 0; color: #6a8090; font-size: 0.88rem; }

  /* Grid de tarjetas */
  .perfil-grid {
    display: grid;
    grid-template-columns: 280px 1fr;
    grid-template-rows: auto auto;
    gap: 1.25rem;
    align-items: start;
  }

  .card {
    background: white;
    border-radius: 18px;
    padding: 1.75rem;
    box-shadow: 0 2px 12px rgba(9,38,58,0.06);
    border: 1px solid rgba(9,38,58,0.06);
  }

  /* Tarjeta principal de perfil */
  .perfil-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.25rem;
    text-align: center;
    grid-row: span 2;
  }

  .avatar-grande {
    width: 88px;
    height: 88px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0d6ea8 0%, #0a4a7a 100%);
    color: white;
    font-size: 1.65rem;
    font-weight: 800;
    display: grid;
    place-items: center;
    text-transform: uppercase;
    box-shadow: 0 8px 24px rgba(13,110,168,0.3);
    letter-spacing: 0.05em;
  }

  .perfil-nombre-bloque {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.6rem;
  }

  .perfil-nombre {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 700;
    color: #09263a;
    line-height: 1.2;
  }

  .role-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 99px;
    padding: 0.3rem 0.85rem;
  }

  .role-master { background: rgba(249,115,22,0.12); color: #c2410c; border: 1px solid rgba(249,115,22,0.25); }
  .role-viewer { background: rgba(13,110,168,0.1);  color: #0d6ea8; border: 1px solid rgba(13,110,168,0.2); }

  /* Tarjeta de datos */
  .card-titulo {
    margin: 0 0 1.25rem;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8a9ba5;
  }

  .datos-lista { display: flex; flex-direction: column; gap: 0; }

  .dato-fila {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f0f5f8;
    gap: 1rem;
  }

  .dato-fila:last-child { border-bottom: none; }

  .dato-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.83rem;
    font-weight: 600;
    color: #6a8090;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .dato-valor {
    font-size: 0.9rem;
    color: #09263a;
    font-weight: 500;
    text-align: right;
    word-break: break-word;
  }

  .correo { color: #0d6ea8; font-family: monospace; }
  .id-val  { color: #8a9ba5; font-family: monospace; font-size: 0.82rem; }

  /* Tarjeta de sesión */
  .sesion-bloque { display: flex; flex-direction: column; gap: 1rem; }

  .sesion-row {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
  }

  .sesion-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    flex-shrink: 0;
  }

  .sesion-icon-ok      { background: rgba(46,204,113,0.12); color: #1a7a4a; }
  .sesion-icon-warn    { background: rgba(249,115,22,0.12); color: #c2410c; }
  .sesion-icon-neutral { background: rgba(143,211,255,0.12); color: #5a8ea8; }

  .sesion-titulo {
    margin: 0 0 0.2rem;
    font-size: 0.88rem;
    font-weight: 700;
    color: #09263a;
  }

  .sesion-desc {
    margin: 0;
    font-size: 0.82rem;
    color: #6a8090;
    line-height: 1.5;
  }

  .sesion-cred-body { display: flex; flex-direction: column; gap: 0.4rem; }

  .divider { height: 1px; background: #f0f5f8; }

  .btn-borrar-cred {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 0.35rem;
    padding: 0.35rem 0.75rem;
    border-radius: 8px;
    border: 1px solid rgba(231,76,60,0.25);
    background: rgba(231,76,60,0.06);
    color: #c0392b;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    align-self: flex-start;
  }

  .btn-borrar-cred:hover { background: rgba(231,76,60,0.14); }

  .sin-usuario {
    color: #6a8090;
    font-size: 0.9rem;
    padding: 2rem;
    text-align: center;
  }

  /* Responsive */
  @media (max-width: 900px) {
    .perfil-grid {
      grid-template-columns: 1fr;
      grid-template-rows: auto;
    }
    .perfil-card { grid-row: span 1; }
  }

  @media (max-width: 700px) {
    .admin-shell  { flex-direction: column; }
    .main-content { padding: 1rem; gap: 1.25rem; }
  }
</style>
