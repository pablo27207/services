<script>
  export let titulo = '';
  export let descripcion = '';
  export let items = [];
</script>

<section class="bloque">
  <div class="bloque-header">
    <h2>{titulo}</h2>
    <p>{descripcion}</p>
  </div>

  <div class="fuentes-grid">
    {#each items as enlace}
      <a
        class="fuente-card"
        href={enlace.url}
        target="_blank"
        rel="noopener noreferrer"
      >
        <h3>{enlace.nombre}</h3>
        <p>{enlace.descripcion}</p>
      </a>
    {/each}
  </div>
</section>

<style>
  .bloque {
    margin-top: 2rem;
  }

  .bloque-header {
    margin-bottom: 1rem;
  }

  .bloque-header h2 {
    margin: 0 0 0.4rem;
    font-size: 1.7rem;
    color: #f8fafc;
  }

  .bloque-header p {
    margin: 0;
    color: #94a3b8;
    line-height: 1.5;
  }

  .fuentes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }

  .fuente-card {
    text-decoration: none;
    color: inherit;
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #1f6f8b;
    border-radius: 1rem;
    padding: 1.3rem;
    transition: all 0.25s ease;
  }

  .fuente-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
    border-left: 6px solid #0f3d5e;
    background: #f4fbff;
  }

  .fuente-card h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    color: #0f3d5e;
    font-weight: 700;
  }

  .fuente-card p {
    margin: 0;
    line-height: 1.6;
    color: #334155;
  }
</style>