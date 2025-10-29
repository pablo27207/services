<script>
  import Paper from "$lib/components/Biblioteca/Paper.svelte";
  import Pagina from "$lib/components/Pagina.svelte";
  import Carrusel from "$lib/components/Carrusel.svelte";
  import PaperList from "$lib/components/Biblioteca/PaperList.svelte"
  import Especies from "$lib/components/Biblioteca/Especies.svelte";
  import Noticias from "$lib/components/Biblioteca/Noticias.svelte"; // ← Crear este si no existe
  import EnConstruccion from "$lib/components/EnConstruccion.svelte";
  import PapersExplorer from "$lib/components/Biblioteca/PapersExplorer.svelte";
  let seccionSeleccionada = "especies";




  const papers = [
  {
    titulo: 'Programa de investigación y monitoreo del Golfo San Jorge',
    descripcion: 'Esta publicación surge como una necesidad de comunicar a la sociedad en general el conocimiento existente acerca del ecosistema del Golfo San Jorge, y la importancia de construir, ejecutar y sostener un programa de investigación y monitoreo a largo plazo. ',
    imagen: '/imagenes/papers/GolfoSanJorge.png',
    enlace: 'https://www.pampazul.gob.ar/documentos/Programa-de-investigacion-y-monitoreo-del-Golfo-San-Jorge-Azara.pdf',
    autor: 'Dans, S.L., A.O. Cefarelli., D.E. Galván, M.E. Góngora,, P. Martos y M.A. Varisco (eds.). 2020'
  },
  {
    titulo: 'El Mar Argentino',
    descripcion: '​El documento "El Mar Argentino" de Gabriel Omar Rodríguez ofrece una descripción detallada de las características geográficas, oceanográficas y ecológicas del Mar Argentino, destacando su importancia para la Argentina',
    imagen: '/imagenes/papers/ElMarArgentino.png',
    enlace: 'https://argentinambiental.com/wp-content/uploads/pdf/AA108-64-El_Mar.pdf',
    autor: 'Gabriel Omar Rodríguez'
  },
  {
    titulo: 'Ciencias del mar',
    descripcion: 'El dossier "Ciencia Hoy – Pampa Azul" es una publicación de divulgación científica sobre el Mar Argentino, producida en el marco de la iniciativa Pampa Azul. Presenta artículos sobre biodiversidad marina, cambio climático, tecnología e investigación oceanográfica, destacando la importancia ecológica, económica y estratégica del mar para Argentina, y promoviendo su conservación y uso sostenible.',
    imagen: '/imagenes/papers/CienciaHoy.png',
    enlace: 'https://www.pampazul.gob.ar/documentos/ciencia-hoy-dossier-version-web-simple-pagina.pdf',
    autor: ' La publicación de este volumen es un esfuerzo conjunto de la Asociación Civil CIENCIA HOY y el Ministerio de Ciencia, Tecnología e Innovación Productiva.'
  }
];

    // + más

</script>

<!-- 🎨 Encabezado con carrusel -->

  <!-- Documentos científicos como cards -->
  <section class="bg-[#0f172a] text-white py-12 px-4 ">
    <div class="max-w-4xl mx-auto text-center">
      <div class="bg-base-100 border border-orange-500 rounded-2xl shadow-lg p-6 md:p-10">
        <h1 class="text-3xl md:text-4xl font-bold text-orange-400 mb-4 tracking-wide">
          Biblioteca del Mar
        </h1>
        <p class="text-lg text-white text-justify leading-relaxed">
          En esta sección encontrarás un catálogo de especies marinas del Golfo San Jorge, junto con noticias y novedades sobre el Observatorio Oceanográfico. 
          Próximamente, también estará disponible el acceso a documentos científicos de interés para la región.
        </p>
      </div>
    </div>
  </section>
  

<!-- 🎛️ Selector de sección -->
<div class="text-center mt-6">
  <label class="text-lg font-semibold text-gray-200 mr-4"></label>
  <div class="flex justify-center gap-8">

    <!-- Catálogo de especies -->
    <label class="cursor-pointer flex flex-col items-center">
      <div
        class={`w-6 h-6 rounded-full border-2 ${
          seccionSeleccionada === "especies" ? "bg-white border-white" : "border-blue-400"
        }`}
      >
        <input
          type="radio"
          name="radio-4"
          value="especies"
          bind:group={seccionSeleccionada}
          class="opacity-0 w-full h-full cursor-pointer"
        />
      </div>
      <span
        class={`mt-1 text-sm ${
          seccionSeleccionada === "especies" ? "text-white font-bold" : "text-gray-400"
        }`}
      >
        Catálogo de especies
      </span>
    </label>

    <!-- Noticias y novedades -->
    <label class="cursor-pointer flex flex-col items-center">
      <div
        class={`w-6 h-6 rounded-full border-2 ${
          seccionSeleccionada === "noticias" ? "bg-white border-white" : "border-blue-400"
        }`}
      >
        <input
          type="radio"
          name="radio-4"
          value="noticias"
          bind:group={seccionSeleccionada}
          class="opacity-0 w-full h-full cursor-pointer"
        />
      </div>
      <span
        class={`mt-1 text-sm ${
          seccionSeleccionada === "noticias" ? "text-white font-bold" : "text-gray-400"
        }`}
      >
        Noticias y novedades
      </span>
    </label>


    <!-- Documento científico -->
    <label class="cursor-pointer flex flex-col items-center">
      <div
        class={`w-6 h-6 rounded-full border-2 ${
          seccionSeleccionada === "documento" ? "bg-white border-white" : "border-blue-400"
        }`}
      >
        <input
          type="radio"
          name="radio-4"
          value="documento"
          bind:group={seccionSeleccionada}
          class="opacity-0 w-full h-full cursor-pointer"
        />
      </div>
      <span
        class={`mt-1 text-sm ${
          seccionSeleccionada === "documento" ? "text-white font-bold" : "text-gray-400"
        }`}
      >
        Documento científicos
      </span>
    </label>


    
  </div>
</div>

<!-- 🔁 Contenido dinámico -->
 
<section class="mt-10 px-4 ">
  {#if seccionSeleccionada === "especies"}
    <div class="max-w-5xl mx-auto">
      <Especies />
    </div>

  {:else if seccionSeleccionada === "documento"}
    <PapersExplorer />

  {:else if seccionSeleccionada === "noticias"}
    <div class="max-w-4xl mx-auto">
      <Noticias />
    </div>
  {/if}
</section>

<br>

 📄<!-- Pie de página -->
<!--<Pagina class="mt-20" />-->
