<script>
  import {
    zonasCosta,
    recomendacionesGenerales,
    contenidoEducativo,
    enlacesExternos,
    significadoBanderas
  } from './data/zonasCosta.js';

  import ZonaSelector from './zonas/ZonaSelector.svelte';
  import ZonaDetalle from './zonas/ZonaDetalle.svelte';
  import RecomendacionesGenerales from './global/RecomendacionesGenerales.svelte';
  import EntenderElMar from './global/EntenderElMar.svelte';
  import FuentesInformacion from './global/FuentesInformacion.svelte';
  import MareaRojaInfo from './global/MareaRojaInfo.svelte';

  const zonasVisibles = zonasCosta.filter((zona) => zona.visible);
  let zonaSeleccionada = zonasVisibles[0];

  function seleccionarZona(zona) {
    zonaSeleccionada = zona;
  }
</script>

<section class="costa-segura">
  <header class="hero">
    <div class="hero-texto">
      <p class="eyebrow">Observatorio Oceanográfico Golfo San Jorge</p>
      <h1>Costa Segura</h1>
      <p class="descripcion">
        Información pensada para la comunidad sobre zonas costeras habilitadas, actividades recreativas,
        recomendaciones de seguridad y conceptos básicos para comprender mejor el mar.
      </p>
    </div>
  </header>

  <ZonaSelector
    zonas={zonasVisibles}
    zonaSeleccionada={zonaSeleccionada}
    onSeleccionar={seleccionarZona}
  />

  <ZonaDetalle {zonaSeleccionada} />

  <RecomendacionesGenerales
    titulo="Recomendaciones generales de seguridad"
    descripcion="Consejos básicos para reducir riesgos al realizar actividades costeras."
    items={recomendacionesGenerales}
  />

  <RecomendacionesGenerales
    titulo="Explicación del color de banderas"
    descripcion="Referencia simple sobre señales habituales en espacios costeros."
    items={significadoBanderas}
  />

  <MareaRojaInfo />

  <EntenderElMar
    titulo="Cómo entender mejor el mar"
    descripcion="Conceptos básicos explicados de forma simple."
    items={contenidoEducativo}
  />

  <section class="bloque">
    <div class="bloque-header">
      <h2>Avisos a navegantes</h2>
      <p>Este espacio quedará preparado para mostrar avisos de forma más clara para la comunidad.</p>
    </div>

    <article class="placeholder-largo">
      <h3>Próximamente</h3>
      <p>
        En una próxima etapa se incorporará una sección para presentar avisos oficiales vinculados
        a navegación, seguridad y cambios relevantes en zonas costeras, redactados en lenguaje más accesible.
      </p>
    </article>
  </section>

  <FuentesInformacion
    titulo="Fuentes y sitios para ampliar información"
    descripcion="Para quienes quieran consultar información más técnica o detallada."
    items={enlacesExternos}
  />
</section>

<style>
  .costa-segura {
    max-width: 1300px;
    margin: 0 auto;
    padding: 1rem 0.85rem 3rem;
    color: #f8fafc;
  }

  .hero {
    margin-bottom: 1.5rem;
    padding: 1.25rem;
    border-radius: 1.2rem;
    background: linear-gradient(135deg, #0f3d5e, #1f6f8b);
    color: white;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
  }

  .hero-texto {
    max-width: 820px;
  }

  .eyebrow {
    margin: 0 0 0.45rem;
    font-size: 0.78rem;
    font-weight: 700;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .hero h1 {
    margin: 0 0 0.8rem;
    font-size: clamp(1.8rem, 5vw, 2.6rem);
    line-height: 1.1;
    color: #ffffff;
  }

  .descripcion {
    margin: 0;
    font-size: 0.98rem;
    line-height: 1.65;
    color: #e6f0f6;
  }

  .bloque {
    margin-top: 1.5rem;
  }

  .bloque-header {
    margin-bottom: 0.85rem;
  }

  .bloque-header h2 {
    margin: 0 0 0.35rem;
    font-size: clamp(1.25rem, 4vw, 1.7rem);
    color: #f8fafc;
    line-height: 1.2;
  }

  .bloque-header p {
    margin: 0;
    color: #94a3b8;
    line-height: 1.5;
    font-size: 0.95rem;
  }

  .placeholder-largo {
    background: #ffffff;
    border: 1px solid #d6e2ea;
    border-left: 6px solid #1f6f8b;
    border-radius: 1rem;
    padding: 1rem;
    color: #1e293b;
    transition: all 0.25s ease;
  }

  .placeholder-largo h3 {
    margin-top: 0;
    margin-bottom: 0.55rem;
    color: #0f3d5e;
    font-weight: 700;
    font-size: 1.05rem;
  }

  .placeholder-largo p {
    margin: 0;
    line-height: 1.6;
    color: #334155;
    font-size: 0.95rem;
  }

  @media (min-width: 768px) {
    .costa-segura {
      padding: 2rem 1rem 4rem;
    }

    .hero {
      margin-bottom: 2rem;
      padding: 2rem;
      border-radius: 1.5rem;
    }

    .bloque {
      margin-top: 2rem;
    }

    .bloque-header {
      margin-bottom: 1rem;
    }

    .placeholder-largo {
      padding: 1.3rem;
    }
  }
</style>