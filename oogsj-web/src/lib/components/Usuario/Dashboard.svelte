<script>
  export let user;
  export let onLogout;
  // ... (El resto del script con 'papers', 'editingId', y las funciones startEdit, saveEdit, etc. es IGUAL) ...
  let papers = [
    { id: 1, title: 'Análisis de Svelte', author: 'F. Smith', year: 2023, isVisible: true },
    { id: 2, title: 'Optimización de APIs', author: 'J. Doe', year: 2024, isVisible: true },
    { id: 3, title: 'Patrones de Diseño', author: 'A. B. Johnson', year: 2022, isVisible: true }
  ];
  // ... (funciones de CRUD) ...
</script>

<div class="dashboard-container">
  <header>
    <h1>Bienvenido, {user.name}</h1>
    <button on:click={onLogout}>Cerrar Sesión</button>
  </header>

  <section class="user-info">
    <h2>Información Personal</h2>
    <p><strong>Nombre:</strong> {user.name}</p>
    <p><strong>Email:</strong> {user.email}</p>
    {#if user.message}
        <p><strong>Mensaje Favorito:</strong> *{user.message}*</p>
    {/if}
  </section>

  <section class="papers-section">
    </section>
</div>

<style>
  /* ... Estilos ... */
</style>