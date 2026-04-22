<script>
  export let items = [];
</script>

<section class="bloque">
  <div class="bloque-header">
    <h2>Condiciones del mar</h2>
    <p>Información explicativa orientada a la comunidad sobre los datos que más suelen importar.</p>
  </div>

  <div class="condiciones-grid">
    {#each items as item}
      <article class="placeholder-card">
        <h3>{item.titulo}</h3>
        <p>{item.texto}</p>
      </article>
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

  .condiciones-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }

  .placeholder-card {
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #1f6f8b;
    border-radius: 1rem;
    padding: 1.3rem;
    color: #1e293b;
    transition: all 0.25s ease;
  }

  .placeholder-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
    border-left: 6px solid #0f3d5e;
  }

  .placeholder-card h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    color: #0f3d5e;
    font-weight: 700;
  }

  .placeholder-card p {
    margin: 0;
    line-height: 1.6;
    color: #334155;
  }
</style>