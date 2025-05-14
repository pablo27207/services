

import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/api': {
        target: 'http://web_app:5001', // web_app es el nombre del servicio Docker
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
