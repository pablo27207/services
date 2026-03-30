<script>
  import { checklistCosta } from './informacionCostaData.js';
</script>

<section class="checklist">
  <div class="contenido">
    <div class="encabezado">
      <p class="subtitulo">Guía rápida</p>
      <h2>Antes de entrar al mar</h2>
      <p class="texto">
        Una secuencia simple para mirar el entorno con más atención y reducir decisiones apuradas.
      </p>
    </div>

    <div class="pasos">
      {#each checklistCosta as paso}
        <article class="paso">
          <div class="numero">{paso.numero}</div>

          <div class="info">
            <h3>{paso.titulo}</h3>
            <p>{paso.descripcion}</p>
          </div>
        </article>
      {/each}
    </div>
  </div>
</section>

<style>
  .checklist {
    padding: 0 1.5rem 6rem;
  }

  .contenido {
    max-width: 1280px;
    margin: 0 auto;
    background: linear-gradient(135deg, #0a2436 0%, #10344d 100%);
    border-radius: 32px;
    padding: 3rem 2rem;
    box-shadow: 0 24px 48px rgba(7, 28, 44, 0.18);
  }

  .encabezado {
    text-align: center;
    max-width: 760px;
    margin: 0 auto 2.5rem;
  }

  .subtitulo {
    color: #8fd3ff;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
  }

  h2 {
    font-size: clamp(2rem, 4vw, 3rem);
    color: white;
    margin: 0 0 1rem;
    line-height: 1.1;
  }

  .texto {
    color: #d9ebf7;
    font-size: 1.03rem;
    line-height: 1.7;
    margin: 0;
  }

  .pasos {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }

  .paso {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 22px;
    padding: 1.2rem;
    backdrop-filter: blur(4px);
  }

  .numero {
    width: 54px;
    height: 54px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #8fd3ff, #bde8ff);
    color: #0a2436;
    font-weight: 800;
    font-size: 1rem;
    flex-shrink: 0;
  }

  .info h3 {
    margin: 0 0 0.45rem;
    color: white;
    font-size: 1.05rem;
    line-height: 1.3;
  }

  .info p {
    margin: 0;
    color: #d4e5f1;
    line-height: 1.65;
    font-size: 0.97rem;
  }

  @media (max-width: 900px) {
    .pasos {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 768px) {
    .checklist {
      padding: 0 1rem 4.5rem;
    }

    .contenido {
      padding: 2rem 1rem;
      border-radius: 24px;
    }

    .paso {
      padding: 1rem;
      border-radius: 18px;
    }

    .numero {
      width: 48px;
      height: 48px;
      border-radius: 14px;
      font-size: 0.95rem;
    }
  }
</style>