import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        proxy: {
            '/api': {
                target: 'http://api_ingestor:5000', // <-- Aquí el cambio clave
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '/api'),
            }
        }
    }
});

//import { sveltekit } from '@sveltejs/kit/vite';
//import { defineConfig } from 'vite';

//export default defineConfig({
  //plugins: [sveltekit()],
  //server: {
    ////'/api': {
       // target: 'http://127.0.0.1:5000',
        //changeOrigin: true,
        //secure: false,
      //}
    //}
  //}
//});
