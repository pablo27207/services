<script>
  let suggestion = '';
  let nombre = '';
  let email = '';
  let entidad = '';
  let exito = false;
  let error = false;
  let errorMensaje = '';
  let cargando = false;

  let errores = {
    nombre: false,
    email: false,
    entidad: false,
    suggestion: false
  };

  function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  async function enviarSugerencia() {
    error = false;
    exito = false;
    cargando = true;
    errorMensaje = '';
    errores = { nombre: false, email: false, entidad: false, suggestion: false };

    if (!nombre) errores.nombre = true;
    if (!email || !validarEmail(email)) errores.email = true;
    if (!entidad) errores.entidad = true;
    if (!suggestion) errores.suggestion = true;

    if (Object.values(errores).some(v => v)) {
      error = true;
      errorMensaje = 'Por favor completá todos los campos correctamente.';
      cargando = false;
      return;
    }

    try {
      const res = await fetch('/api/send-suggestion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: suggestion, nombre, email, entidad })
      });

      const data = await res.json();

      if (data.status === 'success') {
        exito = true;
        suggestion = '';
        nombre = '';
        email = '';
        entidad = '';
      } else {
        error = true;
        errorMensaje = data.message || 'Error inesperado al enviar.';
      }
    } catch (e) {
      error = true;
      errorMensaje = 'No se pudo enviar la sugerencia. Intenta nuevamente.';
    } finally {
      cargando = false;
    }
  }
</script>



<div class="w-full max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md border border-gray-200 space-y-4">


  <h2 class="text-2xl font-semibold text-center text-gray-800">Enviar sugerencia</h2>

  <!-- Nombre -->
<input 
type="text"
bind:value={nombre}
class="w-full p-3 text-base text-gray-800 border rounded-lg focus:outline-none focus:ring-2 
         {errores.nombre ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
placeholder="Nombre y apellido"
/>
{#if errores.nombre}
<p class="text-red-500 text-base min-h-[1 rem]">Este campo es obligatorio</p>
{:else}
<p class="min-h-[1 rem] text-base"></p>
{/if}

<input 
  type="email"
  bind:value={email}
  class="w-full p-3 text-base text-gray-800 border rounded-lg focus:outline-none focus:ring-2 
         {errores.email ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
  placeholder="Correo electrónico"
/>
{#if errores.email}
  <p class="text-sm text-red-500">
    {#if email === ''}Este campo es obligatorio{:else}El correo no es válido{/if}
  </p>
  {:else}
  <p class="min-h-[1 rem] text-base"></p>
  {/if}

<input 
  type="text"
  bind:value={entidad}
  class="w-full p-3 text-base text-gray-800 border rounded-lg focus:outline-none focus:ring-2 
         {errores.entidad ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
  placeholder="Entidad donde trabaja"
/>
{#if errores.entidad}
  <p class="text-sm text-red-500">Este campo es obligatorio</p>
  {:else}
  <p class="min-h-[1 rem] text-base"></p>
  {/if}
<textarea 
  bind:value={suggestion} 
  rows="4" 
  class="w-full p-3 text-base text-gray-800 border rounded-lg focus:outline-none focus:ring-2 
         {errores.nombre ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}"
  placeholder="Escribe tu sugerencia aquí..."
></textarea>
{#if errores.suggestion}
  <p class="text-sm text-red-500">Este campo es obligatorio</p>
  {:else}
  <p class="min-h-[1 rem] text-base"></p>
  {/if}

  <button 
    on:click={enviarSugerencia}
    class="w-full py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition duration-300"
    disabled={cargando}
  >
    {#if cargando}
      Enviando...
    {:else}
      Enviar sugerencia
    {/if}
  </button>

  {#if exito}
    <p class="text-green-600 text-center">✅ Sugerencia enviada con éxito.</p>
  {/if}

  {#if error}
    <p class="text-red-600 text-center">❌ Ocurrió un error al enviar la sugerencia.</p>
  {/if}
</div>
