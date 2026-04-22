<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  preserveAspectRatio="xMidYMid meet"
  width="100%"
  height="100%"
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
    <!-- Arena / playa -->
    <linearGradient id="v-arena" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e8d5a3" />
      <stop offset="100%" stop-color="#c9a86a" />
    </linearGradient>
    <marker id="v-arr-on" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0, 9 3.5, 0 7" fill="#c0392b" />
    </marker>
    <marker id="v-arr-off" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0, 9 3.5, 0 7" fill="#0d6ea8" />
    </marker>
  </defs>

  <!-- Sky -->
  <rect width="700" height="360" fill="url(#v-sky)" />

  <!-- Clouds -->
  <ellipse cx="95"  cy="52" rx="58" ry="14" fill="white" opacity="0.38" />
  <ellipse cx="148" cy="48" rx="42" ry="11" fill="white" opacity="0.3"  />
  <ellipse cx="530" cy="44" rx="64" ry="15" fill="white" opacity="0.3"  />
  <ellipse cx="590" cy="40" rx="46" ry="12" fill="white" opacity="0.25" />

  <!-- Sea (left half) -->
  <rect x="0" y="220" width="340" height="140" fill="url(#v-mar)" />
  <path
    d="M0,234 Q43,224 86,234 Q129,244 172,234 Q215,224 258,234 Q301,244 340,234
       L340,252 Q301,262 258,252 Q215,242 172,252 Q129,262 86,252 Q43,242 0,252 Z"
    fill="#1d93d4" opacity="0.45"
  />
  <path
    d="M0,268 Q56,258 113,268 Q169,278 226,268 Q282,258 340,268
       L340,286 Q282,296 226,286 Q169,276 113,286 Q56,296 0,286 Z"
    fill="#1d93d4" opacity="0.35"
  />

  <!-- ARENA (derecha — playa costera, color arena) -->
  <rect x="360" y="220" width="340" height="140" fill="url(#v-arena)" />

  <!-- Textura arena: ondas suaves -->
  <path
    d="M360,240 Q440,232 520,242 Q600,252 700,238
       L700,256 Q600,270 520,260 Q440,250 360,258 Z"
    fill="#d4b882" opacity="0.5"
  />
  <path
    d="M360,278 Q450,268 540,278 Q630,288 700,274
       L700,292 Q630,306 540,296 Q450,286 360,296 Z"
    fill="#c4a46a" opacity="0.4"
  />

  <!-- Piedras/guijarros patagónicos en la playa (colores tierra) -->
  <ellipse cx="420" cy="274" rx="22" ry="8"  fill="#b08a55" opacity="0.55" />
  <ellipse cx="480" cy="258" rx="14" ry="5"  fill="#b08a55" opacity="0.45" />
  <ellipse cx="555" cy="290" rx="18" ry="6"  fill="#b08a55" opacity="0.5"  />
  <ellipse cx="630" cy="266" rx="24" ry="8"  fill="#b08a55" opacity="0.5"  />
  <ellipse cx="680" cy="300" rx="14" ry="5"  fill="#987850" opacity="0.45" />

  <!-- Divisoria costa -->
  <rect x="340" y="0" width="20" height="360" fill="#c9a86a" opacity="0.45" />
  <path
    d="M338,220 Q350,210 362,220 L362,360 L338,360 Z"
    fill="#b89060" opacity="0.3"
  />

  <!-- Etiqueta: MAR -->
  <rect x="16" y="190" width="64" height="22" rx="6" fill="rgba(13,110,168,0.85)" />
  <text x="25" y="206" font-family="system-ui,sans-serif" font-size="12" fill="white" font-weight="700">MAR</text>

  <!-- Etiqueta: COSTA -->
  <rect x="620" y="190" width="68" height="22" rx="6" fill="rgba(180,140,80,0.9)" />
  <text x="630" y="206" font-family="system-ui,sans-serif" font-size="12" fill="white" font-weight="700">COSTA</text>

  <!-- ONSHORE arrows (mar → costa, de izquierda a derecha) — rojo -->
  <line x1="28"  y1="78"  x2="318" y2="78"  stroke="#c0392b" stroke-width="3.5" marker-end="url(#v-arr-on)" stroke-linecap="round" />
  <line x1="48"  y1="128" x2="318" y2="128" stroke="#c0392b" stroke-width="3.5" marker-end="url(#v-arr-on)" stroke-linecap="round" />
  <line x1="28"  y1="178" x2="318" y2="178" stroke="#c0392b" stroke-width="3.5" marker-end="url(#v-arr-on)" stroke-linecap="round" />

  <!-- Label ONSHORE -->
  <rect x="32" y="50" width="118" height="20" rx="5" fill="rgba(192,57,43,0.12)" />
  <text x="40" y="64" font-family="system-ui,sans-serif" font-size="11" fill="#c0392b" font-weight="700">ONSHORE →</text>

  <!-- OFFSHORE arrows (costa → mar, de derecha a izquierda) — azul -->
  <line x1="670" y1="78"  x2="382" y2="78"  stroke="#0d6ea8" stroke-width="3.5" marker-end="url(#v-arr-off)" stroke-linecap="round" />
  <line x1="650" y1="128" x2="382" y2="128" stroke="#0d6ea8" stroke-width="3.5" marker-end="url(#v-arr-off)" stroke-linecap="round" />
  <line x1="670" y1="178" x2="382" y2="178" stroke="#0d6ea8" stroke-width="3.5" marker-end="url(#v-arr-off)" stroke-linecap="round" />

  <!-- Label OFFSHORE -->
  <rect x="548" y="50" width="120" height="20" rx="5" fill="rgba(13,110,168,0.1)" />
  <text x="554" y="64" font-family="system-ui,sans-serif" font-size="11" fill="#0d6ea8" font-weight="700">← OFFSHORE</text>

  <!-- Silueta humana en la línea de costa -->
  <circle cx="350" cy="200" r="9"  fill="#1e2e3a" />
  <path d="M350,209 L350,241" stroke="#1e2e3a" stroke-width="5"   stroke-linecap="round" />
  <path d="M334,221 L350,218 L366,221" stroke="#1e2e3a" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M350,241 L339,264" stroke="#1e2e3a" stroke-width="4.5" stroke-linecap="round" />
  <path d="M350,241 L361,264" stroke="#1e2e3a" stroke-width="4.5" stroke-linecap="round" />
  <ellipse cx="352" cy="268" rx="14" ry="4" fill="#1e2e3a" opacity="0.16" />

  <!-- Badge advertencia offshore -->
  <rect x="374" y="138" width="158" height="36" rx="8" fill="rgba(13,110,168,0.92)" />
  <text x="384" y="152" font-family="system-ui,sans-serif" font-size="10" fill="white" font-weight="700">⚠ RIESGO OFFSHORE</text>
  <text x="384" y="167" font-family="system-ui,sans-serif" font-size="9.5" fill="#cde8f5">Arrastra flotadores al mar</text>
</svg>
