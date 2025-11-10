<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';

  let ready = false;
  let user = null;
  const unsub = auth.subscribe(v => user = v);

  onMount(() => {
    if (!user) {
      const next = encodeURIComponent('/admin/biblioteca');
      goto(`/login?next=${next}`);
      return;
    }
    ready = true;
  });
</script>

{#if ready}
  <slot />
{:else}
  <div class="min-h-[40vh] flex items-center justify-center">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{/if}
