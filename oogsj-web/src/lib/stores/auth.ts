import { writable } from 'svelte/store';

type User = { username: string } | null;

function createAuthStore() {
  const initial = typeof localStorage !== 'undefined'
    ? (localStorage.getItem('oogsj_user') ? { username: localStorage.getItem('oogsj_user')! } : null)
    : null;

  const { subscribe, set } = writable<User>(initial);

  return {
    subscribe,
    login(username: string) {
      localStorage.setItem('oogsj_user', username);
      set({ username });
    },
    logout() {
      localStorage.removeItem('oogsj_user');
      set(null);
    }
  };
}

export const auth = createAuthStore();
