<script>
  let noticias = [
    {
      titulo: "Un buque científico búlgaro visitó el puerto de Comodoro en su viaje a la Antártida",
      fecha: "Febrero 16, 2025",
      resumen: "Una embarcación búlgara llegó a Comodoro rumbo a la Antártida para una misión científica. Fue recibida por autoridades locales y de Bulgaria, quienes destacaron la importancia de la cooperación, la cultura búlgara en la ciudad y el valor del mar y la Antártida como espacios de paz e investigación.",
      fuente: "Agencia Comodoro Conocimiento",
      url: "https://conocimiento.gob.ar/index.php/noticias/un-buque-cientifico-bulgaro-visito-el-puerto-de-comodoro-en-su-viaje-a-la-antartida-2"
    },
    {
      titulo: "Comodoro Conocimiento impulsa la certificación profesional en los puertos",
      fecha: "Enero 26, 2025",
      resumen: "Agencia Comodoro Conocimiento, CGT y SUPA impulsan capacitaciones portuarias con certificación, ampliadas a Madryn, Rawson y Camarones, para fortalecer empleo y competitividad regional.",
      fuente: "Agencia Comodoro Conocimiento",
      url: "https://conocimiento.gob.ar/index.php/noticias/comodoro-conocimiento-impulsa-la-certificacion-profesional-en-los-puertos"
    },


    {
      titulo: "Fue instalada la boya oceanográfica en las aguas del Golfo San Jorge",
      fecha: "Enero 21, 2025",
      resumen: "Se puso en funcionamiento la boya oceanográfica Comodoro II, ubicada a 4 km de la costa en el Golfo San Jorge. El operativo de traslado e instalación fue realizado por el Municipio, Comodoro Conocimiento, el Puerto local, la Universidad y el CONICET. Esta boya transmitirá datos por al menos cinco meses y marca un hito en el desarrollo del Observatorio Oceanográfico. Permitirá obtener información clave para la navegación, obras costeras y políticas de sustentabilidad relacionadas con pesca y energía mareomotriz. El operativo incluyó buzos, embarcaciones de apoyo y un anclaje de 11 toneladas.",
      fuente: "Agencia Comodoro Conocimiento",
      url: "https://conocimiento.gob.ar/index.php/noticias/fue-instalada-la-boya-oceanografica-en-las-aguas-del-golfo-san-jorge"
    },
    {
      titulo: "Comodoro Conocimiento realizó una prueba de funcionamiento de la boya oceanográfica en el Puerto local",
      fecha: "Enero 06, 2025",
      resumen: "En el marco del Programa CID MAR AUSTRAL, se realizó con éxito la botadura de una boya oceanográfica recuperada tras 10 años. La maniobra, liderada por el Observatorio Oceanográfico del Golfo San Jorge junto a Comodoro Conocimiento, CONICET y la UNPSJB, marca un paso clave para el monitoreo marino. Actualmente se encuentra en pruebas en el Puerto de Comodoro, equipada con sensores nacionales para medir corrientes, olas, temperatura, viento y radiación. Luego será instalada en su ubicación definitiva. Este avance fortalecerá la investigación oceanográfica y el monitoreo ambiental en el Atlántico Sur.",
      fuente: "Agencia Comodoro Conocimiento",
      url: "https://conocimiento.gob.ar/index.php/noticias/comodoro-conocimiento-realizo-una-prueba-de-funcionamiento-de-la-boya-oceanografica-en-el-puerto-local"
    },
    {
      titulo: "Comodoro Conocimiento, CONICET y la Administración Portuaria ponen en marcha el Observatorio Oceanográfico del Golfo San Jorge",
      fecha: "Octubre 24, 2024",
      resumen: "Se realizó el segundo encuentro de becarios e investigadores del CONICET del Golfo San Jorge, con la participación de autoridades académicas y públicas. Se firmaron dos convenios clave: uno entre Comodoro Conocimiento y el IIDEPyS-CONICET para avanzar en el Observatorio Oceanográfico del Golfo San Jorge, y otro con la Administración Portuaria para coordinar la logística y mantenimiento de la boya oceanográfica. Se destacó la importancia del monitoreo marino para el desarrollo sostenible. Además, se anunció el 1° Foro del Mar en noviembre, como espacio de debate sobre el uso estratégico del mar.",
      fuente: "Agencia Comodoro Conocimiento",
      url: "https://conocimiento.gob.ar/index.php/noticias/comodoro-conocimiento-conicet-y-la-administracion-portuaria-ponen-en-marcha-el-observatorio-oceanografico-del-golfo-san-jorge"
    },
    {
      titulo: "Un buque científico búlgaro visitó el puerto de Comodoro en su viaje a la Antártida",
      fecha: "Febrero 17, 2024",
      resumen: "Una embarcación científica búlgara en misión hacia la Antártida fue recibida en Comodoro Rivadavia por autoridades locales. La visita destacó los lazos entre Bulgaria y Argentina, el valor de la colectividad búlgara en la ciudad y la importancia del mar y la Antártida como espacios de paz e investigación. Autoridades resaltaron la preservación cultural y el compromiso con el desarrollo sustentable del océano.",
      fuente: "Agencia Comodoro Conocimiento",
      url: "https://conocimiento.gob.ar/index.php/noticias/un-buque-cientifico-bulgaro-visito-el-puerto-de-comodoro-en-su-viaje-a-la-antartida"
    }
  ];

  let pagina = 1;
  const porPagina = 3;

  $: totalPaginas = Math.ceil(noticias.length / porPagina);
  $: noticiasPaginadas = noticias.slice((pagina - 1) * porPagina, pagina * porPagina);

  function cambiarPagina(nuevaPagina) {
    if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas) {
      pagina = nuevaPagina;
    }
  }
</script>

<div class="my-8">
  <h2 class="text-2xl font-bold text-white mb-4">Noticias del Observatorio</h2>

  <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
    {#each noticiasPaginadas as noticia}
      <a href={noticia.url} target="_blank" rel="noopener noreferrer" class="block h-full">
        <div class="bg-base-100 p-4 rounded shadow text-white border border-gray-700 hover:border-orange-400 hover:shadow-lg transition duration-200 flex flex-col justify-between h-full">
          <h3 class="text-lg font-semibold text-orange-400 mb-1">{noticia.titulo}</h3>
          <p class="text-xs text-gray-400 mb-2">{noticia.fecha} | {noticia.fuente}</p>
          <div class="text-sm text-gray-200 bg-gray-800 p-2 rounded overflow-y-auto" style="max-height: 100px;">
            {noticia.resumen}
          </div>
        </div>
      </a>
    {/each}
  </div>

  <!-- Paginación -->
  <div class="flex justify-center mt-6 space-x-2">
    <button on:click={() => cambiarPagina(pagina - 1)} class="px-3 py-1 bg-gray-700 text-white rounded disabled:opacity-50" disabled={pagina === 1}>
      Anterior
    </button>
    {#each Array(totalPaginas) as _, idx}
      <button on:click={() => cambiarPagina(idx + 1)} class="px-3 py-1 rounded border border-gray-600 text-white hover:bg-orange-500 hover:text-black {pagina === idx + 1 ? 'bg-orange-400 text-black' : ''}">
        {idx + 1}
      </button>
    {/each}
    <button on:click={() => cambiarPagina(pagina + 1)} class="px-3 py-1 bg-gray-700 text-white rounded disabled:opacity-50" disabled={pagina === totalPaginas}>
      Siguiente
    </button>
  </div>
</div>
