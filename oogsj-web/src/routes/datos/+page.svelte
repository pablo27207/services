<script>
  import L from 'leaflet';
  import { onMount, onDestroy } from 'svelte';
  import 'leaflet/dist/leaflet.css';

  import GraficosMareografo from '$lib/components/PlataformaGraficos/GraficosMareografo.svelte';
  import GraficosBoya from '$lib/components/PlataformaGraficos/GraficosBoya.svelte';
  import EstacionCaleta from '$lib/components/PlataformaGraficos/EstacionCaleta.svelte';
  import EstacionPuerto from '$lib/components/PlataformaGraficos/EstacionPuerto.svelte';
  import PlataformaNoHabilitada from '$lib/components/PlataformaGraficos/PlataformaNoHabilitada.svelte';

  let map;
  let mapElement;
  let showModal = false;
  let plataformaSeleccionada = null;

  const plataformas = [
    { nombre: "Mareógrafo Puerto de Comodoro Rivadavia", lat: -45.8613,  lon: -67.4647,  info: "Mareógrafo en Comodoro Rivadavia para monitoreo del nivel del mar.", imagen: "/imagenes/mareografo.jpg" },
    { nombre: "Boya Comodoro II",                         lat: -45.876267, lon: -67.448823, info: "Boya oceanográfica que mide la temperatura y altura de olas.",        imagen: "/imagenes/boya.jpg" },
    { nombre: "Estacion Meteorologica Puerto Comodoro Rivadavia", lat: -45.8620,  lon: -67.4639, info: "Mareógrafo en Comodoro Rivadavia.", imagen: "/imagenes/Estacion-Metereologica-Puerto/EstacionMetereologica.jpg",
      sensores: [{ nombre: "Sensor 1", tipo: "Nivel del mar", imagen: "/imagenes/Sensores/mareografo.jpg", descripcion: "Mide el nivel del mar en tiempo real." }]
    },
    { nombre: "Estacion Meteorologica Caleta Cordoba",    lat: -45.749312, lon: -67.368301, info: "Mareógrafo en Comodoro Rivadavia.", imagen: "/imagenes/Estacion-Metereologica-Puerto/EstacionMetereologica.jpg",
      sensores: [{ nombre: "Sensor 1", tipo: "Nivel del mar", imagen: "/imagenes/Sensores/mareografo.jpg", descripcion: "Mide el nivel del mar en tiempo real." }]
    }
  ];

  // --- clickOutside para cerrar modal ---
  function clickOutside(node) {
    const handleClick = (event) => {
      if (!node.contains(event.target)) showModal = false;
    };
    document.addEventListener('mousedown', handleClick, true);
    return {
      destroy() {
        document.removeEventListener('mousedown', handleClick, true);
      }
    };
  }

  function openModal(plataforma) {
    plataformaSeleccionada = plataforma;
    showModal = true;
    // Nota: más adelante acá vamos a forzar resize/redraw de gráficos si hace falta.
  }

  function closeModal() {
    showModal = false;
  }

function addMarkers() {
  if (!map) return;

  // limpiar marcadores previos
  map.eachLayer(layer => {
    if (layer instanceof L.Marker) map.removeLayer(layer);
  });

  plataformas.forEach(plataforma => {
    let emoji = "📡";
    const nombre = plataforma.nombre.toLowerCase();

    if (nombre.includes("boya")) emoji = "🛟";
    else if (nombre.includes("mareógrafo") || nombre.includes("mareografo")) emoji = "🌊";
    else if (nombre.includes("estacion")) emoji = "📡";

    const customIcon = L.divIcon({
      className: 'emoji-marker',
      html: `<span style="font-size: 26px; line-height: 26px;">${emoji}</span>`,
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });

    const marker = L.marker([plataforma.lat, plataforma.lon], { icon: customIcon }).addTo(map);
    marker.bindTooltip(plataforma.nombre, { permanent: false, direction: "top" });
    marker.on('click', () => openModal(plataforma));
  });
}




  // handler estable para add/remove
  const handleResize = () => {
    if (map) map.invalidateSize();
  };

  onMount(() => {
    if (typeof window === 'undefined') return;

    map = L.map(mapElement).setView([plataformas[0].lat, plataformas[0].lon], 14);

    // === IGN por TMS (evita el "Bloqueado WMS") ===
    const ignLayer = L.tileLayer(
      'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/' +
      'capabaseargenmap@EPSG:3857@png/{z}/{x}/{-y}.png',
      {
        tms: true,
        attribution: '© IGN Argentina',
        maxZoom: 18
      }
    );

    // Fallback a Esri si falla IGN
    ignLayer.on('tileerror', () => {
      console.error("No se pudo cargar la capa del IGN, cambiando a Esri.");
      if (map?.hasLayer(ignLayer)) map.removeLayer(ignLayer);
      const esriLayer = L.tileLayer(
        'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        { attribution: '© Esri, Maxar, Earthstar Geographics' }
      );
      esriLayer.addTo(map);
    });

    ignLayer.addTo(map);

    addMarkers();
    window.addEventListener('resize', handleResize);
  });

  onDestroy(() => {
    window.removeEventListener('resize', handleResize);
    if (map) map.remove();
  });
</script>

<div class="map-wrapper">
  <div id="map" bind:this={mapElement}></div>

  <div class="modal-container {showModal ? '' : 'modal-hidden'}" use:clickOutside>
    {#if plataformaSeleccionada}
      <div class="modal-body">
        <!-- Nota: este bloque de variables depende de que exista plataformaSeleccionada.variables -->
        {#if plataformaSeleccionada.variables}
          <div class="grid-container">
            {#each plataformaSeleccionada.variables as variable}
              <div class="chart-card" data-title={variable.icono + " " + variable.nombre}>
                <div class="chart-container"></div>
              </div>
            {/each}
          </div>
        {/if}

        {#if plataformaSeleccionada.nombre.toLowerCase().includes("mareógrafo")}
          <GraficosMareografo />
        {:else if plataformaSeleccionada.nombre.toLowerCase().includes("boya")}
          <GraficosBoya />
        {:else if plataformaSeleccionada.nombre.toLowerCase().includes("caleta")}
          <EstacionCaleta />
        {:else if plataformaSeleccionada.nombre.toLowerCase().includes("puerto")}
          <EstacionPuerto />
        {:else}
          <PlataformaNoHabilitada />
        {/if}
      </div>

      <div class="modal-footer">
        <button on:click={closeModal}>❌</button>
      </div>
    {/if}
  </div>
</div>

<style>
  /* ===== MAPA FULL WIDTH/HEIGHT ===== */
  .map-wrapper {
    position: relative;
    width: 100vw;
    max-width: none;
    height: calc(100vh - 70px);
    margin: 0;
    z-index: 0;
  }

  #map {
    width: 100%;
    height: 100%;
    margin: 0;
    z-index: 0;
  }

  /* ===== MODAL RESPONSIVO ===== */
  .modal-container {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    background: white;
    color: black;
    padding: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,.3);
    display: flex;
    flex-direction: column;
    align-items: stretch;
    border-radius: 12px;

    z-index: 999;

    width: min(92vw, 1200px);
    height: min(85dvh, 700px);
    max-height: 85dvh;
    overflow: hidden;
  }

  .modal-hidden {
    opacity: 0;
    pointer-events: none;
  }

  .modal-body {
    overflow: auto;
    min-height: 0;
    flex: 1;
  }

  /* Botón cerrar: arriba, accesible */
  .modal-footer {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1000;
    background: transparent;
    padding: 0;
  }

  .modal-footer button {
    width: auto;
    margin: 0;
    padding: 8px 10px;
    border-radius: 999px;
    border: none;
    cursor: pointer;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,.2);
  }

  .modal-footer button:hover {
    background: #a39997;
  }

  @media (max-width: 700px) {
    .modal-container {
      width: 94vw;
      height: 88dvh;
      border-radius: 14px;
      padding: 10px;
    }
  }
  :global(html, body) {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

</style>
