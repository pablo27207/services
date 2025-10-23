<script>
  // Propiedad que se pasa desde App.svelte para manejar el éxito del login
  export let onLoginSuccess; 

  let username = '';
  let password = '';
  let error = '';

  const handleSubmit = () => {
    // Lógica de validación hardcodeada
    if (username === 'franky' && password === '123') {
      error = '';
      // Llama a la función del componente padre para indicar que el login fue exitoso
      onLoginSuccess({ name: 'Franky Smith', email: 'franky@example.com' });
    } else {
      error = 'Usuario o contraseña incorrectos. Usa "franky" / "123"';
    }
  };
</script>

<div class="login-container">
  <h2>Iniciar Sesión</h2>
  <form on:submit|preventDefault={handleSubmit}>
    <input 
      type="text" 
      bind:value={username} 
      placeholder="Usuario (franky)"
      required
    />
    <input 
      type="password" 
      bind:value={password} 
      placeholder="Contraseña (123)"
      required
    />
    <button type="submit">Entrar</button>
  </form>
  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>

<style>
  .login-container {
    max-width: 300px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    text-align: center;
  }
  input, button {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    box-sizing: border-box;
  }
  .error {
    color: red;
  }
</style>