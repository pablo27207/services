<script>
  import HeroInformacionCosta from './HeroInformacionCosta.svelte';
  import GridTemasCosta from './GridTemasCosta.svelte';
  import EscenariosCosta from './EscenariosCosta.svelte';
  import ChecklistCosta from './ChecklistCosta.svelte';
  import AvisosNavegante from './AvisosNavegante.svelte';
</script>

<section class="informacion-costa">
  <HeroInformacionCosta />
  <GridTemasCosta />
  <EscenariosCosta />
  <ChecklistCosta />
  <AvisosNavegante /> 
</section>

<style>
  .informacion-costa {
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(
      to bottom,
      #061826 0%,
      #0b2233 24%,
      #f4f8fb 24%,
      #f4f8fb 100%
    );
  }
</style>