<script lang="ts">
  import { onMount } from 'svelte';

  type Especie = {
    id: number;
    nombre_comun: string;
    nombre_cientifico: string | null;
    descripcion: string | null;
    categoria: string | null;
    imagen_url: string | null;
  };

  const API = import.meta.env.VITE_API_URL ?? '';
  const POR_PAGINA = 6;

  let especies: Especie[] = [];
  let pagina   = 1;
  let cargando = true;
  let error: string | null = null;
  let busqueda  = '';
  let catFiltro = '';
  let expandidos: Record<number, boolean> = {};

  const CATEGORIAS = ['Peces', 'Mamíferos marinos', 'Aves costeras', 'Invertebrados', 'Algas', 'Reptiles', 'Otro'];

  async function cargar() {
    cargando = true;
    error    = null;
    try {
      const params = new URLSearchParams();
      if (busqueda.trim())  params.set('q', busqueda.trim());
      if (catFiltro.trim()) params.set('categoria', catFiltro.trim());
      const res = await fetch(`${API}/api/especies/?${params}`);
      if (!res.ok) throw new Error('Error al cargar especies');
      const data = await res.json();
      especies = data.especies ?? [];
      pagina   = 1;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Error desconocido';
    } finally {
      cargando = false;
    }
  }

  onMount(cargar);

  $: totalPaginas      = Math.ceil(especies.length / POR_PAGINA);
  $: especiesPaginadas = especies.slice((pagina - 1) * POR_PAGINA, pagina * POR_PAGINA);

  function cambiarPagina(p: number) {
    if (p >= 1 && p <= totalPaginas) {
      pagina = p;
    }
  }

  function toggleExpand(id: number) {
    expandidos = { ...expandidos, [id]: !expandidos[id] };
  }

  function resumen(texto: string): string {
    return texto.length > 220 ? texto.slice(0, 220) + '…' : texto;
  }
</script>

<!-- Filtros -->
<div class="flex flex-wrap gap-3 mb-6 mt-4">
  <input
    type="text"
    bind:value={busqueda}
    on:keydown={(e) => e.key === 'Enter' && cargar()}
    placeholder="Buscar por nombre..."
    class="input input-bordered bg-base-200 text-white border-gray-600 flex-1 min-w-[180px]"
  />
  <select
    bind:value={catFiltro}
    on:change={cargar}
    class="select select-bordered bg-base-200 text-white border-gray-600"
  >
    <option value="">Todas las categorías</option>
    {#each CATEGORIAS as cat}
      <option value={cat}>{cat}</option>
    {/each}
  </select>
  <button on:click={cargar} class="btn bg-orange-500 hover:bg-orange-600 text-white border-none">
    Buscar
  </button>
</div>

{#if cargando}
  <div class="text-center text-gray-400 py-16">Cargando especies...</div>
{:else if error}
  <div class="text-center text-red-400 py-16">{error}</div>
{:else if especies.length === 0}
  <div class="text-center text-gray-400 py-16">No se encontraron especies.</div>
{:else}
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-8">
    {#each especiesPaginadas as especie}
      <div class="bg-base-100 shadow-xl rounded-lg overflow-hidden p-4 text-white flex flex-col">
        {#if especie.imagen_url}
          <img
            src={especie.imagen_url}
            alt={especie.nombre_comun}
            class="rounded-md h-48 w-full object-cover mb-4"
          />
        {:else}
          <div class="h-48 w-full bg-gray-800 rounded-md mb-4 flex items-center justify-center text-gray-500 text-sm">
            Sin imagen
          </div>
        {/if}

        <h3 class="text-xl font-bold text-orange-400">{especie.nombre_comun}</h3>

        {#if especie.nombre_cientifico}
          <p class="italic text-sm text-gray-300 mb-1">{especie.nombre_cientifico}</p>
        {/if}

        {#if especie.categoria}
          <span class="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded mb-2 self-start">
            {especie.categoria}
          </span>
        {/if}

        {#if especie.descripcion}
          <p class="text-gray-200 text-sm mt-1 flex-1">
            {expandidos[especie.id] ? '' : resumen(especie.descripcion)}
          </p>

          <button
            class="mt-2 text-blue-400 underline hover:text-blue-300 transition text-sm self-start"
            on:click={() => toggleExpand(especie.id)}
          >
            {expandidos[especie.id] ? 'Ver menos' : 'Ver más'}
          </button>

          {#if expandidos[especie.id]}
            <div class="mt-2 whitespace-pre-wrap text-gray-300 text-sm max-h-96 overflow-y-auto border-t pt-2 border-gray-600">
              {especie.descripcion}
            </div>
          {/if}
        {/if}
      </div>
    {/each}
  </div>

  <!-- Paginación -->
  {#if totalPaginas > 1}
    <div class="mt-10 flex justify-center gap-2 flex-wrap">
      <button
        class="px-3 py-1 bg-gray-700 text-white rounded disabled:opacity-50"
        on:click={() => cambiarPagina(pagina - 1)}
        disabled={pagina === 1}
      >◀ Anterior</button>

      {#each Array(totalPaginas) as _, i}
        <button
          class="px-3 py-1 rounded {pagina === i + 1 ? 'bg-orange-500 text-white' : 'bg-gray-700 text-gray-300'}"
          on:click={() => cambiarPagina(i + 1)}
        >{i + 1}</button>
      {/each}

      <button
        class="px-3 py-1 bg-gray-700 text-white rounded disabled:opacity-50"
        on:click={() => cambiarPagina(pagina + 1)}
        disabled={pagina === totalPaginas}
      >Siguiente ▶</button>
    </div>
  {/if}
{/if}
