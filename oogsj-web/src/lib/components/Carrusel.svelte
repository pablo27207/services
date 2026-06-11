<script>
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';

  const originalImages = [
    "/imagenes/cola-ballena.webp",
    "/imagenes/Pingüinos.webp",
    "/imagenes/Península-valdez-chubut.webp",
    "/imagenes/Despliegue-Boya/imagen1.webp",
    "/imagenes/Despliegue-Boya/imagen2.webp",
    "/imagenes/Despliegue-Boya/imagen3.webp",
    "/imagenes/Imagenes-comodoro-Ivan/imagen15.webp",
    "/imagenes/Imagenes-comodoro-Ivan/imagen10.webp",
    "/imagenes/Imagenes-comodoro-Ivan/imagen6.webp",
    "/imagenes/Costa-RadaTilly.webp",
    "/imagenes/loberia-rio-negro.webp",
    "/imagenes/foto-boya-dia1.webp",
    "/imagenes/lobomarino-gaviotas.webp",
    "/imagenes/faro-comodoro-rivadavia.webp",
  ];

  let images = [];
  let current = 0;
  let timer;

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

  function next() {
    current = (current + 1) % images.length;
    resetTimer();
  }

  function prev() {
    current = (current - 1 + images.length) % images.length;
    resetTimer();
  }

  function goTo(i) {
    current = i;
    resetTimer();
  }

  function resetTimer() {
    clearInterval(timer);
    timer = setInterval(() => {
      current = (current + 1) % images.length;
    }, 5500);
  }

  onMount(() => {
    images = seededShuffle(originalImages, Date.now() % 100000);
    resetTimer();
  });

  onDestroy(() => clearInterval(timer));
</script>

<div class="hero-carousel">
  {#if images.length > 0}
    {#key current}
      <div class="slide" in:fade={{ duration: 900 }}>
        <img src={images[current]} alt="Golfo San Jorge" class="slide-img" />
      </div>
    {/key}
  {/if}

  <div class="overlay"></div>

  <div class="hero-text">
    <p class="hero-sub">Monitoreo marino · Patagonia Argentina</p>
    <h1 class="hero-title">Observatorio del<br />Golfo San Jorge</h1>
    <div class="hero-divider"></div>
    <p class="hero-desc">Ciencia, tecnología y soberanía ambiental en el Atlántico Sur</p>
  </div>

  <div class="dots">
    {#each images as _, i}
      <button
        class="dot"
        class:active={i === current}
        on:click={() => goTo(i)}
        aria-label="Ir a imagen {i + 1}"
      ></button>
    {/each}
  </div>

  <button class="arrow left" on:click={prev} aria-label="Anterior">&#8249;</button>
  <button class="arrow right" on:click={next} aria-label="Siguiente">&#8250;</button>
</div>

<style>
  .hero-carousel {
    position: relative;
    width: 100%;
    height: 78vh;
    min-height: 420px;
    overflow: hidden;
    background: #0a1628;
  }

  .slide {
    position: absolute;
    inset: 0;
  }

  .slide-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    animation: kenburns 9s ease-in-out forwards;
  }

  @keyframes kenburns {
    0%   { transform: scale(1)    translate(0,    0);    }
    100% { transform: scale(1.08) translate(-1.5%, 0.8%); }
  }

  .overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      160deg,
      rgba(0, 0, 0, 0.10) 0%,
      rgba(0, 10, 30, 0.20) 40%,
      rgba(0, 10, 30, 0.72) 100%
    );
    pointer-events: none;
  }

  .hero-text {
    position: absolute;
    bottom: 90px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    color: #fff;
    text-shadow: 0 2px 16px rgba(0, 0, 0, 0.65);
    pointer-events: none;
    width: 90%;
    max-width: 760px;
    animation: rise 1.2s ease both;
  }

  @keyframes rise {
    from { opacity: 0; transform: translateX(-50%) translateY(22px); }
    to   { opacity: 1; transform: translateX(-50%) translateY(0); }
  }

  .hero-sub {
    font-size: 0.8rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #fb923c;
    margin-bottom: 12px;
    font-weight: 700;
  }

  .hero-title {
    font-size: clamp(1.9rem, 5.5vw, 3.8rem);
    font-weight: 900;
    line-height: 1.1;
    color: #fff;
    margin: 0;
  }

  .hero-divider {
    width: 56px;
    height: 3px;
    background: #f97316;
    margin: 16px auto;
    border-radius: 2px;
  }

  .hero-desc {
    font-size: clamp(0.85rem, 2vw, 1.05rem);
    color: rgba(255, 255, 255, 0.82);
    letter-spacing: 0.03em;
    margin: 0;
  }

  .dots {
    position: absolute;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 9px;
    z-index: 10;
  }

  .dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.35);
    border: 1.5px solid rgba(255, 255, 255, 0.5);
    cursor: pointer;
    transition: background 0.3s, transform 0.3s, border-color 0.3s;
    padding: 0;
  }

  .dot.active {
    background: #f97316;
    border-color: #f97316;
    transform: scale(1.5);
  }

  .arrow {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0, 0, 0, 0.28);
    backdrop-filter: blur(4px);
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 2.2rem;
    line-height: 1;
    width: 48px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 6px;
    transition: background 0.2s, border-color 0.2s;
    z-index: 10;
  }

  .arrow:hover {
    background: rgba(249, 115, 22, 0.55);
    border-color: #f97316;
  }

  .arrow.left  { left:  14px; }
  .arrow.right { right: 14px; }
</style>
