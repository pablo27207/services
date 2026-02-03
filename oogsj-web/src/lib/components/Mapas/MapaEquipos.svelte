<script lang="ts">
  import L from 'leaflet';
  import { onMount } from 'svelte';
  import 'leaflet/dist/leaflet.css';
  import { plataformaSeleccionada } from '$lib/stores/PlataformaStore';

  let map: any;
  let mapElement: HTMLDivElement;

  const ubicaciones = [
    {
      nombre: "Boya Comodoro-2",
      lat: -45.877486,
      lon: -67.442217,
      info: "La boya oceanográfica CIDMAR-2 está equipada con sensores que permiten medir variables críticas del océano como olas, corrientes y radiación. Su diseño autónomo con paneles solares permite operar durante largos períodos sin intervención humana.",
      imagen: "/imagenes/Despliegue-Boya/imagen2.jpg",
      sensores: [
        { nombre: "Sensor de Altura de Olas", tipo: "Altura de Olas", imagen: "/imagenes/Sensores/altura_olas.png", descripcion: "Mide la altura de las olas en metros." },
        { nombre: "Sensor de Batería", tipo: "Batería", imagen: "/imagenes/Sensores/bateria.png", descripcion: "Mide el voltaje de la batería de la boya." },
        { nombre: "Sensor de Dirección de la Corriente", tipo: "Dirección de la corriente", imagen: "/imagenes/Sensores/corriente_direccion.png", descripcion: "Detecta el ángulo de dirección del flujo marino." },
        { nombre: "Sensor de Dirección de Olas", tipo: "Dirección de Olas", imagen: "/imagenes/Sensores/direccion_olas.png", descripcion: "Detecta el ángulo desde el cual provienen las olas." },
        { nombre: "Sensor de Periodo de Olas", tipo: "Periodo de Olas", imagen: "/imagenes/Sensores/periodo_olas.png", descripcion: "Mide el tiempo entre crestas de olas en segundos." },
        { nombre: "Sensor de Radiación PAR", tipo: "Radiación PAR", imagen: "/imagenes/Sensores/PAR.jpg", descripcion: "Mide la radiación fotosintéticamente activa en micromoles." },
        { nombre: "Sensor de Velocidad de Corriente", tipo: "Velocidad de la corriente", imagen: "/imagenes/Sensores/corriente_velocidad.png", descripcion: "Mide la velocidad del agua en metros por segundo." }
      ]
    },
    {
      nombre: "Estacion Meteorologica Puerto CR",
      lat: -45.862220,
      lon: -67.463340,
      info: "Estación meteorológica instalada en el puerto de Comodoro Rivadavia. Provee datos confiables sobre las condiciones atmosféricas, útiles para operaciones portuarias y monitoreo ambiental.",
      imagen: "/imagenes/Plataformas/Puerto-de-Comodoro-Rivadavia.jpeg",
      sensores: [
        { nombre: "temp_out", tipo: "Temperatura Exterior", imagen: "/imagenes/Sensores/temperatura.png", descripcion: "Mide la temperatura del aire exterior." },
        { nombre: "hum_out", tipo: "Humedad Exterior", imagen: "/imagenes/Sensores/humedad.png", descripcion: "Mide la humedad relativa exterior." },
        { nombre: "wind_speed", tipo: "Velocidad del Viento", imagen: "/imagenes/Sensores/anemometro-foto.jpg", descripcion: "Mide la velocidad instantánea del viento." },
        { nombre: "bar", tipo: "Presión Barométrica", imagen: "/imagenes/Sensores/presion.png", descripcion: "Mide la presión atmosférica en inHg." }
      ]
    },
    {
      nombre: "Estacion Meteorologica Puerto CC",
      lat: -45.749312,
      lon: -67.368301,
      info: "Estación meteorológica instalada en el muelle de Comodoro Rivadavia. Registra parámetros atmosféricos como presión, humedad, temperatura, viento y radiación.",
      imagen: "/imagenes/Plataformas/PuertoCaleta.jpg",
      sensores: [
        { nombre: "abs_press", tipo: "Presión Absoluta", imagen: "/imagenes/Sensores/presion.png", descripcion: "Mide la presión atmosférica absoluta en inHg." },
        { nombre: "hum_out", tipo: "Humedad", imagen: "/imagenes/Sensores/humedad.png", descripcion: "Mide la humedad relativa exterior en porcentaje." },
        { nombre: "temp_out", tipo: "Temperatura", imagen: "/imagenes/Sensores/temperatura.png", descripcion: "Mide la temperatura exterior en grados Fahrenheit." },
        { nombre: "wind_speed_avg", tipo: "Velocidad del viento", imagen: "/imagenes/Sensores/anemometro-foto.jpg", descripcion: "Promedio de la velocidad del viento en mph." }
      ]
    },
    {
      nombre: "Futura Plataforma",
      lat: -45.825157,
      lon: -67.463506,
      info: "Se prevé la instalación de una nueva plataforma en esta ubicación.",
      imagen: "/imagenes/FuturaPlataforma/futuraPlataformaLogo.jpg",
      sensores: []
    },
    {
      nombre: "Mareografo Puerto CC",
      lat: -45.8613,
      lon: -67.4647,
      info: "Estación meteorológica instalada en el muelle de Comodoro Rivadavia. Registra parámetros atmosféricos como presión, humedad, temperatura, viento y radiación.",
      imagen: "/imagenes/Plataformas/Puerto-de-Comodoro-Rivadavia.jpeg",
      sensores: [
        { nombre: "abs_press", tipo: "Altura de ola", imagen: "/imagenes/Sensores/presion.png", descripcion: "Mide altura respecto respecto al nivel del mar." }
      ]
    }
  ];

  function selectPlataforma(ubicacion: any) {
    plataformaSeleccionada.set(ubicacion);
  }

  // 1) Solo “activas” (según tu pedido: boya + estaciones + mareógrafo; sin futuras y con sensores)
  function esPlataformaActiva(u: any) {
    const nombre = (u?.nombre ?? '').toLowerCase();
    const esTipoValido =
      nombre.includes('boya') ||
      nombre.includes('estacion') ||
      nombre.includes('estación') ||
      nombre.includes('mareografo') ||
      nombre.includes('mareógrafo');

    const noEsFutura = !nombre.includes('futura');
    const tieneSensores = Array.isArray(u?.sensores) && u.sensores.length > 0;

    return esTipoValido && noEsFutura && tieneSensores;
  }

  // 2) Ícono por tipo (misma idea que “datos”: iconos de /static/icons => se usan como /icons/...)
  function getIconUrl(u: any): string {
    const nombre = (u?.nombre ?? '').toLowerCase();

    if (nombre.includes('boya')) return '/icons/boya.png';
    if (nombre.includes('mareografo') || nombre.includes('mareógrafo')) return '/icons/mareografo.png';
    if (nombre.includes('estacion') || nombre.includes('estación')) return '/icons/estacion.png';

    // Fallback por si entra algo raro
    return '/icons/plataformas.png';
  }

  function buildIcon(iconUrl: string) {
    // Ajustá tamaños si querés más grandes
    return L.icon({
      iconUrl,
      iconSize: [34, 34],
      iconAnchor: [17, 34],
      tooltipAnchor: [0, -28]
    });
  }

  onMount(() => {
    if (typeof window === 'undefined') return;

    const activas = ubicaciones.filter(esPlataformaActiva);

    // Si por algún motivo no hay activas, evitamos romper y centramos en Comodoro aprox.
    const center = activas.length
      ? [activas[0].lat, activas[0].lon]
      : [-45.86, -67.48];

    map = L.map(mapElement).setView(center as any, 13);

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

    // Fallback a Esri si falla el IGN
    ignLayer.on('tileerror', () => {
      console.error("No se pudo cargar la capa del IGN, cambiando a Esri.");
      if (map?.hasLayer(ignLayer)) map.removeLayer(ignLayer);
      L.tileLayer(
        'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        { attribution: '© Esri, Maxar, Earthstar Geographics' }
      ).addTo(map);
    });

    ignLayer.addTo(map);

    // Selección inicial: primera activa (si existe)
    if (activas.length) selectPlataforma(activas[0]);

    // Marcadores + tooltips + selección (solo activas)
    activas.forEach((ubicacion) => {
      const iconUrl = getIconUrl(ubicacion);
      const icon = buildIcon(iconUrl);

      const marker = L.marker([ubicacion.lat, ubicacion.lon], { icon }).addTo(map);
      marker.bindTooltip(ubicacion.nombre, { permanent: false, direction: "top" });
      marker.on('click', () => selectPlataforma(ubicacion));
    });
  });
</script>

<div bind:this={mapElement} class="map-container"></div>

<style>
  .map-container {
    width: 100%;
    height: 500px;
  }
</style>
