<script>
  import { temasCosta } from './informacionCostaData.js';
</script>

<section class="temas">
  <div class="encabezado">
    <p class="subtitulo">Puntos clave</p>
    <h2>Lo que tenés que saber</h2>
    <p class="texto">
      Una guía visual para entender mejor los principales factores que influyen en la costa
      y en las actividades que se realizan cerca del mar.
    </p>
  </div>

  <div class="grid">
    {#each temasCosta as tema}
      <article class="card">
        <div class="icono">{tema.icono}</div>
        <h3>{tema.titulo}</h3>
        <p>{tema.descripcion}</p>
      </article>
    {/each}
  </div>
</section>

<style>
  .temas {
    padding: 5rem 1.5rem 6rem;
    max-width: 1280px;
    margin: 0 auto;
  }

  .encabezado {
    text-align: center;
    max-width: 760px;
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

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
  }

  .card {
    background: white;
    border-radius: 22px;
    padding: 1.5rem;
    box-shadow: 0 14px 35px rgba(8, 37, 58, 0.08);
    border: 1px solid rgba(9, 38, 58, 0.06);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }

  .card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 40px rgba(8, 37, 58, 0.14);
  }

  .icono {
    width: 64px;
    height: 64px;
    display: grid;
    place-items: center;
    border-radius: 18px;
    background: linear-gradient(135deg, #dff4ff, #eef9ff);
    font-size: 1.8rem;
    margin-bottom: 1rem;
  }

  h3 {
    margin: 0 0 0.75rem;
    font-size: 1.2rem;
    color: #0a2436;
  }

  .card p {
    margin: 0;
    color: #5a6d7b;
    line-height: 1.65;
    font-size: 0.98rem;
  }

  @media (max-width: 768px) {
    .temas {
      padding: 4rem 1rem 5rem;
    }

    .grid {
      gap: 1rem;
    }

    .card {
      padding: 1.25rem;
      border-radius: 18px;
    }
  }
</style>