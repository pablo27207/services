import containerQueries from '@tailwindcss/container-queries';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import type { Config } from 'tailwindcss';
import daisyui from "daisyui";

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],

  theme: {
    extend: {}, 
  },

  daisyui: {
    themes: ["night"], // <-- Mueve la configuración de DaisyUI aquí
  },

  plugins: [daisyui, typography, forms, containerQueries]
} satisfies Config;
