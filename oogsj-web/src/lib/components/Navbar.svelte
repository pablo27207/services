<style>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 20;
  }

  .content {
    margin-top: 60px;
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
      <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
      <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[50] mt-3 w-52 p-2 shadow">
        <li><a href="/">Inicio</a></li>
        <li><a href="/datos">Datos</a></li>
        <li><a href="/equipos">Equipos</a></li>
        <li><a href="/contacto">Contacto</a></li>
        <li><a href="/biblioteca">Biblioteca del mar</a></li>
        <li><a href="/costa-segura">Informacion de costa</a></li>
      </ul>
    </div>
  </div>

  <div class="navbar-center">
    <a href="/" class="btn btn-ghost text-xl hidden md:flex">OBSERVATORIO OCEANOGRÁFICO GOLFO SAN JORGE</a>
  </div>

  <div class="navbar-end">
    <div class="hidden md:flex items-center gap-2 mr-2">
      <img src="/imagenes/Logotipos/NuevoConocimientoLogo.webp" alt="Logo Nuevo Conocimiento" class="h-12" />
      <img src="/imagenes/Logotipos/logo-puerto-bien.webp" alt="Logo Puerto Bien" class="h-12" />
      <img src="/imagenes/Logotipos/logoiidepis.webp" alt="Logo IIDEPIS" class="h-12" />
    </div>
    <a href="/login" class="btn btn-ghost btn-circle" aria-label="Panel de administración">
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
