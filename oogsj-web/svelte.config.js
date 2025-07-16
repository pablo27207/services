import adapter from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';

const config = {
  preprocess: preprocess(),

  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build', // ✅ esta línea es importante
      fallback: 'index.html',
      precompress: false
    }),
    paths: {
      base: '',
      assets: ''
    }
    // 🚫 sin prerender, como querés
  }
};

export default config;

