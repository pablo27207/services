<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth';

  let ready = false;

  onMount(async () => {
    const user = await authStore.init();
    if (!user) {
      goto('/login?next=' + encodeURIComponent(window.location.pathname));
      return;
    }
    if (!user.is_admin) {
      goto('/login?next=' + encodeURIComponent(window.location.pathname));
      return;
    }
    ready = true;
  });
</script>

{#if ready}
  <slot />
{:else}
  <div class="guard-loading">
    <div class="spinner"></div>
    <p>Verificando acceso...</p>
  </div>
{/if}

<style>
  .guard-loading {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    background: #06121d;
    color: #8fd3ff;
    font-size: 0.95rem;
  }

  .spinner {
    width: 36px;
    height: 36px;
    border: 3px solid rgba(143,211,255,0.2);
    border-top-color: #0d6ea8;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }
</style>
