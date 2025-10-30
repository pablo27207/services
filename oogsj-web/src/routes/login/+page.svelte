<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { auth } from '$lib/stores/auth';

  let username = '';
  let password = '';
  let error = '';

  function onSubmit(e: Event) {
    e.preventDefault();
    if (username.trim().length < 3 || password.trim().length < 3) {
      error = 'Usuario y contraseña deben tener al menos 3 caracteres.';
      return;
    }
    auth.login(username.trim());
    const next = $page.url.searchParams.get('next') ?? '/admin/biblioteca';
    goto(next);
  }
</script>
<!-- ...resto igual... -->
<span></span>

<div class="min-h-[60vh] flex items-center justify-center p-4">
  <form class="card w-full max-w-sm bg-base-200 shadow-xl" on:submit={onSubmit}>
    <div class="card-body">
      <h2 class="card-title">Ingreso</h2>

      {#if error}
        <div class="alert alert-error">{error}</div>
      {/if}

      <label class="form-control">
        <span class="label-text">Usuario</span>
        <input class="input input-bordered" bind:value={username} autocomplete="username" />
      </label>

      <label class="form-control">
        <span class="label-text">Contraseña</span>
        <input type="password" class="input input-bordered" bind:value={password} autocomplete="current-password" />
      </label>

      <div class="card-actions justify-end mt-2">
        <button class="btn btn-primary" type="submit">Entrar</button>
      </div>
    </div>
  </form>
</div>
