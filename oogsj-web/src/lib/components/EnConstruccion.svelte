<script>
    export let titulo = "Sección en desarrollo";
    export let mensaje = "Esta área estará disponible próximamente. Estamos trabajando para brindarte acceso a este contenido lo antes posible.";
  </script>
  
  <section class="flex flex-col items-center justify-center text-center py-16 px-4 bg-[#0f172a] rounded-xl border border-dashed border-orange-500 shadow-lg">
    <div class="text-6xl mb-4">🚧</div>
    <h2 class="text-2xl md:text-3xl font-bold text-orange-400 mb-2">{titulo}</h2>
    <p class="text-white max-w-xl text-lg leading-relaxed">{mensaje}</p>
  </section>
  