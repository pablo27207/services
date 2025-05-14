<script>
    import { onMount } from "svelte";
    import L from "leaflet"; // Importa Leaflet
  
    let map; // Variable para el mapa
  
    // Función que se ejecutará cuando el componente se monte
    onMount(() => {
      // Verifica si estamos en el navegador (cliente)
      if (typeof window !== "undefined") {
        // Crea el mapa y establece su vista inicial
        map = L.map("map").setView([51.505, -0.09], 13); // Coordenadas por defecto (Londres) y nivel de zoom
  
        // Capa de OpenStreetMap
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }).addTo(map);
      }
    });
  </script>
  
  <!-- Contenedor donde se renderizará el mapa -->
  <div id="map" class="w-full h-96"></div>
  
  <!-- Estilo opcional para asegurar que el mapa ocupe el contenedor -->
  <style>
    #map {
      height: 100%;  /* Asegura que el mapa ocupe todo el contenedor */
      width: 100%;
    }
  </style>
  