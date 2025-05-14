<!-- Paper.svelte -->
<script>
  export let titulo;
  export let descripcion;
  export let imagen;
  export let enlace; // URL externa al paper original
  export let autor;  // Opcional, puede mostrar el nombre del dueño del paper
</script>

<div class="bg-sky-900 rounded-2xl text-white shadow-md hover:shadow-lg transition duration-300 flex flex-col h-full">
  <img src={imagen} alt={titulo} class="w-full h-40 object-cover rounded-t-2xl" />
  <div class="p-4 flex flex-col flex-grow">
    <h3 class="text-lg font-semibold mb-2">{titulo}</h3>
    {#if autor}
      <p class="text-xs text-gray-300 mb-1">por {autor}</p>
    {/if}
    <p class="text-sm text-gray-100 mb-4 flex-grow">{descripcion}</p>
    <a
      href={enlace}
      target="_blank"
      rel="noopener noreferrer"
      class="mt-auto inline-block text-center bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition"
    >
      Ver documento
    </a>
  </div>
</div>
