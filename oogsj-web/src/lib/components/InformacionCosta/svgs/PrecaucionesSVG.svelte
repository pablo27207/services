<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label="Ilustración de precauciones generales en la costa patagónica"
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
    <linearGradient id="p-playa" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8a9ba5" />
      <stop offset="100%" stop-color="#56686f" />
    </linearGradient>
  </defs>

  <!-- Sky -->
  <rect width="700" height="360" fill="url(#p-sky)" />

  <!-- Wind lines in sky -->
  <path d="M28,52 Q85,44 140,52"  stroke="#7dc0e8" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0.7" />
  <path d="M20,78 Q94,67 168,78"  stroke="#7dc0e8" stroke-width="2"   fill="none" stroke-linecap="round" opacity="0.6" />
  <path d="M38,104 Q105,94 172,104" stroke="#7dc0e8" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.5" />
  <path d="M480,48 Q560,38 640,48" stroke="#7dc0e8" stroke-width="2"   fill="none" stroke-linecap="round" opacity="0.55" />
  <path d="M500,74 Q575,65 650,74" stroke="#7dc0e8" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.45" />

  <!-- Sea -->
  <rect x="0" y="235" width="700" height="125" fill="url(#p-mar)" />
  <path
    d="M0,235 Q88,225 175,235 Q263,245 350,235 Q438,225 525,235 Q613,245 700,235
       L700,255 Q613,265 525,255 Q438,245 350,255 Q263,265 175,255 Q88,245 0,255 Z"
    fill="#1d93d4"
    opacity="0.38"
  />
  <path
    d="M0,275 Q113,263 225,275 Q338,287 450,275 Q563,263 700,275
       L700,295 Q563,307 450,295 Q338,283 225,295 Q113,307 0,295 Z"
    fill="#1d93d4"
    opacity="0.28"
  />

  <!-- Beach / ground -->
  <path d="M0,230 Q350,218 700,230 L700,360 L0,360 Z" fill="url(#p-playa)" />
  <ellipse cx="95"  cy="265" rx="30" ry="10" fill="#6b7c87" opacity="0.5" />
  <ellipse cx="225" cy="278" rx="22" ry="7"  fill="#6b7c87" opacity="0.45" />
  <ellipse cx="440" cy="260" rx="26" ry="9"  fill="#6b7c87" opacity="0.45" />
  <ellipse cx="610" cy="274" rx="32" ry="11" fill="#6b7c87" opacity="0.5" />

  <!-- Floating mattress drifting offshore -->
  <rect x="490" y="218" width="70" height="28" rx="8" fill="#e74c3c" opacity="0.85" />
  <line x1="490" y1="232" x2="560" y2="232" stroke="white" stroke-width="1.2" opacity="0.45" />
  <line x1="525" y1="218" x2="525" y2="246" stroke="white" stroke-width="1.2" opacity="0.45" />
  <!-- Drift arrow -->
  <line x1="568" y1="232" x2="610" y2="232" stroke="#c0392b" stroke-width="2.5" stroke-linecap="round" />
  <polygon points="602,227 612,232 602,237" fill="#c0392b" />

  <!-- Warning sign on beach -->
  <rect x="282" y="148" width="136" height="74" rx="10" fill="white" opacity="0.94" />
  <rect x="282" y="148" width="136" height="74" rx="10" fill="none" stroke="#c0392b" stroke-width="2" />
  <!-- Triangle inside sign -->
  <polygon points="350,163 374,200 326,200" fill="#f39c12" opacity="0.9" />
  <text x="346" y="196" font-family="system-ui,sans-serif" font-size="22" fill="#0a2436" font-weight="900">!</text>
  <!-- Sign pole -->
  <rect x="348" y="222" width="4" height="38" rx="2" fill="#2d3f4b" />

  <!-- Person 1 (standing, observing — safe) -->
  <!-- Left, on beach -->
  <circle cx="140" cy="194" r="10" fill="#1e2e3a" />
  <path d="M140,204 L140,240" stroke="#1e2e3a" stroke-width="5.5" stroke-linecap="round" />
  <path d="M122,218 L140,215 L158,218" stroke="#1e2e3a" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M140,240 L129,264" stroke="#1e2e3a" stroke-width="5" stroke-linecap="round" />
  <path d="M140,240 L151,264" stroke="#1e2e3a" stroke-width="5" stroke-linecap="round" />
  <ellipse cx="142" cy="267" rx="15" ry="5" fill="#1e2e3a" opacity="0.16" />

  <!-- Person 2 (companion standing next to person 1) -->
  <circle cx="175" cy="198" r="9"   fill="#2d3f4b" />
  <path d="M175,207 L175,238" stroke="#2d3f4b" stroke-width="5" stroke-linecap="round" />
  <path d="M160,220 L175,217 L190,220" stroke="#2d3f4b" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M175,238 L165,260" stroke="#2d3f4b" stroke-width="4.5" stroke-linecap="round" />
  <path d="M175,238 L185,260" stroke="#2d3f4b" stroke-width="4.5" stroke-linecap="round" />
  <ellipse cx="177" cy="263" rx="13" ry="4.5" fill="#1e2e3a" opacity="0.14" />

  <!-- Cold water temp indicator -->
  <rect x="560" y="148" width="120" height="56" rx="10" fill="rgba(10,36,54,0.82)" />
  <text x="572" y="170" font-family="system-ui,sans-serif" font-size="12" fill="#8fd3ff" font-weight="700">AGUA FRÍA</text>
  <text x="572" y="190" font-family="system-ui,sans-serif" font-size="12" fill="#d4e5f1">~ 9–13 °C</text>
  <line x1="620" y1="204" x2="620" y2="228" stroke="#8fd3ff" stroke-width="1.8" stroke-dasharray="4,3" opacity="0.55" />
</svg>