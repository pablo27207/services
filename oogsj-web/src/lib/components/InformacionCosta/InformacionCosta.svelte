<script>
  import { onMount } from 'svelte';
  import HeroInformacionCosta from './HeroInformacionCosta.svelte';
  import GridTemasCosta from './GridTemasCosta.svelte';
  import EscenariosCosta from './EscenariosCosta.svelte';
  import ChecklistCosta from './ChecklistCosta.svelte';
  import BanderasPlaya from './BanderasPlaya.svelte';
  import AvisosNavegante from './AvisosNavegante.svelte';

  const secciones = [
    { id: 'temas',      label: 'Condiciones del Mar',  icono: '🌊' },
    { id: 'escenarios', label: 'Escenarios',            icono: '⚠️' },
    { id: 'checklist',  label: 'Checklist',             icono: '✅' },
    { id: 'banderas',   label: 'Banderas',              icono: '🚩' },
    { id: 'avisos',     label: 'Avisos al Navegante',   icono: '📡' }
  ];

  let seccionActiva = '';

  onMount(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            seccionActiva = entry.target.id;
          }
        }
      },
      { rootMargin: '-20% 0px -65% 0px', threshold: 0 }
    );

    for (const sec of secciones) {
      const el = document.getElementById(sec.id);
      if (el) observer.observe(el);
    }

    return () => observer.disconnect();
  });

  function irA(id) {
    const el = document.getElementById(id);
    if (el) {
      const navAltura = 64;
      const top = el.getBoundingClientRect().top + window.scrollY - navAltura;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  }
</script>

<section class="informacion-costa">
  <HeroInformacionCosta />

  <nav class="nav-secciones" aria-label="Secciones de información de costa">
    <div class="nav-inner">
      {#each secciones as sec}
        <button
          class="nav-btn"
          class:activo={seccionActiva === sec.id}
          on:click={() => irA(sec.id)}
        >
          <span class="nav-icono" aria-hidden="true">{sec.icono}</span>
          <span class="nav-label">{sec.label}</span>
        </button>
      {/each}
    </div>
  </nav>

  <div id="temas">   <GridTemasCosta />   </div>
  <div id="escenarios"> <EscenariosCosta /> </div>
  <div id="checklist">  <ChecklistCosta />  </div>
  <div id="banderas">   <BanderasPlaya />   </div>
  <div id="avisos">     <AvisosNavegante /> </div>
</section>

<style>
  .informacion-costa {
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(
      to bottom,
      #061826 0%,
      #0b2233 24%,
      #f4f8fb 24%,
      #f4f8fb 100%
    );
  }

  /* ── Barra de navegación sticky ─────────────────────── */
  .nav-secciones {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(4, 20, 34, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(143, 211, 255, 0.12);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
  }

  .nav-inner {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 1.5rem;
    display: flex;
    align-items: stretch;
    gap: 0;
    overflow-x: auto;
    scrollbar-width: none;
  }

  .nav-inner::-webkit-scrollbar { display: none; }

  .nav-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0 1.1rem;
    height: 52px;
    background: none;
    border: none;
    border-bottom: 2.5px solid transparent;
    color: rgba(200, 225, 245, 0.65);
    font-size: 0.88rem;
    font-weight: 600;
    white-space: nowrap;
    cursor: pointer;
    transition: color 0.2s ease, border-color 0.2s ease, background 0.2s ease;
    flex-shrink: 0;
  }

  .nav-btn:hover {
    color: #e5f3ff;
    background: rgba(143, 211, 255, 0.06);
  }

  .nav-btn.activo {
    color: #8fd3ff;
    border-bottom-color: #8fd3ff;
  }

  .nav-icono {
    font-size: 1rem;
    line-height: 1;
  }

  @media (max-width: 768px) {
    .nav-inner { padding: 0 0.75rem; gap: 0; }

    .nav-btn {
      padding: 0 0.75rem;
      height: 48px;
      font-size: 0.82rem;
      gap: 0.35rem;
    }

    .nav-label { display: none; }

    .nav-icono { font-size: 1.2rem; }
  }

  @media (max-width: 480px) {
    .nav-label { display: none; }
  }
</style>
