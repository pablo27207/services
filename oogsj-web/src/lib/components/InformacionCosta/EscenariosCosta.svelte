<script>
  import { escenariosCosta } from './informacionCostaData.js';
</script>

<section class="escenarios">
  <div class="encabezado">
    <p class="subtitulo">Escenarios frecuentes</p>
    <h2>Situaciones que conviene entender antes de ingresar</h2>
    <p class="texto">
      Algunas condiciones pueden parecer simples a primera vista, pero cambian mucho la experiencia
      en la costa. Entenderlas ayuda a tomar decisiones con más criterio.
    </p>
  </div>

  <div class="lista-escenarios">
    {#each escenariosCosta as escenario}
      <article class="escenario-card">
        <div class="top">
          <div class="icono">{escenario.icono}</div>
          <h3>{escenario.titulo}</h3>
        </div>

        <p class="descripcion">{escenario.descripcion}</p>

        <div class="detalle">
          <span>Qué implica</span>
          <p>{escenario.implica}</p>
        </div>

        <div class="accion">
          <span>Qué hacer</span>
          <p>{escenario.accion}</p>
        </div>
      </article>
    {/each}
  </div>
</section>

<style>
  .escenarios {
    padding: 2rem 1.5rem 6rem;
    max-width: 1280px;
    margin: 0 auto;
  }

  .encabezado {
    text-align: center;
    max-width: 820px;
    margin: 0 auto 3rem;
  }

  .subtitulo {
    color: #0d6ea8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
  }

  h2 {
    font-size: clamp(2rem, 4vw, 3rem);
    color: #09263a;
    margin: 0 0 1rem;
    line-height: 1.1;
  }

  .texto {
    color: #4f6575;
    font-size: 1.05rem;
    line-height: 1.7;
    margin: 0;
  }

  .lista-escenarios {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem;
  }

  .escenario-card {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbfd 100%);
    border-radius: 24px;
    padding: 1.6rem;
    border: 1px solid rgba(9, 38, 58, 0.08);
    box-shadow: 0 16px 36px rgba(9, 38, 58, 0.08);
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .top {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .icono {
    width: 68px;
    height: 68px;
    border-radius: 20px;
    display: grid;
    place-items: center;
    font-size: 1.9rem;
    background: linear-gradient(135deg, #dff4ff, #eef9ff);
    flex-shrink: 0;
  }

  h3 {
    margin: 0;
    color: #0a2436;
    font-size: 1.25rem;
    line-height: 1.2;
  }

  .descripcion {
    margin: 0;
    color: #546a79;
    line-height: 1.7;
    font-size: 1rem;
  }

  .detalle,
  .accion {
    background: #f2f8fb;
    border-radius: 18px;
    padding: 1rem;
  }

  .detalle span,
  .accion span {
    display: inline-block;
    font-size: 0.86rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #0c6a9c;
    margin-bottom: 0.5rem;
  }

  .detalle p,
  .accion p {
    margin: 0;
    color: #415766;
    line-height: 1.65;
  }

  .accion {
    background: #fff6e9;
  }

  .accion span {
    color: #c56c00;
  }

  @media (max-width: 900px) {
    .lista-escenarios {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 768px) {
    .escenarios {
      padding: 1rem 1rem 4.5rem;
    }

    .escenario-card {
      padding: 1.25rem;
      border-radius: 20px;
    }

    .top {
      align-items: flex-start;
    }

    .icono {
      width: 60px;
      height: 60px;
      border-radius: 18px;
      font-size: 1.7rem;
    }

    h3 {
      font-size: 1.1rem;
    }
  }
</style>