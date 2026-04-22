<script>
  export let guardavidas = '';
  export let horarioGuardavidas = '';
</script>

<article class="mini-card">
  <h3>Guardavidas</h3>
  <p><strong>Disponibilidad:</strong> {guardavidas}</p>
  <p><strong>Horario:</strong> {horarioGuardavidas}</p>
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

  .mini-card p {
    margin: 0 0 0.6rem 0;
    line-height: 1.6;
    color: #334155;
  }

  .mini-card p:last-child {
    margin-bottom: 0;
  }
</style>