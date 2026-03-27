<script>
  import HeroInformacionCosta from './HeroInformacionCosta.svelte';
  import GridTemasCosta from './GridTemasCosta.svelte';
</script>

<section class="informacion-costa">
  <HeroInformacionCosta />
  <GridTemasCosta />
</section>

<style>
  .informacion-costa {
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(to bottom, #061826 0%, #0b2233 30%, #f4f8fb 30%, #f4f8fb 100%);
  }
</style>