<script>
    import Paper from './Paper.svelte';
  
    export let papers = [];
  
    let search = '';
    let currentPage = 1;
    const perPage = 6;
  
    $: filtered = papers.filter(p =>
      p.titulo.toLowerCase().includes(search.toLowerCase()) ||
      p.descripcion.toLowerCase().includes(search.toLowerCase())
    );
  
    $: totalPages = Math.ceil(filtered.length / perPage);
    $: paginated = filtered.slice((currentPage - 1) * perPage, currentPage * perPage);
  
    function goToPage(page) {
      if (page >= 1 && page <= totalPages) currentPage = page;
    }
  </script>
  
  <!-- 🔍 Buscador -->
  <div class="max-w-3xl mx-auto mt-6">
    <input
      type="text"
      placeholder="Buscar por título o descripción..."
      bind:value={search}
      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring"
    />
  </div>
  
  <!-- 📄 Lista de papers -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6 max-w-6xl mx-auto">
    {#each paginated as paper}
      <Paper {...paper} />
    {/each}
  </div>
  
  <!-- 📑 Paginación -->
  <div class="flex justify-center mt-6 gap-2">
    <button on:click={() => goToPage(currentPage - 1)} disabled={currentPage === 1}
      class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">◀</button>
  
    {#each Array(totalPages) as _, i}
      <button on:click={() => goToPage(i + 1)}
        class="px-3 py-1 rounded 
        {currentPage === i + 1 ? 'bg-blue-500 text-white' : 'bg-gray-100 hover:bg-gray-300'}">
        {i + 1}
      </button>
    {/each}
  
    <button on:click={() => goToPage(currentPage + 1)} disabled={currentPage === totalPages}
      class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">▶</button>
  </div>
  