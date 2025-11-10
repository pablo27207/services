<script lang="ts">
  import { onMount } from 'svelte';

  let sending = false;
  let okMsg = '';
  let errMsg = '';

  async function onSubmit(e: Event) {
    e.preventDefault();
    okMsg = ''; errMsg = '';
    sending = true;

    const formEl = e.target as HTMLFormElement;
    const fd = new FormData(formEl);

    try {
      // Endpoint público (proxied por nginx al Flask): ajusta si usás otro
      const res = await fetch('/api/library/upload', {
        method: 'POST',
        body: fd,
        credentials: 'include'
      });
      if (!res.ok) throw new Error(await res.text());
      okMsg = 'Documento subido correctamente.';
      formEl.reset();
    } catch (err: any) {
      errMsg = err?.message ?? 'Error subiendo el documento.';
    } finally {
      sending = false;
    }
  }
</script>

<div class="max-w-3xl mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Subir documento</h1>

  {#if okMsg}<div class="alert alert-success mb-3">{okMsg}</div>{/if}
  {#if errMsg}<div class="alert alert-error mb-3">{errMsg}</div>{/if}

  <form class="card bg-base-200 shadow-xl" on:submit={onSubmit}>
    <div class="card-body grid grid-cols-1 md:grid-cols-2 gap-4">
      <label class="form-control">
        <span class="label-text">Título *</span>
        <input name="title" required class="input input-bordered" />
      </label>

      <label class="form-control">
        <span class="label-text">Año</span>
        <input name="year" type="number" min="1800" max="2100" class="input input-bordered" />
      </label>

      <label class="form-control md:col-span-2">
        <span class="label-text">Autores (separados por coma)</span>
        <input name="authors" class="input input-bordered" placeholder="Apellido, Nombre; Apellido, Nombre" />
      </label>

      <label class="form-control">
        <span class="label-text">Revista / Venue</span>
        <input name="venue" class="input input-bordered" />
      </label>

      <label class="form-control">
        <span class="label-text">DOI</span>
        <input name="doi" class="input input-bordered" />
      </label>

      <label class="form-control md:col-span-2">
        <span class="label-text">URL</span>
        <input name="url" type="url" class="input input-bordered" />
      </label>

      <label class="form-control md:col-span-2">
        <span class="label-text">Resumen</span>
        <textarea name="abstract" rows="4" class="textarea textarea-bordered"></textarea>
      </label>

      <label class="form-control md:col-span-2">
        <span class="label-text">Archivo PDF *</span>
        <input name="file" type="file" accept="application/pdf" required class="file-input file-input-bordered" />
      </label>

      <div class="md:col-span-2 flex justify-end">
        <button class="btn btn-primary" disabled={sending}>
          {#if sending}<span class="loading loading-spinner"></span>{/if}
          Subir
        </button>
      </div>
    </div>
  </form>
</div>
