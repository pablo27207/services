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

  type DocItem = {
    title: string;
    year: number | null;
    venue: string | null;
    citations: number;
    url: string | null;
    doi: string | null;
  };

  let items: DocItem[] = [];

  // --- Config ---
  const endpointBase = '/api/library';

  // --- Helpers ---
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
      console.error(e);
      errorMsg = 'No pude cargar los documentos. Probá de nuevo.';
    } finally {
      loading = false;
    }
  }

  // Debounce del buscador
  let t: ReturnType<typeof setTimeout> | null = null;
  function onSearchInput(v: string) {
    q = v;
    page = 1;
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
    sort = v as typeof sort;
    page = 1;
    fetchList();
  }

  function doiHref(doi: string | null) {
    if (!doi) return null;
    const clean = doi.replace(/^https?:\/\/doi\.org\//i, '');
    return `https://doi.org/${clean}`;
  }

  onMount(fetchList);
</script>


<style>
  /* Blindaje contra numeraciones o bullets impuestos por CSS globales */
  .no-list {
    list-style: none !important;
    padding-left: 0 !important;
    counter-reset: none !important;
  }
  .no-list > li { counter-increment: none !important; }
  .no-list > li::marker { content: '' !important; }
  .no-list > li::before { content: none !important; }
</style>

<div class="max-w-5xl mx-auto mt-4 px-2 md:px-0">
  <!-- Búsqueda + orden -->
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
      <select
        class="select select-bordered"
        bind:value={sort}
        on:change={(e) => onChangeSort((e.target as HTMLSelectElement).value)}
        disabled={q.trim().length > 0}
        title={q.trim().length > 0 ? 'El orden se fija en modo búsqueda' : 'Cambiar orden'}
      >
        <option value="year_desc">Año ↓ (recientes)</option>
        <option value="year_asc">Año ↑</option>
        <option value="citations_desc">Citas ↓</option>
        <option value="citations_asc">Citas ↑</option>
        <option value="title_asc">Título A–Z</option>
      </select>
    </div>
  </div>

  {#if loading}
    <div class="text-center py-8 opacity-80">Cargando…</div>
  {:else if errorMsg}
    <div class="alert alert-error">{errorMsg}</div>
  {:else if items.length === 0}
    <div class="text-center py-8 opacity-70">Sin resultados.</div>
  {:else}
    <!-- Lista: sin numeración -->
    <ul class="space-y-3 no-list">
      {#each items as it}
        <li class="card bg-base-100 border border-base-300 shadow-sm">
          <div class="card-body p-4">
            <!-- Título -->
            <h3 class="font-semibold text-lg leading-snug">{it.title}</h3>

            <!-- Badges -->
            <div class="mt-1 flex flex-wrap gap-2 text-xs">
              <span class="badge">{it.year ?? '—'}</span>
              <span class="badge badge-ghost">Citas: {it.citations ?? 0}</span>
              {#if it.venue}<span class="badge badge-outline">{it.venue}</span>{/if}
            </div>

            <!-- Acciones -->
            <div class="mt-3 flex flex-wrap gap-2">
              {#if it.url}
                <a class="btn btn-sm" href={it.url} target="_blank" rel="noopener noreferrer">Ver fuente</a>
              {/if}
              {#if it.doi}
                <a class="btn btn-sm btn-outline" href={doiHref(it.doi)} target="_blank" rel="noopener noreferrer">DOI</a>
              {/if}
            </div>
          </div>
        </li>
      {/each}
    </ul>

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
