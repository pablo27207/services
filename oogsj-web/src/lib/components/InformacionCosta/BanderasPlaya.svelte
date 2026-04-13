<section class="banderas">
  <div class="encabezado">
    <p class="subtitulo">Seguridad en playas</p>
    <h2>Significado de las Banderas</h2>
    <p class="texto">
      Las banderas en playa indican las condiciones del mar y situaciones de emergencia.
      Respetá siempre las indicaciones del personal de guardavidas.
    </p>
  </div>

  <ul class="lista">

    <li class="bandera-item celeste">
      <div class="flag-wrap">
        <div class="asta"></div>
        <div class="flag"></div>
      </div>
      <div class="info">
        <span class="nombre">Bandera Celeste</span>
        <p class="descripcion">
          Mar bueno. Las condiciones son favorables para el baño. El mar está apto
          y el riesgo es bajo para todos los bañistas.
        </p>
      </div>
      <span class="badge permitido">Mar bueno</span>
    </li>

    <li class="bandera-item roja-negra">
      <div class="flag-wrap">
        <div class="asta"></div>
        <div class="flag bicolor">
          <div class="mitad top"></div>
          <div class="mitad bot"></div>
        </div>
      </div>
      <div class="info">
        <span class="nombre">Bandera Roja y Negra</span>
        <p class="descripcion">
          Mar peligroso. Las condiciones representan un riesgo alto para los bañistas.
          Se desaconseja fuertemente el ingreso al agua.
        </p>
      </div>
      <span class="badge peligroso">Mar peligroso</span>
    </li>

    <li class="bandera-item amarilla-negra">
      <div class="flag-wrap">
        <div class="asta"></div>
        <div class="flag bicolor">
          <div class="mitad top"></div>
          <div class="mitad bot"></div>
        </div>
      </div>
      <div class="info">
        <span class="nombre">Bandera Amarilla y Negra</span>
        <p class="descripcion">
          Mar dudoso. Existen condiciones de riesgo moderado: oleaje, corrientes o viento.
          Ingresá con precaución y bajo tu propia responsabilidad.
        </p>
      </div>
      <span class="badge dudoso">Mar dudoso</span>
    </li>

    <li class="bandera-item roja">
      <div class="flag-wrap">
        <div class="asta"></div>
        <div class="flag"></div>
      </div>
      <div class="info">
        <span class="nombre">Bandera Roja</span>
        <p class="descripcion">
          Prohibido bañarse. No se permite el ingreso al agua bajo ninguna circunstancia.
          Esta indicación debe respetarse sin excepción.
        </p>
      </div>
      <span class="badge prohibido">Prohibido bañarse</span>
    </li>

    <li class="bandera-item blanca">
      <div class="flag-wrap">
        <div class="asta"></div>
        <div class="flag"></div>
      </div>
      <div class="info">
        <span class="nombre">Bandera Blanca</span>
        <p class="descripcion">
          Niño o niña perdido/a. Se está buscando a un menor extraviado en la playa.
          Acercate de inmediato al puesto de guardavidas si encontrás a alguien
          o si perdés de vista a un niño.
        </p>
      </div>
      <span class="badge extraviado">Niño/a perdido/a</span>
    </li>

    <li class="bandera-item negra">
      <div class="flag-wrap">
        <div class="asta"></div>
        <div class="flag"></div>
      </div>
      <div class="info">
        <span class="nombre">Bandera Negra</span>
        <p class="descripcion">
          Evacuación de la playa por probable tormenta eléctrica. Salí del agua
          y alejate de la orilla de inmediato. Buscá refugio en un lugar cerrado
          y alejado de árboles o estructuras metálicas.
        </p>
      </div>
      <span class="badge evacuacion">Evacuación</span>
    </li>

  </ul>

  <p class="disclaimer">
    Esta información es de carácter informativo y educativo. Respetá siempre las indicaciones
    del guardavidas habilitado y la señalización oficial de cada playa.
  </p>
</section>

<style>
  .banderas {
    padding: 2rem 1.5rem 4rem;
    max-width: 1280px;
    margin: 0 auto;
  }

  /* ── Encabezado ── */
  .encabezado {
    text-align: center;
    max-width: 680px;
    margin: 0 auto 2.5rem;
  }

  .subtitulo {
    color: #0d6ea8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
  }

  h2 {
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    color: #09263a;
    margin: 0 0 1rem;
    line-height: 1.1;
  }

  .texto {
    color: #4f6575;
    font-size: 1rem;
    line-height: 1.7;
    margin: 0;
  }

  /* ── Lista ── */
  .lista {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  /* ── Item base ── */
  .bandera-item {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: white;
    border: 1.5px solid rgba(9, 38, 58, 0.07);
    border-radius: 18px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 4px 16px rgba(8, 37, 58, 0.05);
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
  }

  .bandera-item:hover {
    box-shadow: 0 8px 28px rgba(8, 37, 58, 0.1);
  }

  /* ── Estructura bandera ── */
  .flag-wrap {
    display: flex;
    align-items: flex-start;
    gap: 0;
    flex-shrink: 0;
  }

  .asta {
    width: 3px;
    height: 64px;
    background: #5a6d7b;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .flag {
    width: 44px;
    height: 32px;
    border-radius: 0 3px 3px 0;
    flex-shrink: 0;
  }

  /* Bandera bicolor (mitades horizontales) */
  .flag.bicolor {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border-radius: 0 3px 3px 0;
    padding: 0;
  }

  .mitad {
    flex: 1;
    width: 100%;
  }

  /* ── Colores por tipo ── */
  /* Celeste */
  .celeste .flag         { background: #5bc8e8; }
  .celeste               { border-left: 4px solid #5bc8e8; }

  /* Roja y Negra */
  .roja-negra .mitad.top { background: #e74c3c; }
  .roja-negra .mitad.bot { background: #1a1a2e; }
  .roja-negra            { border-left: 4px solid #e74c3c; }

  /* Amarilla y Negra */
  .amarilla-negra .mitad.top { background: #f1c40f; }
  .amarilla-negra .mitad.bot { background: #1a1a2e; }
  .amarilla-negra            { border-left: 4px solid #f1c40f; }

  /* Roja */
  .roja .flag { background: #e74c3c; }
  .roja       { border-left: 4px solid #e74c3c; }

  /* Blanca */
  .blanca .flag { background: #f8f9fa; border: 1px solid #dee2e6; }
  .blanca       { border-left: 4px solid #adb5bd; }

  /* Negra */
  .negra .flag { background: #1a1a2e; }
  .negra       { border-left: 4px solid #1a1a2e; }

  /* ── Texto info ── */
  .info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .nombre {
    font-size: 1rem;
    font-weight: 700;
    color: #0a2436;
  }

  .descripcion {
    margin: 0;
    font-size: 0.92rem;
    color: #4f6575;
    line-height: 1.6;
  }

  /* ── Badges ── */
  .badge {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border-radius: 999px;
    padding: 0.3rem 0.75rem;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .permitido  { background: #d8f4fb; color: #0b6a85; }
  .peligroso  { background: #fde8e8; color: #9b2020; }
  .dudoso     { background: #fef9e0; color: #8a6800; }
  .prohibido  { background: #fde8e8; color: #9b2020; }
  .extraviado { background: #f0f0f0; color: #444444; }
  .evacuacion { background: #e8e8e8; color: #1a1a2e; }

  /* ── Disclaimer ── */
  .disclaimer {
    margin-top: 2rem;
    padding: 1rem 1.25rem;
    background: #f0f7fb;
    border-radius: 14px;
    border-left: 3px solid #8fd3ff;
    font-size: 0.88rem;
    color: #4f6575;
    line-height: 1.6;
    font-style: italic;
  }

  /* ── Mobile ── */
  @media (max-width: 640px) {
    .banderas { padding: 1.5rem 1rem 3rem; }

    .bandera-item {
      flex-wrap: wrap;
      gap: 1rem;
      padding: 1rem;
    }

    .badge {
      order: -1;
      align-self: flex-start;
    }

    .asta  { height: 48px; }
    .flag  { width: 36px; height: 26px; }
  }
</style>
