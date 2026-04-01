<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label="Ilustración de ciclo de mareas: pleamar y bajamar en costa patagónica"
>
  <defs>
    <linearGradient id="m-sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0c1f2e" />
      <stop offset="100%" stop-color="#1a3d5c" />
    </linearGradient>
    <linearGradient id="m-mar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d6ea8" />
      <stop offset="100%" stop-color="#061826" />
    </linearGradient>
    <linearGradient id="m-roca" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#7d8f99" />
      <stop offset="100%" stop-color="#3a4e5a" />
    </linearGradient>
    <linearGradient id="m-intermareal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3d6070" />
      <stop offset="100%" stop-color="#274050" />
    </linearGradient>
  </defs>

  <!-- Night sky -->
  <rect width="700" height="360" fill="url(#m-sky)" />

  <!-- Stars -->
  <circle cx="45"  cy="28"  r="1.5" fill="white" opacity="0.65" />
  <circle cx="125" cy="48"  r="1"   fill="white" opacity="0.5" />
  <circle cx="210" cy="20"  r="1.5" fill="white" opacity="0.6" />
  <circle cx="310" cy="42"  r="1"   fill="white" opacity="0.45" />
  <circle cx="175" cy="14"  r="1"   fill="white" opacity="0.55" />
  <circle cx="420" cy="35"  r="1.2" fill="white" opacity="0.5" />
  <circle cx="88"  cy="65"  r="1"   fill="white" opacity="0.45" />

  <!-- Moon -->
  <circle cx="620" cy="58" r="36" fill="#8fd3ff" opacity="0.1" />
  <circle cx="620" cy="58" r="27" fill="#f4edcc" opacity="0.85" />
  <circle cx="611" cy="50" r="4.5" fill="#e8ddb8" opacity="0.55" />
  <circle cx="630" cy="65" r="3"   fill="#e8ddb8" opacity="0.45" />
  <circle cx="618" cy="68" r="2"   fill="#e8ddb8" opacity="0.4" />

  <!-- Rocky shore (right side) — path CERRADO correctamente -->
  <path
    d="M548,108 L562,90 L577,107 L592,86 L608,104 L624,82
       L641,100 L658,78 L675,96 L691,76 L700,86
       L700,360 L548,360 Z"
    fill="url(#m-roca)"
  />

  <!-- Rock layer mid -->
  <path
    d="M548,148 L566,135 L584,150 L601,132 L618,148 L636,128
       L654,144 L671,130 L690,146 L700,138
       L700,185 L548,185 Z"
    fill="#546a79"
    opacity="0.5"
  />

  <!-- Intertidal zone strip -->
  <path
    d="M548,185 L566,178 L584,188 L601,176 L618,186 L636,175
       L654,185 L671,176 L690,184 L700,179
       L700,220 L548,220 Z"
    fill="url(#m-intermareal)"
    opacity="0.7"
  />

  <!-- Sea fill pleamar -->
  <rect x="0" y="155" width="548" height="205" fill="url(#m-mar)" />
  <path
    d="M0,155 Q92,143 184,155 Q276,167 368,155 Q460,143 548,155
       L548,175 Q460,163 368,175 Q276,187 184,175 Q92,163 0,175 Z"
    fill="#1d93d4"
    opacity="0.45"
  />

  <!-- Pleamar label -->
  <rect x="14" y="134" width="122" height="28" rx="7" fill="rgba(13,110,168,0.85)" />
  <text x="26" y="153" font-family="system-ui,sans-serif" font-size="13" fill="white" font-weight="700">PLEAMAR</text>

  <!-- Bajamar dashed line -->
  <line x1="0" y1="226" x2="548" y2="226" stroke="#8fd3ff" stroke-width="1.6" stroke-dasharray="10,6" opacity="0.65" />

  <!-- Bajamar label -->
  <rect x="14" y="228" width="120" height="28" rx="7" fill="rgba(9,38,58,0.82)" />
  <text x="26" y="247" font-family="system-ui,sans-serif" font-size="13" fill="#8fd3ff" font-weight="700">BAJAMAR</text>

  <!-- Tidal range double arrow -->
  <line x1="505" y1="157" x2="505" y2="224" stroke="#f4edcc" stroke-width="2.2" />
  <polygon points="499,163 505,152 511,163" fill="#f4edcc" />
  <polygon points="499,218 505,229 511,218" fill="#f4edcc" />
  <rect x="468" y="180" width="68" height="22" rx="5" fill="rgba(10,26,38,0.75)" />
  <text x="476" y="196" font-family="system-ui,sans-serif" font-size="11" fill="#f4edcc" font-weight="600">~5 m</text>

  <!-- Moon reflection on water -->
  <ellipse cx="350" cy="200" rx="72" ry="12" fill="#f4edcc" opacity="0.08" />
  <line x1="350" y1="165" x2="350" y2="185" stroke="#f4edcc" stroke-width="1.4" stroke-dasharray="4,4" opacity="0.3" />

  <!-- Rock pool -->
  <ellipse cx="590" cy="215" rx="24" ry="9" fill="#1a93d4" opacity="0.5" />
</svg>