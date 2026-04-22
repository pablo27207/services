import { writable } from 'svelte/store';

export type AdminUser = {
  id:         number;
  email:      string;
  first_name: string;
  last_name:  string;
  is_admin:   boolean;
};

type AuthState = {
  user:    AdminUser | null;
  checked: boolean;   // true una vez que se consultó /api/auth/me
  loading: boolean;
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    user:    null,
    checked: false,
    loading: false,
  });

  const store = {
    subscribe,

    /** Verifica el estado de auth contra el backend (httponly cookie). */
    async init(): Promise<AdminUser | null> {
      update(s => ({ ...s, loading: true }));
      try {
        const res  = await fetch('/api/auth/me', { credentials: 'include' });
        const data = await res.json();
        const user = data.authenticated ? (data.user as AdminUser) : null;
        set({ user, checked: true, loading: false });
        return user;
      } catch {
        set({ user: null, checked: true, loading: false });
        return null;
      }
    },

    /** Login real contra la API. Lanza un Error con el mensaje si falla. */
    async login(email: string, password: string): Promise<void> {
      update(s => ({ ...s, loading: true }));
      const res = await fetch('/api/auth/login', {
        method:      'POST',
        credentials: 'include',
        headers:     { 'Content-Type': 'application/json' },
        body:        JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        update(s => ({ ...s, loading: false }));
        throw new Error(body.error ?? 'Error al iniciar sesión');
      }
      // Cookie seteada → verificar quién es
      await store.init();
    },

    /** Logout real contra la API. */
    async logout(): Promise<void> {
      await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });
      set({ user: null, checked: true, loading: false });
    },
  };

  return store;
}

export const authStore = createAuthStore();
