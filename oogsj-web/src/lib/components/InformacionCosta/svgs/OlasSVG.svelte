<svg
  viewBox="0 0 700 360"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label="Ilustración de olas costeras patagónicas"
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
    <linearGradient id="o-roca" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="#8a9ba5" />
      <stop offset="100%" stop-color="#3d5260" />
    </linearGradient>
  </defs>

  <!-- Sky -->
  <rect width="700" height="360" fill="url(#o-sky)" />

  <!-- Clouds -->
  <ellipse cx="115" cy="68" rx="72" ry="17" fill="white" opacity="0.42" />
  <ellipse cx="165" cy="64" rx="52" ry="14" fill="white" opacity="0.36" />
  <ellipse cx="430" cy="52" rx="62" ry="15" fill="white" opacity="0.3" />
  <ellipse cx="488" cy="48" rx="46" ry="13" fill="white" opacity="0.25" />

  <!-- Ocean base -->
  <rect x="0" y="178" width="560" height="182" fill="url(#o-mar)" />

  <!-- Wave 1 — distant -->
  <path
    d="M0,190 C55,173 110,193 165,178 C220,163 275,183 330,168
       C385,153 440,173 495,160 C525,153 545,161 560,156
       L560,360 L0,360 Z"
    fill="#0d6ea8"
    opacity="0.65"
  />

  <!-- Wave 2 — mid -->
  <path
    d="M0,208 C65,188 130,213 195,193 C260,173 325,203 390,183
       C440,168 490,191 540,176
       L540,360 L0,360 Z"
    fill="#1280bc"
    opacity="0.78"
  />

  <!-- Wave 3 — foreground -->
  <path
    d="M0,230 C78,206 155,237 232,213 C308,189 385,226 452,205
       C488,193 515,210 540,203
       L540,360 L0,360 Z"
    fill="#1a93d4"
  />

  <!-- Whitecaps wave 1 -->
  <path d="M62,178 Q98,170 128,177"   stroke="white" stroke-width="2.5" fill="none" opacity="0.55" stroke-linecap="round" />
  <path d="M232,168 Q266,160 296,167" stroke="white" stroke-width="2.5" fill="none" opacity="0.55" stroke-linecap="round" />
  <path d="M378,160 Q408,153 436,160" stroke="white" stroke-width="2"   fill="none" opacity="0.5"  stroke-linecap="round" />

  <!-- Whitecaps wave 2 -->
  <path d="M95,193  Q133,183 168,191" stroke="white" stroke-width="3" fill="none" opacity="0.6" stroke-linecap="round" />
  <path d="M288,181 Q325,171 360,180" stroke="white" stroke-width="3" fill="none" opacity="0.6" stroke-linecap="round" />

  <!-- Breaking foam wave 3 -->
  <path d="M108,216 Q152,204 194,214" stroke="white" stroke-width="3.5" fill="none" opacity="0.65" stroke-linecap="round" />
  <path d="M288,206 Q330,194 368,205" stroke="white" stroke-width="3.5" fill="none" opacity="0.65" stroke-linecap="round" />

  <!-- Seafoam near shore -->
  <path d="M395,248 Q430,240 464,247 Q448,258 413,255 Z" fill="white" opacity="0.3" />
  <path d="M322,260 Q360,252 396,258 Q378,268 342,265 Z" fill="white" opacity="0.25" />

  <!-- Rocky Patagonian shore (right) -->
  <path
    d="M538,112 L555,93 L570,110 L584,88 L598,106 L613,83
       L630,100 L648,78 L666,95 L684,76 L700,90
       L700,360 L538,360 Z"
    fill="url(#o-roca)"
  />
  <!-- Rock layer mid -->
  <path
    d="M538,152 L558,138 L576,153 L593,133 L610,148 L628,128
       L646,146 L666,130 L686,146 L700,136
       L700,202 L538,202 Z"
    fill="#546a79"
    opacity="0.62"
  />
  <!-- Rock lower shadow -->
  <path
    d="M538,202 L558,194 L583,207 L608,197 L636,211 L665,200 L700,208
       L700,242 L538,242 Z"
    fill="#3d5260"
    opacity="0.48"
  />

  <!-- Water on rocks -->
  <path d="M510,226 Q524,216 540,222 Q530,208 514,216 Z" fill="white" opacity="0.45" />
  <path d="M503,240 Q516,231 527,236 Q519,223 505,230 Z" fill="white" opacity="0.38" />
</svg>