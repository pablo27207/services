<script>
  export let zonas = [];
  export let zonaSeleccionada;
  export let onSeleccionar = () => {};
</script>

<section class="bloque">
  <div class="bloque-header">
    <h2>Zonas costeras</h2>
    <p>Seleccioná una zona para ver su información principal.</p>
  </div>

  <div class="zonas-grid">
    {#each zonas as zona}
      <button
        class="zona-boton"
        class:activa={zonaSeleccionada?.id === zona.id}
        on:click={() => onSeleccionar(zona)}
      >
        <span class="zona-nombre">{zona.nombre}</span>
      </button>
    {/each}
  </div>
</section>

<style>
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
  }

  .bloque-header p {
    margin: 0;
    color: #94a3b8;
    line-height: 1.5;
    font-size: 0.95rem;
  }

  .zonas-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .zona-boton {
    width: 100%;
    padding: 0.95rem 1rem;
    border: 2px solid #244a68;
    border-radius: 0.95rem;
    background: #0f172a;
    color: #e2e8f0;
    cursor: pointer;
    transition: 0.2s ease;
    text-align: left;
  }

  .zona-boton:hover {
    border-color: #38bdf8;
    background: #132033;
    transform: translateY(-2px);
  }

  .zona-boton.activa {
    background: #1f6f8b;
    border-color: #38bdf8;
    color: white;
    box-shadow: 0 8px 18px rgba(31, 111, 139, 0.35);
  }

  .zona-nombre {
    font-size: 0.98rem;
    font-weight: 700;
    line-height: 1.3;
  }

  @media (min-width: 640px) {
    .zonas-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (min-width: 1024px) {
    .zonas-grid {
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
    }

    .bloque {
      margin-top: 2rem;
    }

    .bloque-header {
      margin-bottom: 1rem;
    }

    .zona-boton {
      padding: 1rem 1.2rem;
      border-radius: 1rem;
    }

    .zona-nombre {
      font-size: 1rem;
    }
  }
</style>