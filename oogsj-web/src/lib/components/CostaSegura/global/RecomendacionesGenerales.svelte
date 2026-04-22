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

  <div class="lista-card">
    <ul>
      {#each items as item}
        <li>{item}</li>
      {/each}
    </ul>
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

  .lista-card {
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #1f6f8b;
    border-radius: 1rem;
    padding: 1.3rem;
    color: #1e293b;
    transition: all 0.25s ease;
  }

  .lista-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
    border-left: 6px solid #0f3d5e;
  }

  .lista-card ul {
    margin: 0;
    padding-left: 1.2rem;
  }

  .lista-card li {
    margin-bottom: 0.6rem;
    line-height: 1.6;
    color: #334155;
  }
</style>