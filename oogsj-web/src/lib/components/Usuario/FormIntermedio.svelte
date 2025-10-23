<script>
  // Función para avanzar al dashboard, pasado desde el padre
  export let onFormSubmit;
  // Información básica del usuario, pasada desde el padre
  export let user;

  let userName = user.name || '';
  let favoriteMessage = '';

  const handleSubmit = () => {
    // Almacenamos el mensaje favorito junto con los datos existentes
    const fullUserData = {
      ...user,
      name: userName, // Permitimos modificar el nombre
      message: favoriteMessage
    };
    // Llamamos a la función del padre para avanzar al dashboard
    onFormSubmit(fullUserData);
  };
</script>

<div class="form-container">
  <h2>Paso Intermedio: Personalización</h2>
  <form on:submit|preventDefault={handleSubmit}>
    <label for="name">Nombre de Usuario:</label>
    <input 
      id="name"
      type="text" 
      bind:value={userName} 
      placeholder="Tu nombre"
      required
    />

    <label for="message">Mensaje Favorito:</label>
    <input 
      id="message"
      type="text" 
      bind:value={favoriteMessage} 
      placeholder="Ej: Amo Svelte"
      required
    />
    
    <button type="submit">Ir al Dashboard</button>
  </form>
</div>

<style>
  .form-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }
  label {
    display: block;
    margin-top: 10px;
    margin-bottom: 5px;
    font-weight: bold;
  }
  input, button {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    box-sizing: border-box;
  }
</style>