import { writable } from 'svelte/store';

// Creamos un store writable para almacenar la plataforma seleccionada
export const plataformaSeleccionada = writable(null);
