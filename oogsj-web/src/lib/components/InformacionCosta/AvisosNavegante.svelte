<script>
  import { onMount } from 'svelte';

  const API_URL = '/api/avisos/navegante?limit=10';

  let avisos = [];
  let cargando = true;
  let error = false;
  let avisoAbierto = null;

  onMount(async () => {
    try {
      const res = await fetch(API_URL);
      if (!res.ok) throw new Error('Error de red');
      const data = await res.json();
      avisos = data.avisos || [];
    } catch (e) {
      error = true;
    } finally {
      cargando = false;
    }
  });

  function toggle(id) {
    avisoAbierto = avisoAbierto === id ? null : id;
  }

  function formatFecha(iso) {
    if (!iso) return '—';
    const [y, m, d] = iso.split('-');
    return `${d}/${m}/${y}`;
  }
</script>

<section class="avisos">
  <div class="encabezado">
    <p class="subtitulo">Servicio de Hidrografía Naval</p>
    <h2>Avisos al Navegante</h2>
    <p class="texto">
      Información oficial sobre novedades de balizamiento, tareas subacuáticas y restricciones
      de navegación en el Golfo San Jorge y la provincia del Chubut.
      Fuente: SHN Argentina.
    </p>
  </div>

  {#if cargando}
    <div class="estado">
      <div class="spinner"></div>
      <p>Cargando avisos...</p>
    </div>

  {:else if error}
    <div class="estado error">
      <span>⚠️</span>
      <p>No se pudieron cargar los avisos en este momento.</p>
    </div>

  {:else if avisos.length === 0}
    <div class="estado">
      <span>📡</span>
      <p>No hay avisos recientes para esta región.</p>
    </div>

  {:else}
    <ul class="lista">
      {#each avisos as aviso (aviso.id)}
        {@const abierto = avisoAbierto === aviso.id}
        <li class="aviso-item" class:abierto>

          <button class="aviso-header" on:click={() => toggle(aviso.id)} aria-expanded={abierto}>
            <div class="aviso-meta">
              <span class="numero">Radioaviso N° {aviso.numero}</span>
              {#if aviso.tipo}
                <span class="tipo">{aviso.tipo}</span>
              {/if}
            </div>
            <span class="fecha">{formatFecha(aviso.fecha)}</span>
            <span class="chevron" class:rotado={abierto} aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M4.5 6.75l4.5 4.5 4.5-4.5"
                  stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
          </button>

          {#if abierto}
            <div class="aviso-body">
              {#if aviso.texto_es}
                <div class="bloque">
                  <span class="bloque-label">Español</span>
                  <p>{aviso.texto_es}</p>
                </div>
              {/if}
              {#if aviso.texto_en}
                <div class="bloque ingles">
                  <span class="bloque-label">English</span>
                  <p>{aviso.texto_en}</p>
                </div>
              {/if}
              <div class="aviso-footer">
                <span>Fuente: {aviso.fuente || 'SHN Argentina'}</span>
                {#if aviso.scraped_at}
                  <span>Actualizado: {formatFecha(aviso.scraped_at.slice(0,10))}</span>
                {/if}
              </div>
            </div>
          {/if}

        </li>
      {/each}
    </ul>

    <p class="disclaimer">
      Esta información es de carácter informativo y educativo. Para navegación operativa,
      consultá siempre los avisos oficiales vigentes del Servicio de Hidrografía Naval.
    </p>
  {/if}
</section>

<style>
  .avisos {
    padding: 3rem 1.5rem 5rem;
    max-width: 1280px;
    margin: 0 auto;
  }

  .encabezado {
    text-align: center;
    max-width: 820px;
    margin: 0 auto 3rem;
    padding: 2rem 2rem 2.5rem;
    background: linear-gradient(135deg, #041c2c 0%, #0a3352 100%);
    border-radius: 24px;
    box-shadow: 0 12px 40px rgba(4, 28, 44, 0.25);
  }

  .subtitulo {
    color: #8fd3ff;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.9rem;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .subtitulo::before,
  .subtitulo::after {
    content: '';
    display: inline-block;
    width: 32px;
    height: 1.5px;
    background: #8fd3ff;
    opacity: 0.5;
    vertical-align: middle;
  }

  h2 {
    font-size: clamp(2rem, 5vw, 3.2rem);
    color: white;
    margin: 0 0 1.1rem;
    line-height: 1.1;
    font-weight: 900;
    letter-spacing: -0.02em;
  }

  .texto {
    color: #a8cde0;
    font-size: 1.05rem;
    line-height: 1.75;
    margin: 0;
  }

  /* ── Estado (carga / error / vacío) ── */
  .estado {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    padding: 3rem;
    color: #5a6d7b;
    font-size: 1rem;
  }

  .estado.error { color: #b03025; }

  .spinner {
    width: 36px; height: 36px;
    border: 3px solid #dde8f0;
    border-top-color: #0d6ea8;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* ── Lista ── */
  .lista {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .aviso-item {
    background: white;
    border: 1.5px solid rgba(9, 38, 58, 0.09);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(8, 37, 58, 0.07);
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
  }

  .aviso-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(8, 37, 58, 0.1);
  }

  .aviso-item.abierto {
    border-color: #0d6ea8;
    box-shadow: 0 10px 32px rgba(13, 110, 168, 0.15);
  }

  /* ── Header ── */
  .aviso-header {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.1rem 1.4rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
  }

  .aviso-meta {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .numero {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0a2436;
  }

  .aviso-item.abierto .numero {
    color: #0d6ea8;
  }

  .tipo {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #0d6ea8;
    background: #e8f4fc;
    border-radius: 999px;
    padding: 0.25rem 0.65rem;
  }

  .fecha {
    font-size: 0.88rem;
    color: #7a8f9b;
    white-space: nowrap;
    flex-shrink: 0;
  }

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

  /* ── Body expandible ── */
  .aviso-body {
    padding: 0 1.4rem 1.4rem;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    border-top: 1px solid rgba(9, 38, 58, 0.06);
  }

  .bloque {
    background: #f4f8fb;
    border-radius: 14px;
    border-left: 3px solid #0d6ea8;
    padding: 1rem;
  }

  .bloque.ingles {
    background: #f8f8f5;
    border-left-color: #7a8f9b;
  }

  .bloque-label {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #0d6ea8;
    margin-bottom: 0.5rem;
  }

  .bloque.ingles .bloque-label { color: #7a8f9b; }

  .bloque p {
    margin: 0;
    font-size: 0.93rem;
    color: #415766;
    line-height: 1.7;
    white-space: pre-wrap;
    font-family: 'Courier New', monospace;
  }

  .aviso-footer {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    font-size: 0.82rem;
    color: #8a9ba5;
    padding-top: 0.25rem;
  }

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
  @media (max-width: 768px) {
    .avisos { padding: 1.5rem 1rem 4rem; }
    .aviso-header { padding: 1rem; }
    .aviso-body { padding: 0 1rem 1rem; }
    .numero { font-size: 0.92rem; }
  }
</style>