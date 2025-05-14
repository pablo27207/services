<script lang="ts">
  import { plataformaSeleccionada } from '$lib/stores/PlataformaStore';

  import { onDestroy, onMount } from 'svelte';

let plataforma;
let unsubscribe;

onMount(() => {
  unsubscribe = plataformaSeleccionada.subscribe(value => {
    plataforma = value;
  });
});

onDestroy(() => {
  if (unsubscribe) unsubscribe();
});

</script>

<div class="overflow-visible"> <!-- para que los dropdowns no se recorten -->


  {#if plataforma}
    <!-- Encabezado: Imagen + Info -->
    <div class="flex flex-wrap md:flex-nowrap items-center gap-8 mb-8">
      <div class="flex-shrink-0 mx-auto md:ml-16">
        <img 
          src={plataforma.imagen} 
          alt={plataforma.nombre} 
          class="w-40 h-40 object-cover rounded-md shadow-md"
        />
      </div>
      <div class="text-white">
        <h2 class="text-2xl font-bold mb-2">{plataforma.nombre}</h2>
        <p class="text-justify">{plataforma.info}</p>
      </div>
    </div>

    <!-- Título Sensores -->
    <div class="ml-4 md:ml-24 mb-4">
      <h3 class="text-xl font-bold text-orange-400">Sensores</h3>
    </div>

    <!-- Dropdowns de Sensores -->
    <div class="space-y-4 ml-4 md:ml-16">
      {#each plataforma.sensores as sensor}
        <div class="dropdown relative z-100">
          <label tabindex="0" class="btn btn-ghost text-left w-full">
            {sensor.tipo}
          </label>
          <ul
            tabindex="0"
            class="menu dropdown-content absolute z-[9999] p-2 shadow-lg bg-base-100 rounded-box w-60"
          >
            <li>
              <h3 class="font-bold text-orange-400 mb-1">{sensor.tipo}</h3>
              <p class="text-sm text-white ">{sensor.descripcion}</p>
            </li>
          </ul>
        </div>
      {/each}
    </div>
  {:else}
    <p class="text-center text-white">Selecciona una plataforma en el mapa.</p>
  {/if}
</div>

<style>
  h1, h2, h3 {
    color: #ff8c00;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    transition: transform 0.3s ease, color 0.3s ease;
    transform-origin: center;
  }

  h1:hover, h2:hover, h3:hover {
    color: #ffa500;
    transform: scale(1.05);
  }
</style>
