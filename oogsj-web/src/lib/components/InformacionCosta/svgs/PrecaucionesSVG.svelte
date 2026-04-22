<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  preserveAspectRatio="xMidYMid meet"
  width="100%"
  height="100%"
  role="img"
  aria-label="Precauciones: temperatura del agua e hipotermia en el Golfo San Jorge"
>
  <defs>
    <linearGradient id="p-sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d6eaf4" />
      <stop offset="100%" stop-color="#9dcce8" />
    </linearGradient>
    <linearGradient id="p-mar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a7baa" />
      <stop offset="100%" stop-color="#061826" />
    </linearGradient>
    <linearGradient id="p-arena" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e8d5a3" />
      <stop offset="100%" stop-color="#c9a86a" />
    </linearGradient>
    <linearGradient id="p-thermo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2ecc71" />
      <stop offset="35%" stop-color="#f1c40f" />
      <stop offset="65%" stop-color="#e67e22" />
      <stop offset="100%" stop-color="#e74c3c" />
    </linearGradient>
  </defs>

  <!-- Sky -->
  <rect width="700" height="360" fill="url(#p-sky)" />

  <!-- Líneas de viento -->
  <path d="M20,48 Q72,40 125,48"  stroke="#7dc0e8" stroke-width="2"   fill="none" stroke-linecap="round" opacity="0.65" />
  <path d="M12,72 Q88,62 160,72"  stroke="#7dc0e8" stroke-width="1.8" fill="none" stroke-linecap="round" opacity="0.55" />
  <path d="M450,42 Q530,34 610,42" stroke="#7dc0e8" stroke-width="2"  fill="none" stroke-linecap="round" opacity="0.5"  />

  <!-- Mar -->
  <rect x="0" y="242" width="700" height="118" fill="url(#p-mar)" />
  <path
    d="M0,242 Q88,232 175,242 Q263,252 350,242 Q438,232 525,242 Q613,252 700,242
       L700,260 Q613,270 525,260 Q438,250 350,260 Q263,270 175,260 Q88,250 0,260 Z"
    fill="#1d93d4" opacity="0.38"
  />
  <path
    d="M0,278 Q113,268 225,278 Q338,288 450,278 Q563,268 700,278
       L700,296 Q563,308 450,296 Q338,284 225,296 Q113,308 0,296 Z"
    fill="#1d93d4" opacity="0.28"
  />

  <!-- Playa (arena) -->
  <path d="M0,236 Q350,224 700,236 L700,360 L0,360 Z" fill="url(#p-arena)" />
  <ellipse cx="90"  cy="268" rx="26" ry="8"  fill="#b08a55" opacity="0.5" />
  <ellipse cx="210" cy="278" rx="18" ry="6"  fill="#b08a55" opacity="0.45" />
  <ellipse cx="540" cy="262" rx="22" ry="7"  fill="#b08a55" opacity="0.45" />
  <ellipse cx="640" cy="276" rx="26" ry="8"  fill="#b08a55" opacity="0.5" />

  <!-- Colchoneta arrastrada offshore -->
  <rect x="500" y="226" width="62" height="24" rx="7" fill="#e74c3c" opacity="0.85" />
  <line x1="500" y1="238" x2="562" y2="238" stroke="white" stroke-width="1.2" opacity="0.4" />
  <line x1="531" y1="226" x2="531" y2="250" stroke="white" stroke-width="1.2" opacity="0.4" />
  <line x1="568" y1="238" x2="606" y2="238" stroke="#c0392b" stroke-width="2.5" stroke-linecap="round" />
  <polygon points="598,233 608,238 598,243" fill="#c0392b" />

  <!-- Dos personas en la orilla -->
  <circle cx="148" cy="206" r="9"  fill="#1e2e3a" />
  <path d="M148,215 L148,246" stroke="#1e2e3a" stroke-width="5" stroke-linecap="round" />
  <path d="M132,228 L148,225 L164,228" stroke="#1e2e3a" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M148,246 L138,268" stroke="#1e2e3a" stroke-width="4.5" stroke-linecap="round" />
  <path d="M148,246 L158,268" stroke="#1e2e3a" stroke-width="4.5" stroke-linecap="round" />
  <circle cx="182" cy="210" r="8"  fill="#2d3f4b" />
  <path d="M182,218 L182,246" stroke="#2d3f4b" stroke-width="4.5" stroke-linecap="round" />
  <path d="M168,228 L182,226 L196,228" stroke="#2d3f4b" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M182,246 L173,266" stroke="#2d3f4b" stroke-width="4" stroke-linecap="round" />
  <path d="M182,246 L191,266" stroke="#2d3f4b" stroke-width="4" stroke-linecap="round" />

  <!-- ══ PANEL HIPOTERMIA (derecha) ══ -->
  <rect x="356" y="10" width="332" height="218" rx="14" fill="rgba(9,26,40,0.88)" />

  <!-- Título panel -->
  <text x="376" y="36" font-family="system-ui,sans-serif" font-size="13" fill="white" font-weight="700">TEMPERATURA DEL AGUA — GSJ</text>

  <!-- Termómetro -->
  <!-- Tubo -->
  <rect x="374" y="52" width="18" height="118" rx="9" fill="#1a3a52" />
  <!-- Relleno termómetro -->
  <rect x="378" y="56" width="10" height="110" rx="5" fill="url(#p-thermo)" opacity="0.9" />
  <!-- Bulbo -->
  <circle cx="383" cy="172" r="12" fill="#e74c3c" />
  <!-- Marcas de temperatura -->
  <line x1="394" y1="58"  x2="400" y2="58"  stroke="#8fd3ff" stroke-width="1.5" />
  <line x1="394" y1="85"  x2="400" y2="85"  stroke="#8fd3ff" stroke-width="1.5" />
  <line x1="394" y1="112" x2="400" y2="112" stroke="#8fd3ff" stroke-width="1.5" />
  <line x1="394" y1="139" x2="400" y2="139" stroke="#8fd3ff" stroke-width="1.5" />
  <line x1="394" y1="166" x2="400" y2="166" stroke="#8fd3ff" stroke-width="1.5" />
  <text x="403" y="62"  font-family="system-ui,sans-serif" font-size="9" fill="#8fd3ff">20°C</text>
  <text x="403" y="89"  font-family="system-ui,sans-serif" font-size="9" fill="#8fd3ff">15°C</text>
  <text x="403" y="116" font-family="system-ui,sans-serif" font-size="9" fill="#8fd3ff">10°C</text>
  <text x="403" y="143" font-family="system-ui,sans-serif" font-size="9" fill="#8fd3ff"> 5°C</text>
  <text x="403" y="170" font-family="system-ui,sans-serif" font-size="9" fill="#8fd3ff"> 0°C</text>

  <!-- Indicador GSJ: 9-13°C (entre 5°C y 15°C) -->
  <rect x="374" y="88" width="14" height="52" rx="4" fill="rgba(143,211,255,0.25)" />
  <line x1="416" y1="112" x2="444" y2="112" stroke="#8fd3ff" stroke-width="1.4" stroke-dasharray="4,3" opacity="0.7" />
  <rect x="444" y="100" width="104" height="24" rx="6" fill="rgba(13,110,168,0.9)" />
  <text x="452" y="111" font-family="system-ui,sans-serif" font-size="10" fill="white" font-weight="700">GSJ: 9–13°C</text>
  <text x="452" y="123" font-family="system-ui,sans-serif" font-size="9" fill="#cde8f5">todo el año</text>

  <!-- Etapas hipotermia -->
  <!-- LEVE -->
  <rect x="376" y="136" width="300" height="24" rx="6" fill="rgba(241,196,15,0.2)" />
  <rect x="376" y="136" width="4"   height="24" rx="2" fill="#f1c40f" />
  <text x="386" y="149" font-family="system-ui,sans-serif" font-size="10" fill="#f1c40f" font-weight="700">LEVE</text>
  <text x="420" y="149" font-family="system-ui,sans-serif" font-size="9.5" fill="#d4e5f1">35°–32°C corporal · Escalofríos intensos</text>

  <!-- MODERADA -->
  <rect x="376" y="164" width="300" height="24" rx="6" fill="rgba(230,126,34,0.2)" />
  <rect x="376" y="164" width="4"   height="24" rx="2" fill="#e67e22" />
  <text x="386" y="177" font-family="system-ui,sans-serif" font-size="10" fill="#e67e22" font-weight="700">MODERADA</text>
  <text x="454" y="177" font-family="system-ui,sans-serif" font-size="9.5" fill="#d4e5f1">32°–28°C · Pérdida de coordinación</text>

  <!-- GRAVE -->
  <rect x="376" y="192" width="300" height="24" rx="6" fill="rgba(231,76,60,0.2)" />
  <rect x="376" y="192" width="4"   height="24" rx="2" fill="#e74c3c" />
  <text x="386" y="205" font-family="system-ui,sans-serif" font-size="10" fill="#e74c3c" font-weight="700">GRAVE</text>
  <text x="424" y="205" font-family="system-ui,sans-serif" font-size="9.5" fill="#d4e5f1">&lt;28°C · Inconsciencia · Paro cardíaco</text>

  <!-- Nota acción -->
  <rect x="376" y="220" width="298" height="22" rx="6" fill="rgba(231,76,60,0.35)" />
  <text x="386" y="235" font-family="system-ui,sans-serif" font-size="10" fill="white" font-weight="700">🆘 Llamar emergencias · Abrigo seco · No frotar</text>

  <!-- ══ PANEL TEMPERATURA AGUA (izquierda, pequeño) ══ -->
  <rect x="12" y="10" width="200" height="58" rx="10" fill="rgba(9,26,40,0.82)" />
  <text x="24" y="28" font-family="system-ui,sans-serif" font-size="11" fill="#8fd3ff" font-weight="700">AGUA FRÍA DEL GOLFO</text>
  <text x="24" y="46" font-family="system-ui,sans-serif" font-size="13" fill="white" font-weight="900">9 – 13 °C</text>
  <text x="24" y="60" font-family="system-ui,sans-serif" font-size="9.5" fill="#9dcce8">Provoca hiperventilación al ingresar</text>

  <!-- Pie nota -->
  <text x="16" y="350" font-family="system-ui,sans-serif" font-size="9" fill="#415766" opacity="0.7">
    Temperatura corporal normal: 37°C. El agua fría extrae calor 25× más rápido que el aire.
  </text>
</svg>
