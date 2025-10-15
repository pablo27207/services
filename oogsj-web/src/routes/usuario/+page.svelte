<!-- src/routes/auth/+page.svelte -->
<section class="min-h-[60vh] flex items-center justify-center">
  <div class="w-full max-w-sm p-6 rounded-2xl bg-base-100 shadow">
    <h1 class="text-2xl font-semibold mb-4">Bienvenido</h1>
    <p class="mb-6 opacity-80">Elegí cómo querés continuar:</p>

    <div class="grid gap-3">
      <a href="/auth/login" class="btn btn-primary w-full">Iniciar sesión</a>
      <a href="/auth/register" class="btn btn-outline w-full">Crear cuenta</a>
    </div>
  </div>
</section>
