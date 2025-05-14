<script>
    export let title;
    export let text;
    export let img;
    export let reverse = false;
  </script>
  
  <div class="flex flex-col md:flex-row items-center justify-center gap-8 my-12 px-6 md:px-20"
       class:md:flex-row-reverse={reverse}>
    <!-- Imagen -->
    <img src={img} alt={title}
         class="w-full md:w-1/2 h-64 object-cover rounded-xl shadow-md" />
  
    <!-- Texto -->
    <div class="text-white md:w-1/2 text-center md:text-left">
      <h2 class="text-2xl font-bold mb-4 text-orange-400">{title}</h2>
      <p class="text-base leading-relaxed">{text}</p>
    </div>
  </div>
  