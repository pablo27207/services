<script>
  export let actividades = [];
</script>

<article class="mini-card">
  <h3>Actividades</h3>
  <ul>
    {#each actividades as actividad}
      <li>{actividad}</li>
    {/each}
  </ul>
</article>

<style>
  .mini-card {
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #1f6f8b;
    border-radius: 1rem;
    padding: 1.3rem;
    color: #1e293b;
    transition: all 0.25s ease;
  }

  .mini-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
    border-left: 6px solid #0f3d5e;
  }

  .mini-card h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    color: #0f3d5e;
    font-weight: 700;
  }

  .mini-card ul {
    margin: 0;
    padding-left: 1.2rem;
  }

  .mini-card li {
    margin-bottom: 0.6rem;
    line-height: 1.6;
    color: #334155;
  }
</style>