<script>
  import { onMount } from 'svelte';

  let originalImages = [
    "/imagenes/cola-ballena.jpeg",
    "/imagenes/Pingüinos.jpeg",
    "/imagenes/Península-valdez-chubut.jpeg",
    "/imagenes/Despliegue-Boya/imagen1.jpg",
    "/imagenes/Despliegue-Boya/imagen2.jpg",
    "/imagenes/Despliegue-Boya/imagen3.jpg",
    "/imagenes/Imagenes-comodoro-Ivan/imagen15.jpg",
    "/imagenes/Imagenes-comodoro-Ivan/imagen10.jpg",
    "/imagenes/Imagenes-comodoro-Ivan/imagen6.jpg",
    "/imagenes/Costa-RadaTilly.jpg",
    "/imagenes/loberia-rio-negro.jpeg",
    "/imagenes/foto-boya-dia1.png",
    "/imagenes/lobomarino-gaviotas.jpg",
    "/imagenes/faro-comodoro-rivadavia.jpeg",
  ];

  let images = [];

  function seededShuffle(array, seed) {
    let result = [...array];
    let random = mulberry32(seed);
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }

  function mulberry32(a) {
    return function () {
      let t = a += 0x6D2B79F5;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  onMount(() => {
    // Mezclamos solo una vez y guardamos el resultado
    images = seededShuffle(originalImages, Date.now() % 100000);

  });
</script>

<div class="relative w-full overflow-hidden">
  <div class="flex animate-marquee">
    {#each images as image}
      <div class="flex-shrink-0">
        <img src={image} alt="Imagen" class="w-auto h-96 object-contain" />
      </div>
    {/each}
    {#each images as image}
      <div class="flex-shrink-0">
        <img src={image} alt="Imagen" class="w-auto h-96 object-contain" />
      </div>
    {/each}
  </div>
</div>

<style>
  @keyframes marquee {
    0% {
      transform: translateX(0);
    }
    100% {
      transform: translateX(-50%);
    }
  }

  .animate-marquee {
    animation: marquee 30s linear infinite;
  }
</style>
