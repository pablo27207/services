<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label="Ilustración de viento onshore y offshore en la costa"
>
  <defs>
    <linearGradient id="v-sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#cde8f5" />
      <stop offset="100%" stop-color="#a8d8f0" />
    </linearGradient>
    <linearGradient id="v-mar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a7baa" />
      <stop offset="100%" stop-color="#061826" />
    </linearGradient>
    <linearGradient id="v-tierra" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8a9ba5" />
      <stop offset="100%" stop-color="#56686f" />
    </linearGradient>
    <!-- Arrowhead onshore: rojo cálido, apunta derecha -->
    <marker id="v-arr-on" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0, 9 3.5, 0 7" fill="#c0392b" />
    </marker>
    <!-- Arrowhead offshore: azul, orient auto lo rota al apuntar izquierda -->
    <marker id="v-arr-off" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0, 9 3.5, 0 7" fill="#0d6ea8" />
    </marker>
  </defs>

  <!-- Sky -->
  <rect width="700" height="360" fill="url(#v-sky)" />

  <!-- Sea (bottom left) -->
  <rect x="0" y="220" width="340" height="140" fill="url(#v-mar)" />
  <!-- Waves on sea -->
  <path
    d="M0,234 Q43,224 86,234 Q129,244 172,234 Q215,224 258,234 Q301,244 340,234
       L340,252 Q301,262 258,252 Q215,242 172,252 Q129,262 86,252 Q43,242 0,252 Z"
    fill="#1d93d4"
    opacity="0.45"
  />
  <path
    d="M0,268 Q56,258 113,268 Q169,278 226,268 Q282,258 340,268
       L340,286 Q282,296 226,286 Q169,276 113,286 Q56,296 0,286 Z"
    fill="#1d93d4"
    opacity="0.38"
  />

  <!-- Land (bottom right) -->
  <rect x="360" y="220" width="340" height="140" fill="url(#v-tierra)" />
  <!-- Land texture -->
  <path
    d="M360,232 Q440,222 520,234 Q600,246 700,232
       L700,252 Q600,266 520,254 Q440,242 360,252 Z"
    fill="#7d8f99"
    opacity="0.5"
  />
  <!-- Rocks on land -->
  <ellipse cx="430" cy="278" rx="28" ry="10" fill="#6b7c87" opacity="0.55" />
  <ellipse cx="555" cy="294" rx="22" ry="8"  fill="#6b7c87" opacity="0.5" />
  <ellipse cx="648" cy="270" rx="30" ry="11" fill="#6b7c87" opacity="0.5" />

  <!-- Coastline divider -->
  <rect x="340" y="0" width="20" height="360" fill="#7d8f99" opacity="0.55" />
  <path
    d="M338,0 L341,35 L337,65 L342,100 L337,135 L341,170
       L337,205 L342,240 L338,275 L341,310 L338,360"
    stroke="#546a79"
    stroke-width="1.8"
    fill="none"
    opacity="0.4"
  />

  <!-- ONSHORE arrows (sea → shore, left to right) — rojo -->
  <line x1="28"  y1="78"  x2="318" y2="78"  stroke="#c0392b" stroke-width="3.5" marker-end="url(#v-arr-on)" stroke-linecap="round" />
  <line x1="48"  y1="128" x2="318" y2="128" stroke="#c0392b" stroke-width="3.5" marker-end="url(#v-arr-on)" stroke-linecap="round" />
  <line x1="28"  y1="178" x2="318" y2="178" stroke="#c0392b" stroke-width="3.5" marker-end="url(#v-arr-on)" stroke-linecap="round" />

  <!-- OFFSHORE arrows (shore → sea, right to left) — azul -->
  <line x1="670" y1="78"  x2="382" y2="78"  stroke="#0d6ea8" stroke-width="3.5" marker-end="url(#v-arr-off)" stroke-linecap="round" />
  <line x1="650" y1="128" x2="382" y2="128" stroke="#0d6ea8" stroke-width="3.5" marker-end="url(#v-arr-off)" stroke-linecap="round" />
  <line x1="670" y1="178" x2="382" y2="178" stroke="#0d6ea8" stroke-width="3.5" marker-end="url(#v-arr-off)" stroke-linecap="round" />

  <!-- Human silhouette at coastline -->
  <circle cx="350" cy="205" r="9" fill="#1e2e3a" />
  <path d="M350,214 L350,246" stroke="#1e2e3a" stroke-width="5" stroke-linecap="round" />
  <path d="M334,226 L350,222 L366,226" stroke="#1e2e3a" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M350,246 L339,268" stroke="#1e2e3a" stroke-width="4.5" stroke-linecap="round" />
  <path d="M350,246 L361,268" stroke="#1e2e3a" stroke-width="4.5" stroke-linecap="round" />
  <ellipse cx="352" cy="272" rx="14" ry="4.5" fill="#1e2e3a" opacity="0.18" />
</svg>