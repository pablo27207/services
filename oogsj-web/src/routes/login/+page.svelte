<script lang="ts">
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth';

  let email    = '';
  let password = '';
  let error    = '';
  let loading  = false;

  async function onSubmit(e: Event) {
    e.preventDefault();
    error   = '';
    loading = true;
    try {
      await authStore.login(email.trim().toLowerCase(), password);
      const next = new URLSearchParams(window.location.search).get('next') ?? '/admin/dashboard';
      goto(next);
    } catch (err: any) {
      error = err?.message ?? 'Error al iniciar sesión';
    } finally {
      loading = false;
    }
  }
</script>

<div class="login-page">
  <div class="login-card">

    <div class="login-header">
      <div class="logo-mark">
        <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
          <circle cx="18" cy="18" r="18" fill="#0d6ea8" opacity="0.15"/>
          <path d="M6 22 Q10 14 18 18 Q26 22 30 14" stroke="#0d6ea8" stroke-width="2.5"
            fill="none" stroke-linecap="round"/>
          <path d="M6 26 Q10 18 18 22 Q26 26 30 18" stroke="#0d6ea8" stroke-width="2"
            fill="none" stroke-linecap="round" opacity="0.6"/>
        </svg>
      </div>
      <div>
        <p class="logo-eyebrow">OOGSJ</p>
        <h1>Panel de administración</h1>
      </div>
    </div>

    <p class="login-desc">
      Acceso restringido al personal autorizado del Observatorio Oceanográfico del Golfo San Jorge.
    </p>

    {#if error}
      <div class="error-banner">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <circle cx="8" cy="8" r="7" stroke="#e74c3c" stroke-width="1.4"/>
          <path d="M8 5v4" stroke="#e74c3c" stroke-width="1.5" stroke-linecap="round"/>
          <circle cx="8" cy="11.5" r="0.75" fill="#e74c3c"/>
        </svg>
        {error}
      </div>
    {/if}

    <form on:submit={onSubmit} class="login-form">
      <label class="field">
        <span>Correo electrónico</span>
        <input
          type="email"
          bind:value={email}
          autocomplete="email"
          placeholder="usuario@organismo.gob.ar"
          required
          disabled={loading}
        />
      </label>

      <label class="field">
        <span>Contraseña</span>
        <input
          type="password"
          bind:value={password}
          autocomplete="current-password"
          placeholder="••••••••"
          required
          disabled={loading}
        />
      </label>

      <button type="submit" class="btn-login" disabled={loading}>
        {#if loading}
          <span class="spinner"></span> Verificando...
        {:else}
          Ingresar
        {/if}
      </button>
    </form>

    <p class="login-footer">
      Si no tenés credenciales, contactá al administrador del sistema.
    </p>

  </div>
</div>

<style>
  .login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #06121d 0%, #09263a 50%, #0b3050 100%);
    padding: 2rem 1rem;
  }

  .login-card {
    background: white;
    border-radius: 24px;
    padding: 2.5rem;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 32px 80px rgba(0,0,0,0.35);
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  /* Header */
  .login-header {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .logo-mark {
    flex-shrink: 0;
  }

  .logo-eyebrow {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #0d6ea8;
    margin: 0 0 0.15rem;
  }

  h1 {
    margin: 0;
    font-size: 1.25rem;
    color: #09263a;
    line-height: 1.2;
    font-weight: 700;
  }

  .login-desc {
    margin: 0;
    font-size: 0.88rem;
    color: #6a7f8e;
    line-height: 1.6;
    border-top: 1px solid #edf2f5;
    padding-top: 1.25rem;
  }

  /* Error */
  .error-banner {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #fdf0ef;
    border: 1px solid #f5c6c2;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.88rem;
    color: #9b2020;
    font-weight: 500;
  }

  /* Form */
  .login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .field span {
    font-size: 0.83rem;
    font-weight: 600;
    color: #3a5060;
  }

  .field input {
    border: 1.5px solid #d4e2ea;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    font-size: 0.95rem;
    color: #09263a;
    outline: none;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    background: #f8fbfd;
  }

  .field input:focus {
    border-color: #0d6ea8;
    box-shadow: 0 0 0 3px rgba(13,110,168,0.12);
    background: white;
  }

  .field input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-login {
    margin-top: 0.5rem;
    background: #0d6ea8;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.85rem;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    transition: background 0.2s ease, transform 0.15s ease;
  }

  .btn-login:hover:not(:disabled) {
    background: #0a5a8a;
    transform: translateY(-1px);
  }

  .btn-login:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }

  /* Spinner */
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.35);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .login-footer {
    margin: 0;
    text-align: center;
    font-size: 0.8rem;
    color: #9aafba;
    border-top: 1px solid #edf2f5;
    padding-top: 1rem;
  }
</style>
