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
</style>

<!-- Título -->
<br>

<!-- Contenedor combinado: Contacto + Imagen -->
<!-- <div class="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-center gap-6 p-6 bg-black-200 rounded-lg shadow border" style="border-color: #ff8c00;">-->


  <!-- Contacto de la agencia -->
  <!--<div class="flex-1 flex flex-col items-center text-center space-y-2">
    <h2 class="text-xl font-semibold text-gray-800">Contacto de la Agencia</h2>
    <div class="text-white-800 text-left">
      <p class="mb-2"><strong>Nombre de la agencia:</strong> {agencia.nombre}</p>
      <p class="mb-2"><strong>Correo electrónico:</strong> <a href={`mailto:${agencia.email}`} class="text-blue-600 hover:underline">{agencia.email}</a></p>
      <p><strong>Teléfono:</strong> <a href={`tel:${agencia.telefono}`} class="text-blue-600 hover:underline">{agencia.telefono}</a></p>
    </div>
    
  </div>-->

  <!-- Imagen de la agencia -->
    <!-- <div class="flex-1 flex items-center justify-center">
    <img src="../imagenes/EdificioObservatorioAgencia.jpg" alt="Edificio Agencia CIDMAR" class="rounded-lg shadow-md max-w-full max-h-64 object-cover" />
  </div>
  -->
 <!--</div>-->


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
