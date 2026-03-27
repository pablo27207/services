<section class="hero">
  <div class="overlay"></div>

  <div class="contenido">
    <p class="eyebrow">Observatorio Oceanográfico Golfo San Jorge</p>
    <h1>Información de Costa</h1>
    <p class="descripcion">
      Un espacio visual y educativo para comprender mejor el mar, las condiciones costeras
      y las recomendaciones básicas para disfrutar la costa con mayor conciencia.
    </p>

    <div class="badges">
      <span>Viento</span>
      <span>Oleaje</span>
      <span>Mareas</span>
      <span>Actividades</span>
      <span>Recomendaciones</span>
    </div>
  </div>
</section>

<style>
  .hero {
    position: relative;
    min-height: 75vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 1.5rem;
    background:
      linear-gradient(rgba(4, 18, 31, 0.55), rgba(4, 18, 31, 0.7)),
      url('/imagenes/costa-hero.jpg') center/cover no-repeat;
    overflow: hidden;
  }

  .overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(5, 24, 39, 0.15) 0%, rgba(5, 24, 39, 0.55) 100%);
  }

  .contenido {
    position: relative;
    z-index: 1;
    max-width: 900px;
    text-align: center;
    color: white;
  }

  .eyebrow {
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8fd3ff;
    margin-bottom: 1rem;
  }

  h1 {
    font-size: clamp(2.5rem, 6vw, 5rem);
    line-height: 1.05;
    margin: 0 0 1.25rem;
    font-weight: 800;
  }

  .descripcion {
    font-size: clamp(1rem, 2vw, 1.25rem);
    line-height: 1.7;
    color: #e5f3ff;
    max-width: 760px;
    margin: 0 auto 2rem;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.75rem;
  }

  .badges span {
    padding: 0.7rem 1rem;
    border-radius: 999px;
    background: rgba(143, 211, 255, 0.12);
    border: 1px solid rgba(143, 211, 255, 0.28);
    backdrop-filter: blur(6px);
    color: #f4fbff;
    font-size: 0.95rem;
    font-weight: 600;
  }

  @media (max-width: 768px) {
    .hero {
      min-height: 65vh;
      padding: 3rem 1rem;
    }

    .descripcion {
      font-size: 1rem;
      line-height: 1.6;
    }

    .badges span {
      font-size: 0.88rem;
      padding: 0.6rem 0.9rem;
    }
  }
</style>