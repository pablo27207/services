<script lang="ts">
  import { onMount } from 'svelte';

  // --- Estado ---
  let q = '';
  let sort: 'year_desc' | 'year_asc' | 'citations_desc' | 'citations_asc' | 'title_asc' = 'year_desc';
  let page = 1;
  let limit = 10;

  let loading = false;
  let errorMsg = '';
  let total = 0;
  let items: Array<{
    id: number;
    title: string;
    year: number | null;
    venue: string | null;
    citations: number;
    url: string | null;
    doi: string | null;
  }> = [];

  // --- Helpers ---
  const endpointBase = '/api/library';

  async function fetchList() {
    loading = true;
    errorMsg = '';
    try {
      const url =
        q.trim().length > 0
          ? `${endpointBase}/search?q=${encodeURIComponent(q)}&limit=${limit}&page=${page}`
          : `${endpointBase}/list?sort=${sort}&limit=${limit}&page=${page}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      items = data.items ?? [];
      total = data.total ?? 0;
    } catch (e) {
      errorMsg = 'No pude cargar los documentos. Probá de nuevo.';
      console.error(e);
    } finally {
      loading = false;
    }
  }

  // debounce para el buscador
  let t: ReturnType<typeof setTimeout> | null = null;
  function onSearchInput(v: string) {
    q = v;
    page = 1; // reset página al cambiar búsqueda
    if (t) clearTimeout(t);
    t = setTimeout(fetchList, 350);
  }

  function goPrev() {
    if (page > 1) {
      page -= 1;
      fetchList();
    }
  }
  function goNext() {
    const maxPage = Math.max(1, Math.ceil(total / limit));
    if (page < maxPage) {
      page += 1;
      fetchList();
    }
  }

  function onChangeSort(v: string) {
    // si hay búsqueda activa, mantenemos búsqueda; si no, ordenamos la lista
    sort = (v as typeof sort);
    page = 1;
    fetchList();
  }

  onMount(fetchList);
</script>

<!-- UI -->
<div class="max-w-5xl mx-auto mt-4 px-2 md:px-0">
  <!-- Barra de búsqueda y orden -->
  <div class="flex flex-col md:flex-row gap-3 md:items-center md:justify-between mb-4">
    <div class="flex-1">
      <input
        type="search"
        class="input input-bordered w-full"
        placeholder="Buscar por título, venue, DOI o URL…"
        on:input={(e) => onSearchInput((e.target as HTMLInputElement).value)}
        value={q}
      />
    </div>

    <div class="flex items-center gap-2">
      <label class="text-sm opacity-70">Ordenar:</label>
      <select class="select select-bordered"
        bind:value={sort}
        on:change={(e) => onChangeSort((e.target as HTMLSelectElement).value)}
        disabled={q.trim().length > 0 /* en búsqueda no forzamos orden diferente al default del backend */}
      >
        <option value="year_desc">Año ↓ (recientes)</option>
        <option value="year_asc">Año ↑</option>
        <option value="citations_desc">Citas ↓</option>
        <option value="citations_asc">Citas ↑</option>
        <option value="title_asc">Título A–Z</option>
      </select>
    </div>
  </div>

  <!-- Estado -->
  {#if loading}
    <div class="text-center py-8 opacity-80">Cargando…</div>
  {:else if errorMsg}
    <div class="alert alert-error">{errorMsg}</div>
  {:else if items.length === 0}
    <div class="text-center py-8 opacity-70">Sin resultados.</div>
  {:else}
    <!-- Lista -->
    <ol class="space-y-3">
      {#each items as it, i}
        <li class="card bg-base-100 border border-base-300 shadow-sm">
          <div class="card-body p-4">
            <!-- Línea 1: “03. Título” -->
            <h3 class="font-semibold text-lg">
              {String((page - 1) * limit + i + 1).padStart(2, '0')}. {it.title}
            </h3>

            <!-- Línea 2: “Año: | Citas: | Venue:” -->
            <p class="text-sm opacity-80">
              Año: {it.year ?? '—'}
              {" | "}
              Citas: {it.citations ?? 0}
              {" | "}
              Venue: {it.venue ?? '—'}
            </p>

            <!-- Acciones -->
            <div class="mt-2 flex flex-wrap gap-2">
              {#if it.url}
                <a class="btn btn-sm" href={it.url} target="_blank" rel="noopener noreferrer">Ver fuente</a>
              {/if}
              {#if it.doi}
                <a class="btn btn-sm btn-outline" href={'https://doi.org/' + it.doi.replace('https://doi.org/','')} target="_blank" rel="noopener noreferrer">
                  DOI
                </a>
              {/if}
            </div>
          </div>
        </li>
      {/each}
    </ol>

    <!-- Paginación -->
    <div class="mt-6 flex items-center justify-between">
      <div class="text-sm opacity-70">
        Página {page} de {Math.max(1, Math.ceil(total / limit))} — {total} resultados
      </div>
      <div class="join">
        <button class="btn join-item" on:click={goPrev} disabled={page <= 1}>« Anterior</button>
        <button class="btn join-item" on:click={goNext} disabled={page >= Math.max(1, Math.ceil(total / limit))}>Siguiente »</button>
      </div>
    </div>
  {/if}
</div>
