<script lang="ts">
  import { onMount } from 'svelte';

  type Noticia = {
    id: number;
    titulo: string;
    contenido: string;
    categoria: string | null;
    imagen_url: string | null;
    publicado: boolean;
    created_at: string | null;
  };

  const API = import.meta.env.VITE_API_URL ?? '';
  const POR_PAGINA = 3;

  let noticias: Noticia[] = [];
  let pagina   = 1;
  let cargando = true;
  let error: string | null = null;

  async function cargar() {
    cargando = true;
    error    = null;
    try {
      const res = await fetch(`${API}/api/noticias/`);
      if (!res.ok) throw new Error('Error al cargar noticias');
      const data = await res.json();
      noticias = data.noticias ?? [];
    } catch (e) {
      error = e instanceof Error ? e.message : 'Error desconocido';
    } finally {
      cargando = false;
    }
  }

  onMount(cargar);

  $: totalPaginas      = Math.ceil(noticias.length / POR_PAGINA);
  $: noticiasPaginadas = noticias.slice((pagina - 1) * POR_PAGINA, pagina * POR_PAGINA);

  function cambiarPagina(p: number) {
    if (p >= 1 && p <= totalPaginas) pagina = p;
  }

  function formatFecha(iso: string | null): string {
    if (!iso) return '';
    return new Date(iso).toLocaleDateString('es-AR', {
      year: 'numeric', month: 'long', day: 'numeric'
    });
  }

  function resumen(texto: string): string {
    return texto.length > 300 ? texto.slice(0, 300) + '…' : texto;
  }
</script>

<div class="my-8">
  <h2 class="text-2xl font-bold text-white mb-4">Noticias del Observatorio</h2>

  {#if cargando}
    <div class="text-center text-gray-400 py-12">Cargando noticias...</div>
  {:else if error}
    <div class="text-center text-red-400 py-12">{error}</div>
  {:else if noticias.length === 0}
    <div class="text-center text-gray-400 py-12">No hay noticias disponibles.</div>
  {:else}
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {#each noticiasPaginadas as noticia}
        <div class="bg-base-100 p-4 rounded shadow text-white border border-gray-700 hover:border-orange-400 hover:shadow-lg transition duration-200 flex flex-col">
          {#if noticia.imagen_url}
            <img
              src={noticia.imagen_url}
              alt={noticia.titulo}
              class="rounded-md h-40 w-full object-cover mb-3"
            />
          {/if}
          <h3 class="text-lg font-semibold text-orange-400 mb-1">{noticia.titulo}</h3>
          <p class="text-xs text-gray-400 mb-2">
            {formatFecha(noticia.created_at)}{noticia.categoria ? ` | ${noticia.categoria}` : ''}
          </p>
          <div class="text-sm text-gray-200 bg-gray-800 p-2 rounded overflow-y-auto flex-1" style="max-height: 100px;">
            {resumen(noticia.contenido)}
          </div>
        </div>
      {/each}
    </div>

    <!-- Paginación -->
    {#if totalPaginas > 1}
      <div class="flex justify-center mt-6 space-x-2 flex-wrap gap-y-2">
        <button
          on:click={() => cambiarPagina(pagina - 1)}
          class="px-3 py-1 bg-gray-700 text-white rounded disabled:opacity-50"
          disabled={pagina === 1}
        >Anterior</button>

        {#each Array(totalPaginas) as _, idx}
          <button
            on:click={() => cambiarPagina(idx + 1)}
            class="px-3 py-1 rounded border border-gray-600 text-white hover:bg-orange-500 hover:text-black {pagina === idx + 1 ? 'bg-orange-400 text-black' : ''}"
          >{idx + 1}</button>
        {/each}

        <button
          on:click={() => cambiarPagina(pagina + 1)}
          class="px-3 py-1 bg-gray-700 text-white rounded disabled:opacity-50"
          disabled={pagina === totalPaginas}
        >Siguiente</button>
      </div>
    {/if}
  {/if}
</div>
