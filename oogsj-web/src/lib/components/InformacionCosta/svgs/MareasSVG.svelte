<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  preserveAspectRatio="xMidYMid meet"
  width="100%"
  height="100%"
  role="img"
  aria-label="Ciclo de mareas: comparación pleamar y bajamar en el Golfo San Jorge"
>
  <defs>
    <linearGradient id="m-sky-l" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0c1f2e" />
      <stop offset="100%" stop-color="#1a3d5c" />
    </linearGradient>
    <linearGradient id="m-sky-r" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4a8fb5" />
      <stop offset="100%" stop-color="#7bbdd8" />
    </linearGradient>
    <linearGradient id="m-agua-alta" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d6ea8" />
      <stop offset="100%" stop-color="#061826" />
    </linearGradient>
    <linearGradient id="m-agua-baja" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a93d4" />
      <stop offset="100%" stop-color="#0d5280" />
    </linearGradient>
    <linearGradient id="m-roca" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#7d8f99" />
      <stop offset="100%" stop-color="#3a4e5a" />
    </linearGradient>
    <linearGradient id="m-roca-exp" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#9aafba" />
      <stop offset="100%" stop-color="#5a7080" />
    </linearGradient>
    <linearGradient id="m-arena" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e8d5a3" />
      <stop offset="100%" stop-color="#c9a86a" />
    </linearGradient>
    <clipPath id="m-clip-l">
      <rect x="0" y="0" width="330" height="360" />
    </clipPath>
    <clipPath id="m-clip-r">
      <rect x="370" y="0" width="330" height="360" />
    </clipPath>
  </defs>

  <!-- ══ PANEL IZQUIERDO: PLEAMAR (noche / luna) ══ -->
  <rect x="0" y="0" width="330" height="360" fill="url(#m-sky-l)" />

  <!-- Estrellas -->
  <circle cx="35"  cy="22" r="1.4" fill="white" opacity="0.7" />
  <circle cx="95"  cy="40" r="1"   fill="white" opacity="0.55" />
  <circle cx="165" cy="18" r="1.4" fill="white" opacity="0.65" />
  <circle cx="240" cy="36" r="1"   fill="white" opacity="0.5"  />
  <circle cx="55"  cy="58" r="1"   fill="white" opacity="0.5"  />
  <circle cx="290" cy="26" r="1.2" fill="white" opacity="0.55" />

  <!-- Luna -->
  <circle cx="285" cy="52" r="30" fill="#8fd3ff" opacity="0.1" />
  <circle cx="285" cy="52" r="22" fill="#f4edcc" opacity="0.88" />
  <circle cx="277" cy="45" r="4"  fill="#e8ddb8" opacity="0.5"  />
  <circle cx="294" cy="60" r="2.5" fill="#e8ddb8" opacity="0.4" />

  <!-- Rocas patagónicas — sección ALTA (cubierta en pleamar) -->
  <path
    d="M220,118 L235,102 L248,118 L262,98 L276,114 L292,96
       L308,112 L325,94 L330,100 L330,360 L220,360 Z"
    fill="url(#m-roca)"
    clip-path="url(#m-clip-l)"
  />
  <path
    d="M220,158 L238,145 L255,160 L272,143 L288,158 L306,140
       L322,155 L330,148 L330,195 L220,195 Z"
    fill="#546a79" opacity="0.5"
    clip-path="url(#m-clip-l)"
  />

  <!-- Agua PLEAMAR alta -->
  <rect x="0" y="148" width="220" height="212" fill="url(#m-agua-alta)" />
  <!-- Superficie agua alta (suave) -->
  <path
    d="M0,148 Q55,138 110,148 Q165,158 220,148 L220,168 Q165,178 110,168 Q55,158 0,168 Z"
    fill="#1d93d4" opacity="0.4"
    clip-path="url(#m-clip-l)"
  />
  <!-- Agua cubre las rocas -->
  <rect x="220" y="148" width="110" height="212" fill="url(#m-agua-alta)" opacity="0.6"
    clip-path="url(#m-clip-l)" />

  <!-- Reflejo de luna -->
  <ellipse cx="140" cy="195" rx="55" ry="9" fill="#f4edcc" opacity="0.07" />

  <!-- Línea de nivel PLEAMAR -->
  <line x1="0" y1="148" x2="330" y2="148" stroke="#8fd3ff" stroke-width="1.4" stroke-dasharray="8,5" opacity="0.6" />

  <!-- Badge PLEAMAR -->
  <rect x="12" y="118" width="118" height="26" rx="7" fill="rgba(13,110,168,0.9)" />
  <text x="22" y="136" font-family="system-ui,sans-serif" font-size="13" fill="white" font-weight="700">🌑 PLEAMAR</text>

  <!-- Flecha indicadora nivel alto -->
  <line x1="18" y1="155" x2="18" y2="320" stroke="#8fd3ff" stroke-width="2" opacity="0.5" />
  <polygon points="13,160 18,148 23,160" fill="#8fd3ff" opacity="0.7" />

  <!-- Arena playa invisible (cubierta) — sutil -->
  <rect x="0" y="320" width="220" height="40" fill="url(#m-arena)" opacity="0.25"
    clip-path="url(#m-clip-l)" />

  <!-- ══ PANEL DERECHO: BAJAMAR (día / sol) ══ -->
  <rect x="370" y="0" width="330" height="360" fill="url(#m-sky-r)" />

  <!-- Sol -->
  <circle cx="430" cy="52" r="26" fill="#f9d262" opacity="0.9" />
  <circle cx="430" cy="52" r="34" fill="#f9d262" opacity="0.18" />
  <!-- Rayos sol -->
  <line x1="430" y1="12"  x2="430" y2="4"   stroke="#f9d262" stroke-width="2.5" stroke-linecap="round" opacity="0.7" />
  <line x1="455" y1="27"  x2="462" y2="20"  stroke="#f9d262" stroke-width="2.5" stroke-linecap="round" opacity="0.7" />
  <line x1="465" y1="52"  x2="474" y2="52"  stroke="#f9d262" stroke-width="2.5" stroke-linecap="round" opacity="0.7" />
  <line x1="455" y1="77"  x2="462" y2="84"  stroke="#f9d262" stroke-width="2.5" stroke-linecap="round" opacity="0.7" />
  <line x1="405" y1="27"  x2="398" y2="20"  stroke="#f9d262" stroke-width="2.5" stroke-linecap="round" opacity="0.7" />
  <line x1="395" y1="52"  x2="386" y2="52"  stroke="#f9d262" stroke-width="2.5" stroke-linecap="round" opacity="0.7" />

  <!-- Rocas EXPUESTAS en bajamar -->
  <path
    d="M580,88 L596,72 L610,88 L624,68 L638,84 L654,64
       L670,80 L686,62 L700,74 L700,360 L580,360 Z"
    fill="url(#m-roca-exp)"
    clip-path="url(#m-clip-r)"
  />
  <!-- Zona intermareal expuesta (con algas, moluscos) -->
  <path
    d="M580,148 L596,138 L614,152 L632,136 L650,150 L668,134
       L686,148 L700,140 L700,220 L580,220 Z"
    fill="#4a7a6a" opacity="0.55"
    clip-path="url(#m-clip-r)"
  />
  <!-- Pozas de marea -->
  <ellipse cx="622" cy="208" rx="20" ry="7" fill="#1a93d4" opacity="0.55" />
  <ellipse cx="665" cy="228" rx="14" ry="5" fill="#1a93d4" opacity="0.45" />

  <!-- Arena playa expuesta en bajamar -->
  <path
    d="M370,252 Q460,244 580,250 L580,360 L370,360 Z"
    fill="url(#m-arena)"
    clip-path="url(#m-clip-r)"
  />
  <!-- Textura arena -->
  <path
    d="M370,268 Q445,260 520,268 Q560,272 580,268 L580,284 Q560,288 520,284 Q445,276 370,284 Z"
    fill="#d4b882" opacity="0.5"
    clip-path="url(#m-clip-r)"
  />
  <!-- Piedras en arena -->
  <ellipse cx="440" cy="290" rx="18" ry="6" fill="#b08a55" opacity="0.5" />
  <ellipse cx="510" cy="305" rx="14" ry="5" fill="#b08a55" opacity="0.45" />

  <!-- Agua BAJAMAR (nivel bajo) -->
  <rect x="370" y="228" width="210" height="24" fill="url(#m-agua-baja)" opacity="0.7"
    clip-path="url(#m-clip-r)" />
  <rect x="370" y="252" width="210" height="108" fill="url(#m-agua-baja)" opacity="0.0" />
  <!-- Frente del agua en bajamar -->
  <path
    d="M370,228 Q415,220 460,228 Q505,236 540,228 Q560,224 580,228
       L580,248 Q560,244 540,248 Q505,256 460,248 Q415,240 370,248 Z"
    fill="#1d93d4" opacity="0.5"
    clip-path="url(#m-clip-r)"
  />

  <!-- Línea de nivel BAJAMAR -->
  <line x1="370" y1="228" x2="700" y2="228" stroke="#8fd3ff" stroke-width="1.4" stroke-dasharray="8,5" opacity="0.55" />

  <!-- Badge BAJAMAR -->
  <rect x="378" y="118" width="118" height="26" rx="7" fill="rgba(9,38,58,0.85)" />
  <text x="388" y="136" font-family="system-ui,sans-serif" font-size="13" fill="#f4edcc" font-weight="700">☀ BAJAMAR</text>

  <!-- Badge zona intermareal -->
  <rect x="470" y="150" width="104" height="22" rx="6" fill="rgba(74,122,106,0.88)" />
  <text x="479" y="165" font-family="system-ui,sans-serif" font-size="10" fill="white" font-weight="700">Zona expuesta</text>

  <!-- ══ DIVISOR CENTRAL ══ -->
  <rect x="330" y="0" width="40" height="360" fill="#0a2436" />

  <!-- Flecha doble vertical: diferencia de nivel ~5m -->
  <line x1="350" y1="154" x2="350" y2="224" stroke="#f4edcc" stroke-width="2.5" />
  <polygon points="344,160 350,148 356,160" fill="#f4edcc" />
  <polygon points="344,218 350,230 356,218" fill="#f4edcc" />
  <rect x="328" y="178" width="44" height="18" rx="4" fill="rgba(10,26,38,0.9)" />
  <text x="334" y="191" font-family="system-ui,sans-serif" font-size="10.5" fill="#f4edcc" font-weight="700">≈ 5 m</text>

  <!-- Tiempo entre estados -->
  <rect x="320" y="310" width="60" height="34" rx="6" fill="rgba(10,26,38,0.88)" />
  <text x="328" y="325" font-family="system-ui,sans-serif" font-size="9" fill="#8fd3ff" font-weight="700">≈ 6 hs</text>
  <text x="325" y="338" font-family="system-ui,sans-serif" font-size="8.5" fill="#cde8f5">entre estados</text>

  <!-- Etiqueta ← Pleamar / Bajamar → -->
  <text x="162" y="348" font-family="system-ui,sans-serif" font-size="10" fill="#8fd3ff" font-weight="600" text-anchor="middle" opacity="0.7">Nivel alto</text>
  <text x="535" y="348" font-family="system-ui,sans-serif" font-size="10" fill="#c9a86a" font-weight="600" text-anchor="middle" opacity="0.8">Playa ampliada</text>
</svg>
