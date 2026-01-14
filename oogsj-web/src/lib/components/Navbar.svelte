<script>
  import { page } from '$app/stores';
</script>

<style>
  /* Navbar fijo en la parte superior */
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 20; /* Asegura que el navbar esté por encima del contenido */
  }

  /* Deja un espacio debajo del navbar para el contenido */
  .content {
    margin-top: 60px; /* Espacio para que no se superponga el contenido */
  }

  /* Estilo de la imagen de logo */
  .navbar img {
    height: 4rem;
  }
</style>

<!-- Navbar -->
<div class="navbar bg-base-100">
  <div class="navbar-start">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-10 w-10"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
        </svg>
      </div>
      <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
        <li><a href="/" sveltekit:navigate>Inicio</a></li>
        <li><a href="/datos" sveltekit:navigate>Datos</a></li>
        <li><a href="/equipos" sveltekit:navigate>Equipos</a></li>
        <li><a href="/contacto" sveltekit:navigate>Contacto</a></li>
        <li><a href="/biblioteca" sveltekit:navigate>Biblioteca del mar</a></li>
      </ul>
    </div>
  </div>
  <img src="/imagenes/Logotipos/NuevoConocimientoLogo.webp" alt="Logo Observatorio" class="h-16" />
  <img src="/imagenes/Logotipos/logo-puerto-bien.webp" alt="Logo Observatorio" class="h-16" />
 
  <div class="navbar-center">
    <a class="btn btn-ghost text-xl">OBSERVATORIO OCEANOGRÁFICO GOLFO SAN JORGE</a>
  </div>

  <img src="/imagenes/Logotipos/logoiidepis.webp" alt="Logo Observatorio" class="h-16" />
  <img src="/imagenes/Iconos/boya-logo-white.webp" alt="Logo Observatorio" class="h-16" />
   
  

  <div class="navbar-end">
    <button class="btn btn-ghost btn-circle">
      <div class="indicator">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M5.121 19.07A10.97 10.97 0 0112 16c2.7 0 5.18.98 7.121 2.93M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </div>
    </button>
  </div>
</div>

<!-- Espacio debajo del navbar para evitar superposiciones -->
<div class="content"></div>
