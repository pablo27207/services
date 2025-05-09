

<script>
    import Navbar from "../lib/components/Navbar.svelte";
    import Footer from "../lib/components/Footer.svelte";
    import "../app.css";
  </script>
  
  <Navbar />
  
  <div class="content relative z-10 overflow-visible">
    <slot />
  </div>
  
  <Footer />
  