<script>
  export let mensaje = '';
</script>

<div class="banner-mantenimiento">
  <div class="banner-icono">🔧</div>
  <h2>Plataforma en mantenimiento</h2>
  <p class="banner-mensaje">
    {mensaje || 'Esta plataforma se encuentra temporalmente fuera de servicio.'}
  </p>
  <p class="banner-aviso">Los datos no están disponibles en este momento. Disculpe las molestias.</p>
</div>

<style>
  .banner-mantenimiento {
    background: linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%);
    border: 2px solid #f59e0b;
    border-radius: 1rem;
    padding: 2rem 1.5rem;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.18);
  }

  .banner-icono {
    font-size: 3rem;
    line-height: 1;
    margin-bottom: 0.75rem;
  }

  .banner-mantenimiento h2 {
    font-size: 1.4rem;
    font-weight: 700;
    color: #92400e;
    margin: 0 0 0.75rem 0;
  }

  .banner-mensaje {
    font-size: 0.95rem;
    color: #78350f;
    margin: 0 0 0.5rem 0;
    line-height: 1.5;
  }

  .banner-aviso {
    font-size: 0.875rem;
    color: #a16207;
    margin: 0;
    font-style: italic;
  }
</style>
