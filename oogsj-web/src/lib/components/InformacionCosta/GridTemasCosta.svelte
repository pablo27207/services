<script>
  import { categoriasTemas } from './informacionCostaData.js';
  import { slide } from 'svelte/transition';

  import OlasSVG       from './svgs/OlasSVG.svelte';
  import MareasSVG     from './svgs/MareasSVG.svelte';
  import VientoSVG     from './svgs/VientoSVG.svelte';
  import PrecaucionesSVG from './svgs/PrecaucionesSVG.svelte';

  const svgComponents = {
    olas:         OlasSVG,
    mareas:       MareasSVG,
    viento:       VientoSVG,
    precauciones: PrecaucionesSVG
  };

  /** @type {string | null} */
  let temaAbierto = null;

  /** @param {string} id */
  function toggleTema(id) {
    temaAbierto = temaAbierto === id ? null : id;
  }

  function getTemaActivo(categoria) {
    return categoria.temas.find((t) => t.id === temaAbierto) ?? null;
  }
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

  <div class="categorias">
    {#each categoriasTemas as categoria (categoria.id)}
      <div class="categoria-bloque">

        <div class="categoria-label">
          <span class="cat-icono">{categoria.icono}</span>
          <span class="cat-titulo">{categoria.titulo}</span>
        </div>

        <div class="cards-row" class:multi={categoria.temas.length > 1}>
          {#each categoria.temas as tema (tema.id)}
            {@const abierta = temaAbierto === tema.id}
            <button
              class="card"
              class:abierta
              on:click={() => toggleTema(tema.id)}
              aria-expanded={abierta}
            >
              <div class="card-inner">
                <div class="icono">{tema.icono}</div>
                <div class="card-texto">
                  <h3>{tema.titulo}</h3>
                  <p>{tema.descripcion}</p>
                </div>
                <span class="chevron" class:rotado={abierta} aria-hidden="true">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M5 7.5l5 5 5-5" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </button>
          {/each}
        </div>

        {#if getTemaActivo(categoria)}
          {@const tema = getTemaActivo(categoria)}
          <div class="panel" transition:slide={{ duration: 320 }}>
            <div class="panel-inner">

              <!-- SVG: ancho completo, arriba -->
              <div class="panel-svg">
                <svelte:component this={svgComponents[/** @type {keyof typeof svgComponents} */ (tema.id)]} />
              </div>

              <!-- Contenido: título + intro + puntos 2 columnas -->
              <div class="panel-contenido">

                <div class="contenido-header">
                  <h4>{tema.titulo}</h4>
                  <p class="intro">{tema.contenido.intro}</p>
                </div>

                <ul class="puntos">
                  {#each tema.contenido.puntos as punto}
                    <li>
                      <strong>{punto.titulo}</strong>
                      <span>{punto.texto}</span>
                    </li>
                  {/each}
                </ul>

                {#if tema.contenido.nota}
                  <div class="nota">
                    <svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true">
                      <circle cx="7.5" cy="7.5" r="6.5" stroke="#0d6ea8" stroke-width="1.4" />
                      <path d="M7.5 6.5v4.5" stroke="#0d6ea8" stroke-width="1.4" stroke-linecap="round" />
                      <circle cx="7.5" cy="4.5" r="0.75" fill="#0d6ea8" />
                    </svg>
                    <p>{tema.contenido.nota}</p>
                  </div>
                {/if}

              </div>
            </div>
          </div>
        {/if}

      </div>
    {/each}
  </div>
</section>

<style>
  .temas {
    padding: 5rem 1.5rem 6rem;
    max-width: 1280px;
    margin: 0 auto;
  }

  /* ─── Encabezado ─────────────────────────────────── */
  .encabezado {
    text-align: center;
    max-width: 760px;
    margin: 0 auto 3.5rem;
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
    color: #a0b1bd;
    margin: 0 0 1rem;
    line-height: 1.1;
  }

  .texto {
    color: #4f6575;
    font-size: 1.05rem;
    line-height: 1.7;
    margin: 0;
  }

  /* ─── Categorías ─────────────────────────────────── */
  .categorias {
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
  }

  .categoria-bloque {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .categoria-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding-left: 0.5rem;
  }

  .cat-icono {
    font-size: 1.1rem;
    line-height: 1;
  }

  .cat-titulo {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #8a9ba5;
  }

  /* ─── Cards ──────────────────────────────────────── */
  .cards-row {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .cards-row.multi {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .card {
    background: white;
    border: 1.5px solid rgba(9, 38, 58, 0.07);
    border-radius: 20px;
    padding: 0;
    cursor: pointer;
    text-align: left;
    width: 100%;
    transition: box-shadow 0.25s ease, border-color 0.25s ease, transform 0.25s ease;
    box-shadow: 0 8px 24px rgba(8, 37, 58, 0.06);
  }

  .card:hover {
    box-shadow: 0 14px 36px rgba(8, 37, 58, 0.11);
    transform: translateY(-3px);
  }

  .card.abierta {
    border-color: #0d6ea8;
    box-shadow: 0 12px 32px rgba(13, 110, 168, 0.14);
    transform: translateY(0);
  }

  .card-inner {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
  }

  .icono {
    width: 56px;
    height: 56px;
    display: grid;
    place-items: center;
    border-radius: 16px;
    background: linear-gradient(135deg, #dff4ff, #eef9ff);
    font-size: 1.6rem;
    flex-shrink: 0;
  }

  .card-texto { flex: 1; min-width: 0; }

  .card-texto h3 {
    margin: 0 0 0.3rem;
    font-size: 1.05rem;
    color: #0a2436;
    line-height: 1.2;
    transition: color 0.2s ease;
  }

  .card.abierta .card-texto h3 { color: #0d6ea8; }

  .card-texto p {
    margin: 0;
    color: #5a6d7b;
    font-size: 0.92rem;
    line-height: 1.55;
  }

  /* ─── Chevron ─────────────────────────────────────── */
  .chevron {
    color: #a0b1bd;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    transition: transform 0.3s ease, color 0.2s ease;
  }

  .chevron.rotado {
    transform: rotate(180deg);
    color: #0d6ea8;
  }

  /* ─── Panel expandible ────────────────────────────── */
  .panel { overflow: hidden; }

  /* Layout: columna única — SVG arriba, contenido abajo */
  .panel-inner {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    background: white;
    border: 1.5px solid rgba(13, 110, 168, 0.12);
    border-radius: 24px;
    padding: 1.75rem;
    box-shadow: 0 16px 40px rgba(8, 37, 58, 0.08);
  }

  /* SVG: ancho completo, relación 700:280 (más panorámica, menos alta) */
  .panel-svg {
    width: 100%;
    aspect-ratio: 700 / 280;
    border-radius: 14px;
    overflow: hidden;
    background: #f0f7fb;
    flex-shrink: 0;
  }

  .panel-svg :global(svg) {
    width: 100%;
    height: 100%;
    display: block;
  }

  /* ─── Contenido: header + puntos 2 col + nota ─────── */
  .panel-contenido {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .contenido-header {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0 1.5rem;
    align-items: start;
  }

  .panel-contenido h4 {
    margin: 0;
    font-size: 1.2rem;
    color: #0a2436;
    line-height: 1.2;
    white-space: nowrap;
  }

  .intro {
    margin: 0;
    color: #4f6575;
    line-height: 1.65;
    font-size: 0.95rem;
  }

  /* Puntos en grilla de 2 columnas */
  .puntos {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.65rem;
  }

  .puntos li {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    padding: 0.8rem 1rem;
    background: #f4f8fb;
    border-radius: 12px;
    border-left: 3px solid #0d6ea8;
  }

  .puntos li strong {
    font-size: 0.78rem;
    font-weight: 700;
    color: #0d6ea8;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .puntos li span {
    font-size: 0.9rem;
    color: #415766;
    line-height: 1.55;
  }

  .nota {
    display: flex;
    gap: 0.65rem;
    align-items: flex-start;
    background: #eef6fb;
    border-radius: 12px;
    padding: 0.85rem 1rem;
  }

  .nota svg { flex-shrink: 0; margin-top: 2px; }

  .nota p {
    margin: 0;
    color: #4f6575;
    font-size: 0.88rem;
    line-height: 1.6;
    font-style: italic;
  }

  /* ─── Responsive ──────────────────────────────────── */
  @media (max-width: 900px) {
    .cards-row.multi { grid-template-columns: 1fr; }

    .contenido-header {
      grid-template-columns: 1fr;
      gap: 0.5rem;
    }

    .panel-contenido h4 { white-space: normal; }
  }

  @media (max-width: 640px) {
    .temas { padding: 4rem 1rem 5rem; }

    .panel-inner { padding: 1.25rem; border-radius: 20px; gap: 1.25rem; }

    .panel-svg { aspect-ratio: 700 / 320; }

    .card-inner { padding: 1rem 1.25rem; gap: 0.85rem; }

    .icono { width: 48px; height: 48px; font-size: 1.4rem; border-radius: 14px; }

    .card-texto h3 { font-size: 0.98rem; }
    .card-texto p  { font-size: 0.88rem; }

    /* Puntos a 1 columna en mobile chico */
    .puntos { grid-template-columns: 1fr; }

    .puntos li { padding: 0.7rem 0.85rem; border-radius: 10px; }
  }
</style>
