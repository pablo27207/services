<script lang="ts">
  import { page } from '$app/stores';
  import { auth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';

  let user: { username: string } | null = null;
  const unsub = auth.subscribe(v => user = v);

  function logout() {
    auth.logout();
    goto('/');
  }
</script>
<style>
  .navbar {
    position: fixed;
    top: 0; left: 0; width: 100%;
    z-index: 20;
  }
</style>

<div class="navbar-end">
  {#if user}
    <div class="dropdown dropdown-end">
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar placeholder">
        <div class="bg-neutral text-neutral-content rounded-full w-10">
          <span>{user.username.slice(0,1).toUpperCase()}</span>
        </div>
      </div>
      <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
        <li class="menu-title px-3">Hola, {user.username}</li>
        <li><a href="/admin/biblioteca" sveltekit:navigate>Panel de Biblioteca</a></li>
        <li><button on:click={logout}>Salir</button></li>
      </ul>
    </div>
  {:else}
    <a href="/login" sveltekit:navigate class="btn btn-ghost btn-circle" aria-label="Ingresar">
      <div class="indicator">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M5.121 19.07A10.97 10.97 0 0112 16c2.7 0 5.18.98 7.121 2.93M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </div>
    </a>
  {/if}
</div>