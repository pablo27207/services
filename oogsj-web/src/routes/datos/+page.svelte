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

  // Control del modal
  let showModal = false;
  let plataformaSeleccionada = null;

  // Plataformas visibles en el mapa
  const plataformas = [
    {
      nombre: "Mareógrafo Puerto de Comodoro Rivadavia",
      lat: -45.8613,
      lon: -67.4647,
      info: "Mareógrafo en Comodoro Rivadavia para monitoreo del nivel del mar.",
      imagen: "/imagenes/mareografo.jpg"
    },
    {
      nombre: "Boya Comodoro II",
      lat: -45.876267,
      lon: -67.448823,
      info: "Boya oceanográfica que mide la temperatura y altura de olas.",
      imagen: "/imagenes/boya.jpg"
    },
    {
      nombre: "Estacion Meteorologica Puerto Comodoro Rivadavia",
      lat: -45.8620,
      lon: -67.4639,
      info: "Estación meteorológica en Puerto Comodoro Rivadavia.",
      imagen: "/imagenes/Estacion-Metereologica-Puerto/EstacionMetereologica.jpg",
      sensores: [
        {
          nombre: "Sensor 1",
          tipo: "Nivel del mar",
          imagen: "/imagenes/Sensores/mareografo.jpg",
          descripcion: "Mide el nivel del mar en tiempo real."
        }
      ]
    },
    {
      nombre: "Estacion Meteorologica Caleta Cordoba",
      lat: -45.749312,
      lon: -67.368301,
      info: "Estación meteorológica en Caleta Córdova.",
      imagen: "/imagenes/Estacion-Metereologica-Puerto/EstacionMetereologica.jpg",
      sensores: [
        {
          nombre: "Sensor 1",
          tipo: "Nivel del mar",
          imagen: "/imagenes/Sensores/mareografo.jpg",
          descripcion: "Mide el nivel del mar en tiempo real."
        }
      ]
    }
  ];

  // Íconos por tipo de plataforma
  const ICONS = {
    boya: "/icons/boya.png",
    estacion: "/icons/estacion.png",
    mareografo: "/icons/mareografo.png"
  };

  // Detecta qué tipo de plataforma es según su nombre
  function getPlatformType(plataforma) {
    const n = plataforma.nombre.toLowerCase();

    if (n.includes("boya")) return "boya";
    if (n.includes("mareógrafo") || n.includes("mareografo")) return "mareografo";
    if (n.includes("estacion")) return "estacion";

    return "estacion";
  }

  // Acción para cerrar el modal al hacer click fuera
  function clickOutside(node) {
    const handleClick = (event) => {
      if (!node.contains(event.target)) {
        closeModal();
      }
    };

    document.addEventListener('mousedown', handleClick, true);

    return {
      destroy() {
        document.removeEventListener('mousedown', handleClick, true);
      }
    };
  }

  // Abre el modal con la plataforma clickeada
  function openModal(plataforma) {
    plataformaSeleccionada = plataforma;
    showModal = true;
  }

  // Cierra el modal y limpia selección
  function closeModal() {
    showModal = false;
    plataformaSeleccionada = null;
  }

  // Agrega marcadores al mapa
  function addMarkers() {
    if (!map) return;

    // Limpiar marcadores previos
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    plataformas.forEach((plataforma) => {
      const type = getPlatformType(plataforma);
      const iconUrl = ICONS[type] ?? ICONS.estacion;

      const size = 44;

      const customIcon = L.icon({
        iconUrl,
        iconSize: [size, size],
        iconAnchor: [size / 2, size / 2],
        tooltipAnchor: [0, -size / 2]
      });

      const marker = L.marker([plataforma.lat, plataforma.lon], { icon: customIcon }).addTo(map);

      marker.bindTooltip(plataforma.nombre, {
        permanent: false,
        direction: "top"
      });

      marker.on('click', () => openModal(plataforma));
    });
  }

  // Handler estable para resize
  const handleResize = () => {
    if (map) map.invalidateSize();
  };

  onMount(() => {
    if (typeof window === 'undefined') return;

    // Inicialización del mapa
    map = L.map(mapElement).setView([plataformas[0].lat, plataformas[0].lon], 14);

    // Capa base IGN por TMS
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

      if (map?.hasLayer(ignLayer)) {
        map.removeLayer(ignLayer);
      }

      const esriLayer = L.tileLayer(
        'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        {
          attribution: '© Esri, Maxar, Earthstar Geographics'
        }
      );

      esriLayer.addTo(map);
    });

    ignLayer.addTo(map);
    addMarkers();

    window.addEventListener('resize', handleResize);
  });

  onDestroy(() => {
    window.removeEventListener('resize', handleResize);

    if (map) {
      map.remove();
    }
  });
</script>

<div class="map-wrapper">
  <div id="map" bind:this={mapElement}></div>

  {#if showModal && plataformaSeleccionada}
    <div class="modal-container" use:clickOutside>
      <div class="modal-body">
        <!--
          Este bloque queda por compatibilidad si alguna plataforma
          en el futuro trae variables renderizables directamente.
        -->
        {#if plataformaSeleccionada.variables}
          <div class="grid-container">
            {#each plataformaSeleccionada.variables as variable}
              <div class="chart-card" data-title={variable.icono + " " + variable.nombre}>
                <div class="chart-container"></div>
              </div>
            {/each}
          </div>
        {/if}

        <!-- Selección del componente visual según la plataforma -->
        {#if plataformaSeleccionada.nombre.toLowerCase().includes("mareógrafo") || plataformaSeleccionada.nombre.toLowerCase().includes("mareografo")}
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
        <button type="button" on:click={closeModal} aria-label="Cerrar modal">❌</button>
      </div>
    </div>
  {/if}
</div>

<style>
  /* =========================================================
     MAPA
     ========================================================= */
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

  /* =========================================================
     MODAL
     ========================================================= */
  .modal-container {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    background: white;
    color: black;
    padding: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    align-items: stretch;
    border-radius: 12px;

    z-index: 999;

    width: min(92vw, 1200px);
    height: min(85dvh, 700px);
    max-height: 85dvh;

    /*
      IMPORTANTE:
      Dejamos visible el contorno del modal para no generar
      problemas innecesarios con elementos flotantes internos.
    */
    overflow: visible;
  }

  .modal-body {
    /*
      El scroll vive acá.
      Esto permite recorrer contenido largo sin que el modal
      entero se desarme.
    */
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0;
    flex: 1;
    position: relative;
    padding-right: 4px;
  }

  /* =========================================================
     BOTÓN DE CIERRE
     ========================================================= */
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
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .modal-footer button:hover {
    background: #a39997;
  }

  /* =========================================================
     BLOQUES GENÉRICOS DE GRILLA
     ========================================================= */
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .chart-card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1rem;
    box-sizing: border-box;
  }

  .chart-container {
    width: 100%;
  }

  /* =========================================================
     RESPONSIVE
     ========================================================= */
  @media (max-width: 700px) {
    .modal-container {
      width: 94vw;
      height: 88dvh;
      border-radius: 14px;
      padding: 10px;
    }

    .modal-body {
      padding-right: 2px;
    }

    .modal-footer {
      top: 8px;
      right: 8px;
    }

    .modal-footer button {
      padding: 7px 9px;
    }
  }

  @media (max-width: 480px) {
    .modal-container {
      width: 96vw;
      height: 90dvh;
      border-radius: 12px;
      padding: 8px;
    }
  }
</style>