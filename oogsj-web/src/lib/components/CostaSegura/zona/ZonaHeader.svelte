<script>
  export let zonaSeleccionada;
</script>

<div class="detalle-imagen">
  <img src={zonaSeleccionada.imagen} alt={zonaSeleccionada.nombre} />
</div>

<style>
  .detalle-imagen img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: 1rem;
    display: block;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.2);
  }

  @media (min-width: 768px) {
    .detalle-imagen img {
      height: 320px;
      border-radius: 1.1rem;
    }
  }

  @media (min-width: 900px) {
    .detalle-imagen img {
      height: 100%;
      min-height: 380px;
      border-radius: 1.25rem;
    }
  }
</style>