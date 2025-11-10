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

  onMount(() => {
    if (typeof window === 'undefined') return;

    map = L.map(mapElement).setView([ubicaciones[0].lat, ubicaciones[0].lon], 14);

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

    // Marcadores + tooltips + selección
    selectPlataforma(ubicaciones[0]);

    ubicaciones.forEach(ubicacion => {
      let emoji = "🟢";
      if (ubicacion.nombre.includes("Futura") || ubicacion.sensores.length === 0) emoji = "🔴";

      const customIcon = L.divIcon({
        className: 'emoji-marker',
        html: `<span style="font-size: 10px;">${emoji}</span>`,
        iconSize: [15, 15],
        iconAnchor: [8, 18]
      });

      const marker = L.marker([ubicacion.lat, ubicacion.lon], { icon: customIcon }).addTo(map);
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


<!--{
  nombre: "Comodoro II",
  lat: -45.876267,
  lon: -67.448823,
  info: "Una boya oceanográfica es un dispositivo flotante que se instala en el mar para recopilar datos importantes sobre el ambiente marino. Aunque a simple vista parezca solo un objeto flotando, en realidad está equipada con sensores que miden cosas como la velocidad del viento, la altura de las olas, la dirección del agua y otros parámetros que ayudan a entender mejor el océano.",
  imagen: "/imagenes/boya-foto-perfil.jpg",
  sensores: [
    { nombre: "Sensor 1", tipo: "Anemómetro", imagen: "/imagenes/Sensores/anemometro-foto.jpg", descripcion: "Mide la velocidad y dirección del viento." },
    { nombre: "Sensor 2", tipo: "Oligrafo", imagen: "/imagenes/Sensores/oligrafo.jpg", descripcion: "Registra datos ambientales como temperatura y presión atmosférica." },
    { nombre: "Sensor 3", tipo: "PAR", imagen: "/imagenes/Sensores/PAR.jpg", descripcion: "Mide la radiación fotosintéticamente activa." },
    { nombre: "Alimentación", tipo: "Paneles Solares", imagen: "/imagenes/Sensores/panelesSolares.png", descripcion: "Usa paneles solares de 12V 30W para generar energía." }
  ]
}-->

