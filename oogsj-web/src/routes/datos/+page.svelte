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
    {
      nombre: "Mareógrafo Puerto de Comodoro Rivadavia",
      lat: -45.8613,
      lon: -67.4647,
      info: "Mareógrafo en Comodoro Rivadavia para monitoreo del nivel del mar.",
      imagen: "/imagenes/mareografo.jpg",
      
    },
    {
      nombre: "Boya Comodoro II",
      lat: -45.876267,
      lon: -67.448823,
      info: "Boya oceanográfica que mide la temperatura y altura de olas.",
      imagen: "/imagenes/boya.jpg",
    
    },
    {
      nombre: "Estacion Meteorologica Puerto Comodoro Rivadavia",
      lat: -45.8620,
      lon: -67.4639,
      info: "Mareógrafo en Comodoro Rivadavia.",
      imagen: "/imagenes/Estacion-Metereologica-Puerto/EstacionMetereologica.jpg",
      sensores: [
        { nombre: "Sensor 1", tipo: "Nivel del mar", imagen: "/imagenes/Sensores/mareografo.jpg", descripcion: "Mide el nivel del mar en tiempo real." }
      ]
    },
    {
      nombre: "Estacion Meteorologica Caleta Cordoba",
      lat: -45.749312,
      lon: -67.368301,
      info: "Mareógrafo en Comodoro Rivadavia.",
      imagen: "/imagenes/Estacion-Metereologica-Puerto/EstacionMetereologica.jpg",
      sensores: [
        { nombre: "Sensor 1", tipo: "Nivel del mar", imagen: "/imagenes/Sensores/mareografo.jpg", descripcion: "Mide el nivel del mar en tiempo real." }
      ]
    },
    {
      nombre: "Futura Plataforma",
      lat: -45.825157,
      lon: -67.463506,
      info: "Se prevé la instalación de una nueva plataforma en esta ubicación.",
      imagen: "/imagenes/FuturaPlataforma/futuraPlataformaLogo.jpg", // podés usar una imagen diferente o un ícono especial
      sensores: []
    }
  ];

  // Detectar clic fuera del modal
function clickOutside(node) {
  const handleClick = (event) => {
    if (!node.contains(event.target)) {
      showModal = false;
    }
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
  }

  function closeModal() {
    showModal = false;
  }

  function action1() {
    alert("Acción 1 ejecutada");
  }

  function action2() {
    alert("Acción 2 ejecutada");
  }

  function addMarkers() {
  if (!map) return;

  map.eachLayer(layer => {
    if (layer instanceof L.Marker) {
      map.removeLayer(layer);
    }
  });

  plataformas.forEach(plataforma => {
    // 🔁 Lógica para seleccionar emoji por tipo o estado
    let emoji = "🟢"; // activo por defecto

    if (plataforma.nombre.toLowerCase().includes("futura") || (plataforma.sensores?.length === 0)) {
      emoji = "🔴";
    } else if (plataforma.nombre.toLowerCase().includes("mareógrafo")) {
      emoji = "🟢";
    } else if (plataforma.nombre.toLowerCase().includes("Estacion Meteorologica")) {
      emoji = "🟠"; 
    } else if (plataforma.nombre.toLowerCase().includes("boya")) {
      emoji = "🟢";
    } else if (plataforma.nombre.toLowerCase().includes("Estacion Meteorologica caleta") || plataforma.nombre.toLowerCase().includes("puerto")) {
      emoji = "🟠";
    }

    const customIcon = L.divIcon({
      className: 'emoji-marker',
      html: `<span style="font-size: 10px;">${emoji}</span>`,
      iconSize: [15, 15],
      iconAnchor: [8, 8]
    });

    const marker = L.marker([plataforma.lat, plataforma.lon], { icon: customIcon }).addTo(map);
    marker.bindTooltip(plataforma.nombre, { permanent: false, direction: "top" });

    marker.on('click', () => {
      openModal(plataforma);
    });
  });
}


  onMount(() => {
    if (typeof window !== 'undefined') {
      map = L.map(mapElement).setView([plataformas[0].lat, plataformas[0].lon], 14);

      const ignLayer = L.tileLayer.wms('https://wms.ign.gob.ar/geoserver/ows?', {
        layers: 'capabaseargenmap',
        format: 'image/png',
        transparent: false,
        attribution: ''
      });

      const esriLayer = L.tileLayer(
        'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        {
          attribution: ''
        }
      );

      ignLayer.on('tileerror', () => {
        console.error("No se pudo cargar la capa del IGN, cambiando a Esri.");
        if (map?.hasLayer(ignLayer)) {
          map.removeLayer(ignLayer);
        }
        esriLayer.addTo(map);
      });

      ignLayer.addTo(map);
      addMarkers();
      window.addEventListener('resize', addMarkers);
    }
  });

  onDestroy(() => {
    window.removeEventListener('resize', addMarkers);
  });
</script>

<div class="container">
  <div id="map" bind:this={mapElement}></div>

  <div class="modal-container {showModal ? '' : 'modal-hidden'}" use:clickOutside>

    {#if plataformaSeleccionada}   
      <div class="grid-container">
        {#each plataformaSeleccionada.variables as variable}
          <div class="chart-card" data-title={variable.icono + " " + variable.nombre}>
            <div class="chart-container"></div>
          </div>
        {/each}
      </div>
      <!--p style="color: red;">Nombre de la plataforma seleccionada: {plataformaSeleccionada.nombre}</p>-->

      {#if plataformaSeleccionada.nombre.toLowerCase().includes("mareógrafo")}
  <GraficosMareografo />
{:else if plataformaSeleccionada.nombre.toLowerCase().includes("boya")}
  <GraficosBoya />
  {:else if plataformaSeleccionada.nombre.toLowerCase().includes("caleta")}
  <PlataformaNoHabilitada />
{:else if plataformaSeleccionada.nombre.toLowerCase().includes("puerto")}
<PlataformaNoHabilitada />
{:else}
  <PlataformaNoHabilitada />
{/if}


    

      <div class="modal-footer">
        
        <!--<button on:click={action1}>⚙️</button> -->
        <!--<button on:click={action2}>🔍</button> -->
        <button on:click={closeModal}>❌</button>
      </div>
    {/if}
  </div>
</div>

<!-- Estilos optimizados -->
<style>
  .modal-footer {
  position: fixed;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: row;
  gap: 10px;
  background: white;
  padding: 5px;
  z-index: 20;
}


  .container {
    position: relative;
    width: 100%;
    height: calc(100vh - 70px);
    margin-top: 6%;
    z-index: 0;
  }

  #map {
    width: 100%;
    height: 100%;
    z-index: 0;
    margin-left: 3%;
  }

  .modal-container {
    position: absolute;
    top: 2%;
    left: 50%;
    transform: translate(-50%, 0);
    background: white;
    color: black;
    padding: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 8px;
    z-index: 15;
     width: 90vw;
     height: 90%;
    max-width: 1200px;
    max-height: 600px;
    min-width: 700;
    overflow-y: auto;
  }

  .modal-hidden {
    opacity: 0;
    pointer-events: none;
  }

  button {
    background: #fff;
    border: none;
    padding: 10px;
    color: white;
    cursor: pointer;
    border-radius: 10px;
    width: 80%;
    text-align: center;
    margin-left: 20px;
  }

  button:hover {
    background: #a39997;
  }

  @media (max-width: 600px) {
    .modal-container {
      width: 90%;
      top: 5%;
    }
  }




</style>
