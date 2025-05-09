<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let map: L.Map | undefined;
  let mapElement: HTMLDivElement;

  // Coordenadas
  const coordenadasHudson = { lat: -45.8299047, lon: -67.4666491 };
  const coordenadasBoyaComII = { lat: -45.876267, lon: -67.448823 };

  function getIconSize() {
    const width = window.innerWidth;

    if (width < 600) {
      return [10, 10]; // Pequeño para móviles
    } else if (width < 1024) {
      return [15, 15]; // Mediano para tablets
    } else {
      return [20, 20]; // Normal para pantallas grandes
    }
  }

  function updateIcons(L: any) {
    if (!map) return;

    // Crear los íconos con el nuevo tamaño
    const customIconBoya = L.icon({
      iconUrl: '/imagenes/Iconos/boya-logo-black.png',
      iconSize: getIconSize(),
      iconAnchor: [getIconSize()[0] / 2, getIconSize()[1]],
    });

    const customIconLugar = L.icon({
      iconUrl: '/imagenes/Iconos/map-pin.png',
      iconSize: getIconSize(),
      iconAnchor: [getIconSize()[0] / 2, getIconSize()[1]],
    });

    // Eliminar todos los marcadores antes de agregar los nuevos
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    // Agregar marcador para la boya Comodoro II
    L.marker([coordenadasBoyaComII.lat, coordenadasBoyaComII.lon], { icon: customIconBoya })
      .addTo(map)
      .bindPopup('<b>Comodoro II</b>');

    // Agregar marcador para Hudson 54
    L.marker([coordenadasHudson.lat, coordenadasHudson.lon], { icon: customIconLugar })
      .addTo(map)
      .bindPopup('<b>Hudson 54</b>');
  }

  onMount(async () => {
  if (typeof window !== 'undefined') {
    const L = await import('leaflet');
    import('leaflet/dist/leaflet.css');

    map = L.map(mapElement).setView([coordenadasHudson.lat, coordenadasHudson.lon], 8);

    // Capa del IGN con manejo de error
    const ignLayer = L.tileLayer.wms('https://wms.ign.gob.ar/geoserver/ows?', {
      layers: 'capabaseargenmap',
      format: 'image/png',
      transparent: false,
      attribution: '&copy; <a href="https://www.ign.gob.ar/">IGN Argentina</a>'
    });

    ignLayer.on('tileerror', () => {
      console.warn('No se pudo cargar la capa del IGN, cambiando a Esri.');

      map.removeLayer(ignLayer);

      const esriLayer = L.tileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        {
          attribution: '&copy; Esri, Maxar, Earthstar Geographics'
        }
      );

      esriLayer.addTo(map);
    });

    ignLayer.addTo(map);

    updateIcons(L);

    window.addEventListener('resize', () => updateIcons(L));
  }
});



  onDestroy(() => {
    window.removeEventListener('resize', () => updateIcons(L));
  });
</script>

<style>
  div {
    width: 140%;
    height: 500px;
    border-radius: 5px;
    z-index: 5;
  }
</style>

<div class="bg-base-100 w-full max-w-4xl shadow-xl flex flex-row items-center" bind:this={mapElement}></div>
