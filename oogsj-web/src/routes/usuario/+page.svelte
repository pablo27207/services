<script>
  import Login from '$lib/components/Usuarios/Login.svelte';
  import Usuario from '$lib/components/Usuario.svelte';
  import FormIntermedio from '$lib/components/Usuario/FormIntermedio.svelte';

  // **Estado central de la navegación y datos**
  // Posibles valores: 'login', 'form', 'dashboard'
  let step = 'login'; 
  let userData = {};

  // 1. Maneja el éxito del Login
  const handleLogin = (user) => {
    userData = user;
    step = 'form'; // Avanza al formulario intermedio
    console.log("Login exitoso. Avanzando a Formulario Intermedio.");
  };

  // 2. Maneja el envío del Formulario Intermedio
  const handleFormSubmit = (fullUser) => {
    userData = fullUser;
    step = 'dashboard'; // Avanza al dashboard final
    console.log("Formulario completado. Avanzando a Dashboard.");
  };

  // 3. Maneja el Cierre de Sesión (vuelve al inicio)
  const handleLogout = () => {
    step = 'login';
    userData = {};
    console.log("Sesión cerrada. Volviendo a Login.");
  };
</script>

<div>
  {#if step === 'login'}
    <Login onLoginSuccess={handleLogin} />

  {:else if step === 'form'}
    <FormIntermedio 
      user={userData} 
      onFormSubmit={handleFormSubmit}
    />
    
  {:else if step === 'dashboard'}
    <Usuario 
      user={userData} 
      onLogout={handleLogout} 
    />
  {/if}
</div>