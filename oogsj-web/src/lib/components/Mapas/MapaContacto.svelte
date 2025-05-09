<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let map: L.Map | undefined;
  let mapElement: HTMLDivElement;

  // Coordenadas exactas para Calle Hudson 54, Comodoro Rivadavia
  const coordenadas = { lat: -45.8299047, lon: -67.4666491 };

  function getZoomLevel() {
    const width = window.innerWidth;
    if (width < 600) return 16; // Zoom más cercano en móviles
    if (width < 1024) return 15; // Zoom intermedio en tablets
    return 16; // Zoom más alejado en pantallas grandes
  }

  function getIconSize() {
    const width = window.innerWidth;
    if (width < 600) return 16;
    if (width < 1024) return 24;
    return 32;
  }

  function updateIcon() {
    if (!map) return;

    const customIcon = L.divIcon({
      className: 'emoji-marker',
      html: `<span style="font-size: ${getIconSize()}px;">📍</span>`,
      iconSize: [getIconSize(), getIconSize()],
      iconAnchor: [getIconSize() / 2, getIconSize() / 2]
    });

    map.eachLayer(layer => {
      if (layer instanceof L.Marker) {
        map?.removeLayer(layer);
      }
    });

    L.marker([coordenadas.lat, coordenadas.lon], { icon: customIcon })
      .addTo(map)
      .bindPopup('<b>Observatorio Oceanográfico Golfo San Jorge</b>');
  }

  onMount(async () => {
    if (typeof window !== 'undefined') {
      const L = await import('leaflet');
      import('leaflet/dist/leaflet.css');

      map = L.map(mapElement).setView([coordenadas.lat, coordenadas.lon], getZoomLevel());

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
        map?.removeLayer(ignLayer);
        esriLayer.addTo(map);
      });

      ignLayer.addTo(map);
      updateIcon();

      const bounds = [
        [-47.0, -68.5],
        [-43.0, -65.0]
      ];
      map.setMaxBounds(bounds);
      map.setMaxZoom(16);
      map.setMinZoom(9);

      map.on('drag', function () {
        const currentCenter = map.getCenter();
        if (!bounds[0] || !bounds[1]) return;

        if (currentCenter.lat < bounds[0][0]) {
          map.setView([bounds[0][0], currentCenter.lng]);
        } else if (currentCenter.lat > bounds[1][0]) {
          map.setView([bounds[1][0], currentCenter.lng]);
        }

        if (currentCenter.lng < bounds[0][1]) {
          map.setView([currentCenter.lat, bounds[0][1]]);
        } else if (currentCenter.lng > bounds[1][1]) {
          map.setView([currentCenter.lat, bounds[1][1]]);
        }
      });

      window.addEventListener('resize', () => {
        if (map) map.setZoom(getZoomLevel()); // Cambiar zoom si cambia el tamaño de la pantalla
        updateIcon();
      });
    }
  });

  onDestroy(() => {
    window.removeEventListener('resize', updateIcon);
  });
</script>

<style>
  :global(.leaflet-container) {
  width: 100%;
  height: 400px;
  border-radius: 5px;
  z-index: 5;
}

.emoji-marker {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 30px;
  height: 30px;
}

</style>

<div bind:this={mapElement}></div>
