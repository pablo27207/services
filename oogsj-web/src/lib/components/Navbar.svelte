<!-- src/lib/components/Navbar.svelte -->
<script>
  import { page } from '$app/stores';
  $: pathname = $page.url.pathname;
  const isActive = (href) => pathname === href ? 'active font-semibold' : '';
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
  <!-- START -->
  <div class="navbar-start">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
        </svg>
      </div>

      <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
        <li><a href="/" sveltekit:navigate class={isActive('/')}>Inicio</a></li>
        <li><a href="/datos" sveltekit:navigate class={isActive('/datos')}>Datos</a></li>
        <li><a href="/equipos" sveltekit:navigate class={isActive('/equipos')}>Equipos</a></li>
        <li><a href="/contacto" sveltekit:navigate class={isActive('/contacto')}>Contacto</a></li>
        <li><a href="/biblioteca" sveltekit:navigate class={isActive('/biblioteca')}>Biblioteca del mar</a></li>
      </ul>
    </div>
  </div>

  <!-- LOGO IZQUIERDO -->
  <img src="/imagenes/Logotipos/logo comodoro-conocimiento-oscuro.png" alt="Logo Observatorio" class="h-16" />

  <!-- CENTER -->
  <div class="navbar-center">
    <a href="/" sveltekit:navigate class="btn btn-ghost text-xl">
      OBSERVATORIO OCEANOGRÁFICO GOLFO SAN JORGE
    </a>
  </div>

  <!-- LOGO DERECHO -->
  <img src="/imagenes/Iconos/boya-logo-white.png" alt="Logo Observatorio" class="h-16" />

  <!-- END -->
  <div class="navbar-end">
    <!-- Botón de usuario: lleva a /usuario (tu página en routes/usuario/+page.svelte) -->
    <a href="/usuario" sveltekit:navigate aria-label="Ir a registro / iniciar sesión" class="btn btn-ghost btn-circle">
      <div class="indicator">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M5.121 19.07A10.97 10.97 0 0112 16c2.7 0 5.18.98 7.121 2.93M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </div>
    </a>
  </div>
</div>

<!-- Espacio debajo del navbar para evitar superposiciones -->
<div class="content"></div>
