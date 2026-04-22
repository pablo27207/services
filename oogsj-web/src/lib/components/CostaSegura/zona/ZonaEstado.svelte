<script>
  export let estado;
</script>

<article class="estado-card">
  <p class="detalle-tag">Zona seleccionada</p>
  <h2>{estado?.titulo}</h2>
  <p class="detalle-descripcion">{estado?.texto}</p>
</article>

<style>
  .estado-card {
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #1f6f8b;
    border-radius: 1rem;
    padding: 1.3rem;
    color: #1e293b;
  }

  .detalle-tag {
    margin: 0 0 0.5rem 0;
    color: #38bdf8;
    font-size: 0.95rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  h2 {
    margin: 0 0 0.75rem 0;
    font-size: 1.8rem;
    color: #0f3d5e;
  }

  .detalle-descripcion {
    margin: 0;
    line-height: 1.7;
    color: #334155;
  }
</style>