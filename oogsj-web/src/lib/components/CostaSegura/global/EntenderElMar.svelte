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

  <div class="educacion-grid">
    {#each items as item}
      <article class="educacion-card">
        {#if item.imagen}
          <img src={item.imagen} alt={item.titulo} class="educacion-imagen" />
        {/if}

        <h3>{item.titulo}</h3>
        <p>{item.texto}</p>

        {#if item.fuente}
          <small>Fuente orientativa: {item.fuente}</small>
        {/if}
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

  .educacion-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }

  .educacion-card {
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #1f6f8b;
    border-radius: 1rem;
    padding: 1.3rem;
    color: #1e293b;
    transition: all 0.25s ease;
  }

  .educacion-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
    border-left: 6px solid #0f3d5e;
  }

  .educacion-imagen {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 0.85rem;
    margin-bottom: 0.9rem;
    display: block;
  }

  .educacion-card h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    color: #0f3d5e;
    font-weight: 700;
  }

  .educacion-card p {
    margin: 0 0 0.75rem 0;
    line-height: 1.6;
    color: #334155;
  }

  .educacion-card small {
    color: #64748b;
    line-height: 1.4;
  }
</style>