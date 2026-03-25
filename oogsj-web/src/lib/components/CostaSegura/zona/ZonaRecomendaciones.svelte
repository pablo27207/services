<script>
  export let titulo = 'Recomendaciones';
  export let items = [];
</script>

<section class="bloque">
  <article class="lista-card">
    <h3>{titulo}</h3>
    <ul>
      {#each items as item}
        <li>{item}</li>
      {/each}
    </ul>
  </article>
</section>

<style>
  .bloque {
    margin-top: 1rem;
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

  .lista-card h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    color: #0f3d5e;
    font-weight: 700;
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