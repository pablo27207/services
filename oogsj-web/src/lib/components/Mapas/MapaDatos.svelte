<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let map: L.Map | undefined;
  let mapElement: HTMLDivElement;

  // Coordenadas
  const coordenadasHudson = { lat: -45.8299047, lon: -67.4666491 };
  const coordenadasBoyaComII = { lat: -45.876267, lon: -67.448823 };

  // Tamaño dinámico de íconos
  function getIconSize() {
    const width = window.innerWidth;
    if (width < 600) return [10, 10];     // Móviles
    else if (width < 1024) return [15, 15]; // Tablets
    else return [20, 20];                 // Pantallas grandes
  }

  // Actualiza íconos al cambiar tamaño
  function updateIcons(L: any) {
    if (!map) return;

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

    // Limpia marcadores viejos
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) map.removeLayer(layer);
    });

    // Boya Comodoro II
    L.marker([coordenadasBoyaComII.lat, coordenadasBoyaComII.lon], { icon: customIconBoya })
      .addTo(map)
      .bindPopup('<b>Comodoro II</b>');

    // Hudson 54
    L.marker([coordenadasHudson.lat, coordenadasHudson.lon], { icon: customIconLugar })
      .addTo(map)
      .bindPopup('<b>Hudson 54</b>');
  }

  let resizeHandler: (() => void) | null = null;

  onMount(async () => {
    if (typeof window !== 'undefined') {
      const L = await import('leaflet');
      import('leaflet/dist/leaflet.css');

      // Inicializar mapa
      map = L.map(mapElement).setView([coordenadasHudson.lat, coordenadasHudson.lon], 8);

      // Capa base del IGN (TMS en lugar de WMS)
      const ignLayer = L.tileLayer(
        'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/' +
        'capabaseargenmap@EPSG:3857@png/{z}/{x}/{-y}.png',
        {
          tms: true,
          attribution: '© IGN Argentina',
          maxZoom: 18,
        }
      );

      // Fallback a Esri si falla el IGN
      ignLayer.on('tileerror', () => {
        console.warn('No se pudo cargar la capa del IGN, cambiando a Esri.');
        map?.removeLayer(ignLayer);

        const esriLayer = L.tileLayer(
          'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
          { attribution: '© Esri, Maxar, Earthstar Geographics' }
        );

        esriLayer.addTo(map!);
      });

      ignLayer.addTo(map);

      // Cargar íconos iniciales
      updateIcons(L);

      // Manejar cambio de tamaño
      resizeHandler = () => updateIcons(L);
      window.addEventListener('resize', resizeHandler);
    }
  });

  onDestroy(() => {
    if (resizeHandler) window.removeEventListener('resize', resizeHandler);
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

<div
  class="bg-base-100 w-full max-w-4xl shadow-xl flex flex-row items-center"
  bind:this={mapElement}
></div>
