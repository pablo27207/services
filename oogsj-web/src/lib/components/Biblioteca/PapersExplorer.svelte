<script lang="ts">
  import { onMount } from 'svelte';

  // --- Estado de búsqueda/filtros/orden ---
  let q = '';
  let sort: 'year_desc' | 'year_asc' | 'citations_desc' | 'citations_asc' | 'title_asc' = 'year_desc';
  let page = 1;
  let limit = 10;

  let hasDoi: boolean | null = null;   // null = no filtrar, true/false filtran
  let hasFile: boolean | null = null;
  let yearMin: number | null = 1950;
  let yearMax: number | null = new Date().getFullYear();

  // --- Estado de datos/UI ---
  let loading = false;
  let errorMsg = '';
  let total = 0;

  type Author = { id: number; full_name: string };
  type DocItem = {
    id: number;
    title: string;
    year: number | null;
    venue: string | null;
    citations: number;
    url: string | null;
    doi: string | null;
    authors: Author[];
    has_local_file: boolean;
  };

  let items: DocItem[] = [];

  // Detalle (modal)
  let selectedId: number | null = null;
  let detailLoading = false;
  let detailError = '';
  let detail: null | (DocItem & {
    download_url?: string | null;
    canonical_id?: number;
    is_duplicate?: boolean;
  }) = null;

  const endpointBase = '/api/library';

  // --- Helpers ---
  function doiHref(doi: string | null) {
    if (!doi) return null;
    const clean = doi.replace(/^https?:\/\/doi\.org\//i, '');
    return `https://doi.org/${clean}`;
  }

  function buildSearchUrl() {
    const u = new URL(location.origin + `${endpointBase}/search`);
    if (q.trim()) u.searchParams.set('q', q.trim());
    if (yearMin != null) u.searchParams.set('year_min', String(yearMin));
    if (yearMax != null) u.searchParams.set('year_max', String(yearMax));
    if (hasDoi != null)  u.searchParams.set('has_doi', hasDoi ? 'true' : 'false');
    if (hasFile != null) u.searchParams.set('has_file', hasFile ? 'true' : 'false');
    u.searchParams.set('page', String(page));
    u.searchParams.set('limit', String(limit));
    // Permitimos sort también en search
    u.searchParams.set('sort', sort);
    return u.toString().replace(location.origin, '');
  }

  function buildListUrl() {
    const u = new URL(location.origin + `${endpointBase}/list`);
    u.searchParams.set('sort', sort);
    u.searchParams.set('page', String(page));
    u.searchParams.set('limit', String(limit));
    return u.toString().replace(location.origin, '');
  }

  function isUsingSearch() {
    return (
      q.trim().length > 0 ||
      hasDoi !== null ||
      hasFile !== null ||
      yearMin !== null ||
      yearMax !== null
    );
  }

  async function fetchList() {
    loading = true;
    errorMsg = '';
    try {
      const url = isUsingSearch() ? buildSearchUrl() : buildListUrl();
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      items = (data.items ?? []) as DocItem[];
      total = data.total ?? 0;
    } catch (e) {
      console.error(e);
      errorMsg = 'No pude cargar los documentos. Probá de nuevo.';
    } finally {
      loading = false;
    }
  }

  // Detalle
  async function openDetail(id: number) {
    selectedId = id;
    detail = null;
    detailError = '';
    detailLoading = true;
    try {
      const res = await fetch(`${endpointBase}/${id}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      // Mapear a estructura compatible con DocItem + extras
      detail = {
        id: data.id,
        title: data.title,
        year: data.year,
        venue: data.venue,
        citations: data.citations ?? 0,
        url: data.url ?? null,
        doi: data.doi ?? null,
        authors: (data.authors ?? []) as Author[],
        has_local_file: Boolean(data.has_local_file),
        download_url: data.download_url ?? null,
        canonical_id: data.canonical_id,
        is_duplicate: data.is_duplicate
      };
    } catch (e) {
      console.error(e);
      detailError = 'No pude cargar el detalle.';
    } finally {
      detailLoading = false;
    }
  }

  function closeDetail() {
    selectedId = null;
    detail = null;
  }

  // Debounce del buscador
  let t: ReturnType<typeof setTimeout> | null = null;
  function onSearchInput(v: string) {
    q = v;
    page = 1;
    if (t) clearTimeout(t);
    t = setTimeout(fetchList, 350);
  }

  function onToggleHasDoi(v: boolean) {
    hasDoi = v ? true : null; // click para activar; otro click en "limpiar" lo pone null
    page = 1;
    fetchList();
  }
  function onToggleHasFile(v: boolean) {
    hasFile = v ? true : null;
    page = 1;
    fetchList();
  }
  function onYearMin(v: string) {
    yearMin = v ? Number(v) : null;
    page = 1;
    fetchList();
  }
  function onYearMax(v: string) {
    yearMax = v ? Number(v) : null;
    page = 1;
    fetchList();
  }

  function clearFilters() {
    hasDoi = null;
    hasFile = null;
    yearMin = null;
    yearMax = null;
    page = 1;
    fetchList();
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

<div class="max-w-6xl mx-auto mt-4 px-2 md:px-0">
  <!-- 🔎 Búsqueda + Filtros + Orden -->
  <div class="grid grid-cols-1 gap-3 md:grid-cols-12 md:items-end mb-4">
    <!-- Buscador -->
    <div class="md:col-span-6">
      <input
        type="search"
        class="input input-bordered w-full"
        placeholder="Buscar por título, venue, DOI, URL o autor…"
        on:input={(e) => onSearchInput((e.target as HTMLInputElement).value)}
        value={q}
      />
    </div>

    <!-- Filtros -->
    <div class="md:col-span-3 flex gap-2">
      <label class="label cursor-pointer gap-2">
        <span class="label-text">Con DOI</span>
        <input type="checkbox" class="checkbox" checked={hasDoi === true} on:change={(e) => onToggleHasDoi((e.target as HTMLInputElement).checked)} />
      </label>
      <label class="label cursor-pointer gap-2">
        <span class="label-text">Con PDF</span>
        <input type="checkbox" class="checkbox" checked={hasFile === true} on:change={(e) => onToggleHasFile((e.target as HTMLInputElement).checked)} />
      </label>
    </div>

    <!-- Rango de años -->
    <div class="md:col-span-2 flex gap-2">
      <input
  type="number"
  class="input input-bordered w-full"
  placeholder="Año mín."
  min="1900"
  max={new Date().getFullYear()}
  bind:value={yearMin}
  on:change={(e)=>onYearMin((e.target as HTMLInputElement).value)}
/>

<input
  type="number"
  class="input input-bordered w-full"
  placeholder="Año máx."
  min="1900"
  max={new Date().getFullYear()}
  bind:value={yearMax}
  on:change={(e)=>onYearMax((e.target as HTMLInputElement).value)}
/>
    </div>

    <!-- Orden -->
    <div class="md:col-span-1">
      <select
        class="select select-bordered w-full"
        bind:value={sort}
        on:change={(e) => onChangeSort((e.target as HTMLSelectElement).value)}
      >
        <option value="year_desc">Año ↓</option>
        <option value="year_asc">Año ↑</option>
        <option value="citations_desc">Citas ↓</option>
        <option value="citations_asc">Citas ↑</option>
        <option value="title_asc">Título A–Z</option>
      </select>
    </div>
  </div>

  <!-- Botón limpiar filtros -->
  <div class="flex gap-2 mb-3">
    <button class="btn btn-ghost btn-sm" on:click={clearFilters} disabled={!isUsingSearch()}>
      Limpiar filtros
    </button>
  </div>

  {#if loading}
    <div class="space-y-3">
      {#each Array(5) as _}
        <div class="card bg-base-100 border border-base-300 shadow-sm">
          <div class="card-body p-4">
            <div class="skeleton h-4 w-3/4"></div>
            <div class="mt-2 flex gap-2">
              <div class="skeleton h-4 w-12"></div>
              <div class="skeleton h-4 w-16"></div>
              <div class="skeleton h-4 w-24"></div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {:else if errorMsg}
    <div class="alert alert-error">{errorMsg}</div>
  {:else if items.length === 0}
    <div class="text-center py-8 opacity-70">Sin resultados.</div>
  {:else}
    <!-- Lista -->
    <ul class="space-y-3 no-list">
      {#each items as it}
        <li class="card bg-base-100 border border-base-300 shadow-sm">
          <div class="card-body p-4">
            <!-- Título -->
            <div class="flex items-start justify-between gap-3">
              <h3 class="font-semibold text-lg leading-snug cursor-pointer hover:underline" on:click={() => openDetail(it.id)}>
                {it.title}
              </h3>
              <!-- Acciones rápidas -->
              <div class="flex gap-2">
                {#if it.has_local_file}
                  <a class="btn btn-sm btn-secondary" href={`/api/library/file/${it.id}`} target="_blank" rel="noopener noreferrer" title="Descargar PDF">
                    Descargar
                  </a>
                {/if}
                {#if it.doi}
                  <a class="btn btn-sm btn-outline" href={doiHref(it.doi)} target="_blank" rel="noopener noreferrer" title="Abrir DOI">
                    DOI
                  </a>
                {/if}
                {#if it.url}
                  <a class="btn btn-sm" href={it.url} target="_blank" rel="noopener noreferrer" title="Ver fuente">
                    Fuente
                  </a>
                {/if}
              </div>
            </div>

            <!-- Badges -->
            <div class="mt-1 flex flex-wrap gap-2 text-xs">
              <span class="badge">{it.year ?? '—'}</span>
              <span class="badge badge-ghost">Citas: {it.citations ?? 0}</span>
              {#if it.venue}<span class="badge badge-outline">{it.venue}</span>{/if}
              {#if it.has_local_file}<span class="badge badge-secondary">PDF</span>{/if}
            </div>

            <!-- Autores (chips) -->
            {#if it.authors?.length}
              <div class="mt-2 flex flex-wrap gap-2">
                {#each it.authors.slice(0, 4) as au, i}
                  <div class="badge badge-outline" title={au.full_name}>{au.full_name}</div>
                {/each}
                {#if it.authors.length > 4}
                  <div class="badge badge-ghost" title={it.authors.map(a=>a.full_name).join(', ')}>
                    +{it.authors.length - 4} más
                  </div>
                {/if}
              </div>
            {/if}
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

  <!-- Modal de detalle -->
  {#if selectedId !== null}
    <div class="modal modal-open">
      <div class="modal-box max-w-3xl">
        <h3 class="font-bold text-lg">Detalle del documento</h3>
        <button class="btn btn-sm btn-circle absolute right-2 top-2" on:click={closeDetail}>✕</button>

        {#if detailLoading}
          <div class="mt-4 space-y-2">
            <div class="skeleton h-5 w-3/4"></div>
            <div class="skeleton h-4 w-1/2"></div>
            <div class="skeleton h-4 w-2/3"></div>
          </div>
        {:else if detailError}
          <div class="alert alert-error mt-4">{detailError}</div>
        {:else if detail}
          <div class="mt-3 space-y-2">
            <h4 class="font-semibold text-xl leading-snug">{detail.title}</h4>
            <div class="flex flex-wrap gap-2 text-sm">
              <span class="badge">{detail.year ?? '—'}</span>
              {#if detail.venue}<span class="badge badge-outline">{detail.venue}</span>{/if}
              <span class="badge badge-ghost">Citas: {detail.citations ?? 0}</span>
            </div>

            {#if detail.doi || detail.url}
              <div class="mt-2 flex flex-wrap gap-2">
                {#if detail.doi}
                  <a class="link" href={doiHref(detail.doi)} target="_blank" rel="noopener noreferrer">DOI</a>
                {/if}
                {#if detail.url}
                  <a class="link" href={detail.url} target="_blank" rel="noopener noreferrer">Fuente</a>
                {/if}
              </div>
            {/if}

            {#if detail.authors?.length}
              <div class="mt-3">
                <div class="text-sm opacity-70 mb-1">Autores</div>
                <div class="flex flex-wrap gap-2">
                  {#each detail.authors as au}
                    <div class="badge" title={au.full_name}>{au.full_name}</div>
                  {/each}
                </div>
              </div>
            {/if}

            <div class="mt-4 flex gap-2">
              {#if detail.has_local_file && detail.download_url}
                <a class="btn btn-secondary" href={detail.download_url} target="_blank" rel="noopener noreferrer">Descargar PDF</a>
              {/if}
              <button class="btn btn-ghost" on:click={closeDetail}>Cerrar</button>
            </div>
          </div>
        {/if}
      </div>
      <div class="modal-backdrop" on:click={closeDetail}></div>
    </div>
  {/if}
</div>
