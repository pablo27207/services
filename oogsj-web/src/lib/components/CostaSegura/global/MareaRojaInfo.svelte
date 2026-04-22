<section class="bloque">
  <div class="bloque-header">
    <h2>Marea roja</h2>
    <p>Información básica para comprender este fenómeno y actuar con precaución.</p>
  </div>

  <div class="marea-roja-grid">
    <article class="info-card destacado">
      <h3>¿Qué es la marea roja?</h3>
      <p>
        La marea roja es un fenómeno natural asociado a la presencia y proliferación de ciertos
        microorganismos en el mar, algunos de los cuales pueden producir toxinas que se acumulan
        en moluscos y otros organismos marinos.
      </p>
    </article>

    <article class="info-card">
      <h3>Importante</h3>
      <p>
        No siempre cambia el color del agua ni es visible a simple vista. Que el mar se vea normal
        no significa que no exista riesgo.
      </p>
    </article>

    <article class="info-card">
      <h3>Precauciones principales</h3>
      <ul>
        <li>No consumir moluscos, mariscos u organismos recolectados sin control sanitario.</li>
        <li>Respetar alertas, vedas y comunicados oficiales vigentes.</li>
        <li>No asumir que cocinar los productos elimina el riesgo.</li>
        <li>Consultar siempre fuentes oficiales antes de recolectar o consumir productos del mar.</li>
      </ul>
    </article>

    <article class="info-card">
      <h3>Para la comunidad</h3>
      <p>
        Esta sección busca informar y promover el cuidado. La evaluación oficial de riesgo y las
        habilitaciones corresponden a organismos competentes.
      </p>
    </article>
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

  .marea-roja-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1rem;
  }

  .info-card {
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #b91c1c;
    border-radius: 1rem;
    padding: 1.3rem;
    color: #1e293b;
    transition: all 0.25s ease;
  }

  .info-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
  }

  .info-card h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    color: #7f1d1d;
    font-weight: 700;
  }

  .info-card p {
    margin: 0;
    line-height: 1.6;
    color: #334155;
  }

  .info-card ul {
    margin: 0;
    padding-left: 1.2rem;
  }

  .info-card li {
    margin-bottom: 0.6rem;
    line-height: 1.6;
    color: #334155;
  }

  .destacado {
    background: linear-gradient(180deg, #fff7f7 0%, #ffffff 100%);
  }
</style>