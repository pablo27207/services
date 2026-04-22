<script lang="ts">
  import { goto } from '$app/navigation';
  import { authStore, type AdminUser } from '$lib/stores/auth';
  import { page } from '$app/stores';

  export let user: AdminUser | null = null;

  async function logout() {
    await authStore.logout();
    goto('/login');
  }

  $: currentPath = $page.url.pathname;
</script>

<aside class="sidebar">
  <div class="sidebar-brand">
    <svg width="28" height="28" viewBox="0 0 36 36" fill="none">
      <circle cx="18" cy="18" r="18" fill="#0d6ea8" opacity="0.2"/>
      <path d="M6 22 Q10 14 18 18 Q26 22 30 14" stroke="#8fd3ff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <path d="M6 26 Q10 18 18 22 Q26 26 30 18" stroke="#8fd3ff" stroke-width="2"   fill="none" stroke-linecap="round" opacity="0.55"/>
    </svg>
    <span>OOGSJ Admin</span>
  </div>

  <nav class="sidebar-nav">
    <a
      href="/admin/dashboard"
      class="nav-item"
      class:activo={currentPath === '/admin/dashboard'}
    >
      <span class="nav-icon">📊</span> Dashboard
    </a>
    <a
      href="/admin/biblioteca"
      class="nav-item"
      class:activo={currentPath.startsWith('/admin/biblioteca')}
    >
      <span class="nav-icon">📚</span> Biblioteca
    </a>
    <a
      href="/admin/noticias"
      class="nav-item"
      class:activo={currentPath.startsWith('/admin/noticias')}
    >
      <span class="nav-icon">📰</span> Noticias
    </a>
    <a
      href="/admin/especies"
      class="nav-item"
      class:activo={currentPath.startsWith('/admin/especies')}
    >
      <span class="nav-icon">🐟</span> Especies
    </a>
  </nav>

  <div class="sidebar-footer">
    {#if user}
      <div class="user-info">
        <div class="user-avatar">{user.first_name[0]}{user.last_name[0]}</div>
        <div class="user-text">
          <span class="user-name">{user.first_name} {user.last_name}</span>
          <span class="user-email">{user.email}</span>
        </div>
      </div>
    {/if}
    <button class="btn-logout" on:click={logout}>
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
        <polyline points="16 17 21 12 16 7"/>
        <line x1="21" y1="12" x2="9" y2="12"/>
      </svg>
      Cerrar sesión
    </button>
  </div>
</aside>

<style>
  .sidebar {
    width: 230px;
    flex-shrink: 0;
    background: #07192a;
    display: flex;
    flex-direction: column;
    padding: 1.5rem 0;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
  }

  .sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0 1.25rem 1.5rem;
    border-bottom: 1px solid rgba(143,211,255,0.1);
    font-size: 0.93rem;
    font-weight: 700;
    color: #8fd3ff;
  }

  .sidebar-nav {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    padding: 1.25rem 0.75rem;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.6rem 0.85rem;
    border-radius: 10px;
    font-size: 0.88rem;
    color: #7a9ab5;
    text-decoration: none;
    transition: background 0.2s, color 0.2s;
    cursor: pointer;
  }

  .nav-item:hover  { background: rgba(13,110,168,0.15); color: #cde8f5; }
  .nav-item.activo { background: rgba(13,110,168,0.25); color: #8fd3ff; font-weight: 600; }

  .nav-icon { font-size: 0.95rem; }

  .sidebar-footer {
    padding: 1rem 0.75rem 0;
    border-top: 1px solid rgba(143,211,255,0.1);
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.4rem 0.4rem;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #0d6ea8;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    text-transform: uppercase;
  }

  .user-text { display: flex; flex-direction: column; min-width: 0; }

  .user-name {
    font-size: 0.8rem;
    font-weight: 600;
    color: #cde8f5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .user-email {
    font-size: 0.7rem;
    color: #5a7a90;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .btn-logout {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
    padding: 0.55rem 0.85rem;
    border-radius: 10px;
    border: 1px solid rgba(231,76,60,0.25);
    background: rgba(231,76,60,0.08);
    color: #e07070;
    font-size: 0.83rem;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-logout:hover { background: rgba(231,76,60,0.18); color: #f09090; }

  @media (max-width: 700px) {
    .sidebar { width: 100%; height: auto; position: static; }
  }
</style>
