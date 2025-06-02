<script>
  import MandarEmail from "$lib/components/Contactos/MandarEmail.svelte";
  import MapaContacto from "$lib/components/Mapas/MapaContacto.svelte";

  export let agencia = {
    nombre: "Agencia CIDMAR",
    email: "betania.viegas@conocimiento.gob.ar",
    telefono: "Tel. 4558315 Int.104"
  };
</script>

<style>
  h1, h2, h3 {
    color: #ff8c00;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    transition: transform 0.3s ease, color 0.3s ease;
    transform-origin: center;
  }

  h1:hover, h2:hover {
    color: #ffa500;
    transform: scale(1.05);
  }

  .direccion {
    text-align: center;
    color: #f9f9f9;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }

  .ubicacion-aporte-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    padding: 1rem 3%;
    align-items: start;
  }

  .columna {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .titulo-seccion {
    font-size: 1.5rem;
    font-weight: bold;
    color: #ff8c00;
    text-transform: uppercase;
    text-align: center;
    margin: 1.5rem 0 0.5rem 0;
  }

  .contenedor-ajustado {
    width: 100%;
    max-width: 900px;
    display: flex;
    justify-content: center;
  }
  
  .info-texto p {
    text-align: left;
    color: #374151; /* gris oscuro */
  }

  @media (max-width: 768px) {
  .ubicacion-aporte-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .ubicacion-aporte-grid .columna:nth-child(1) {
    order: 1; /* Ubicación */
  }

  .ubicacion-aporte-grid .columna:nth-child(2) {
    order: 2; /* Mandá tu aporte */
  }

  .direccion {
    order: 3; /* Dirección debajo del mapa */
    margin-top: 1rem;
  }

  .contenedor-ajustado {
    width: 100%;
  }
}

</style>

<!-- Título -->
<br>



<!-- Sección de ubicación y formulario -->
<div class="ubicacion-aporte-grid">
  <!-- Columna 1: Ubicación -->
  <div class="columna">
    <h2 class="titulo-seccion">Ubicación</h2>
    <div class="contenedor-ajustado">
      <MapaContacto />
    </div>
    <br>
    <h3 class="direccion">Calle Hudson 54, Comodoro Rivadavia</h3>
  </div>

  <!-- Columna 2: Aporte -->
  <div class="columna">
    <h2 class="titulo-seccion">Mandá tu aporte</h2>
    <div class="contenedor-ajustado">
      <MandarEmail />
    </div>
  </div>
</div>
