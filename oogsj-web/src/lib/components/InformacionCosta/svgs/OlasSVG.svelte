<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  preserveAspectRatio="xMidYMid meet"
  width="100%"
  height="100%"
  role="img"
  aria-label="Ilustración de olas costeras y corriente de retorno (rip current)"
>
  <defs>
    <linearGradient id="o-sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#cde8f5" />
      <stop offset="100%" stop-color="#96ccec" />
    </linearGradient>
    <linearGradient id="o-mar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a7baa" />
      <stop offset="100%" stop-color="#061826" />
    </linearGradient>
    <linearGradient id="o-arena" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e8d5a3" />
      <stop offset="100%" stop-color="#c9a86a" />
    </linearGradient>
    <linearGradient id="o-roca" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="#8a9ba5" />
      <stop offset="100%" stop-color="#3d5260" />
    </linearGradient>
    <!-- Flecha corriente de retorno (roja, peligro) -->
    <marker id="o-rip" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
      <polygon points="0 0, 10 4, 0 8" fill="#e74c3c" />
    </marker>
    <!-- Flecha alimentadora lateral (naranja) -->
    <marker id="o-feed" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto">
      <polygon points="0 0, 8 3.5, 0 7" fill="#e67e22" />
    </marker>
    <!-- Flecha ola entrante (azul) -->
    <marker id="o-wave" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto">
      <polygon points="0 0, 8 3.5, 0 7" fill="#1a7baa" />
    </marker>
  </defs>

  <!-- Sky -->
  <rect width="700" height="360" fill="url(#o-sky)" />

  <!-- Nubes -->
  <ellipse cx="110" cy="56" rx="70" ry="16" fill="white" opacity="0.40" />
  <ellipse cx="162" cy="52" rx="50" ry="13" fill="white" opacity="0.34" />
  <ellipse cx="440" cy="44" rx="60" ry="14" fill="white" opacity="0.28" />
  <ellipse cx="496" cy="40" rx="44" ry="12" fill="white" opacity="0.24" />

  <!-- Mar fondo -->
  <rect x="0" y="162" width="700" height="198" fill="url(#o-mar)" />

  <!-- ══ OLAS EN LOS FLANCOS (rompen fuerte) ══ -->
  <!-- Ola izquierda — zona de rompiente intensa -->
  <path
    d="M0,175 C38,158 75,178 112,162 C149,146 186,168 223,153
       L223,360 L0,360 Z"
    fill="#0d6ea8" opacity="0.7"
  />
  <path
    d="M0,192 C46,172 92,198 138,178 C176,162 210,186 223,175
       L223,360 L0,360 Z"
    fill="#1280bc" opacity="0.8"
  />
  <!-- Espuma rompiente izquierda -->
  <path d="M28,163 Q64,154 96,162"  stroke="white" stroke-width="3"   fill="none" opacity="0.7" stroke-linecap="round" />
  <path d="M55,178 Q92,168 122,177" stroke="white" stroke-width="3.5" fill="none" opacity="0.65" stroke-linecap="round" />
  <path d="M18,193 Q60,182 98,191"  stroke="white" stroke-width="3"   fill="none" opacity="0.6"  stroke-linecap="round" />

  <!-- Ola derecha — zona de rompiente intensa -->
  <path
    d="M477,175 C514,158 551,178 588,162 C625,146 662,168 700,153
       L700,360 L477,360 Z"
    fill="#0d6ea8" opacity="0.7"
  />
  <path
    d="M477,192 C520,172 562,198 600,178 C638,162 670,186 700,175
       L700,360 L477,360 Z"
    fill="#1280bc" opacity="0.8"
  />
  <!-- Espuma rompiente derecha -->
  <path d="M502,163 Q538,154 568,162"  stroke="white" stroke-width="3"   fill="none" opacity="0.7"  stroke-linecap="round" />
  <path d="M524,178 Q562,168 592,177"  stroke="white" stroke-width="3.5" fill="none" opacity="0.65" stroke-linecap="round" />
  <path d="M495,193 Q538,182 572,191"  stroke="white" stroke-width="3"   fill="none" opacity="0.6"  stroke-linecap="round" />

  <!-- ══ CANAL RIP CURRENT (centro, agua más calma) ══ -->
  <!-- Agua más oscura en el canal (diferente color al resto) -->
  <path
    d="M223,162 C248,155 282,152 350,148 C418,152 452,155 477,162
       L477,360 L223,360 Z"
    fill="#08507a"
  />
  <!-- Sutil diferencia de color del canal vs olas -->
  <path
    d="M240,178 C272,165 310,160 350,158 C390,160 428,165 460,178
       L460,360 L240,360 Z"
    fill="#073e60" opacity="0.6"
  />

  <!-- Olas entrantes (fuera del canal, lejanas) -->
  <path d="M0,166 Q87,155 175,166 Q262,177 350,166 Q438,155 526,166 Q613,177 700,166"
    stroke="#1d93d4" stroke-width="2" fill="none" opacity="0.5" />
  <path d="M0,185 Q87,174 175,185 Q262,196 350,185 Q438,174 526,185 Q613,196 700,185"
    stroke="#1d93d4" stroke-width="1.5" fill="none" opacity="0.35" />

  <!-- ══ PLAYA / ORILLA ══ -->
  <path d="M0,315 Q175,302 350,305 Q525,308 700,315 L700,360 L0,360 Z"
    fill="url(#o-arena)" />
  <!-- Textura orilla húmeda -->
  <path d="M0,322 Q175,312 350,315 Q525,318 700,322 L700,335 Q525,328 350,325 Q175,322 0,332 Z"
    fill="#d4b882" opacity="0.45" />
  <!-- Piedras -->
  <ellipse cx="80"  cy="338" rx="18" ry="6" fill="#b08a55" opacity="0.5" />
  <ellipse cx="200" cy="332" rx="14" ry="5" fill="#b08a55" opacity="0.45" />
  <ellipse cx="480" cy="335" rx="16" ry="5" fill="#b08a55" opacity="0.45" />
  <ellipse cx="620" cy="340" rx="18" ry="6" fill="#b08a55" opacity="0.5" />

  <!-- Rocas patagónicas (extremo derecho) -->
  <path
    d="M648,130 L664,112 L678,130 L692,110 L700,120 L700,360 L648,360 Z"
    fill="url(#o-roca)"
  />

  <!-- ══ FLECHAS RIP CURRENT ══ -->
  <!-- Corriente alimentadora izquierda → centro (naranja) -->
  <path d="M115,272 Q170,265 223,260" stroke="#e67e22" stroke-width="3.5"
    fill="none" stroke-linecap="round" marker-end="url(#o-feed)" stroke-dasharray="8,4" />
  <path d="M88,295 Q160,285 228,278" stroke="#e67e22" stroke-width="3"
    fill="none" stroke-linecap="round" marker-end="url(#o-feed)" stroke-dasharray="7,4" opacity="0.8" />

  <!-- Corriente alimentadora derecha → centro (naranja) -->
  <path d="M585,272 Q530,265 477,260" stroke="#e67e22" stroke-width="3.5"
    fill="none" stroke-linecap="round" marker-end="url(#o-feed)" stroke-dasharray="8,4" />
  <path d="M612,295 Q540,285 472,278" stroke="#e67e22" stroke-width="3"
    fill="none" stroke-linecap="round" marker-end="url(#o-feed)" stroke-dasharray="7,4" opacity="0.8" />

  <!-- Corriente de retorno principal: desde orilla hacia mar abierto (roja, fuerte) -->
  <path d="M350,302 Q350,268 350,232" stroke="#e74c3c" stroke-width="5"
    fill="none" stroke-linecap="round" marker-end="url(#o-rip)" />
  <path d="M350,232 Q350,198 348,175" stroke="#e74c3c" stroke-width="4"
    fill="none" stroke-linecap="round" marker-end="url(#o-rip)" stroke-dasharray="10,5" opacity="0.85" />

  <!-- Flechas secundarias del canal (más sutiles) -->
  <path d="M330,288 Q332,258 332,230" stroke="#e74c3c" stroke-width="2.5"
    fill="none" stroke-linecap="round" marker-end="url(#o-rip)" opacity="0.55" />
  <path d="M370,288 Q368,258 368,230" stroke="#e74c3c" stroke-width="2.5"
    fill="none" stroke-linecap="round" marker-end="url(#o-rip)" opacity="0.55" />

  <!-- ══ ETIQUETAS ══ -->
  <!-- Label corriente de retorno -->
  <rect x="250" y="205" width="200" height="28" rx="8" fill="rgba(231,76,60,0.92)" />
  <text x="268" y="224" font-family="system-ui,sans-serif" font-size="13" fill="white" font-weight="700">⚠ CORRIENTE DE RETORNO</text>

  <!-- Label zona calma del canal -->
  <rect x="264" y="155" width="172" height="22" rx="6" fill="rgba(8,60,90,0.85)" />
  <text x="278" y="171" font-family="system-ui,sans-serif" font-size="11" fill="#8fd3ff" font-weight="600">Canal sin rompiente</text>

  <!-- Label olas laterales -->
  <rect x="20" y="144" width="112" height="20" rx="5" fill="rgba(13,110,168,0.8)" />
  <text x="30" y="159" font-family="system-ui,sans-serif" font-size="10.5" fill="white" font-weight="600">Zona rompiente</text>
  <rect x="568" y="144" width="112" height="20" rx="5" fill="rgba(13,110,168,0.8)" />
  <text x="578" y="159" font-family="system-ui,sans-serif" font-size="10.5" fill="white" font-weight="600">Zona rompiente</text>

  <!-- Label corrientes alimentadoras -->
  <rect x="90" y="248" width="122" height="19" rx="5" fill="rgba(230,126,34,0.85)" />
  <text x="100" y="262" font-family="system-ui,sans-serif" font-size="10" fill="white" font-weight="600">Corriente lateral</text>
  <rect x="488" y="248" width="122" height="19" rx="5" fill="rgba(230,126,34,0.85)" />
  <text x="498" y="262" font-family="system-ui,sans-serif" font-size="10" fill="white" font-weight="600">Corriente lateral</text>

  <!-- Persona en peligro (en el canal) -->
  <circle cx="350" cy="316" r="7"  fill="#1e2e3a" />
  <path d="M350,323 L350,342" stroke="#1e2e3a" stroke-width="4" stroke-linecap="round" />
  <path d="M340,330 L350,328 L360,330" stroke="#1e2e3a" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
</svg>
