import xml.etree.ElementTree as ET
from PIL import Image, ImageOps, ImageEnhance

# 1. Process profile photo
img = Image.open(r"D:\berkas\profile.jpeg")
# Crop top 900x1080 (5:6 aspect ratio)
crop = img.crop((0, 0, 900, 1080)).resize((300, 360), Image.Resampling.LANCZOS)
gray = ImageOps.grayscale(crop)

gray_dark = ImageEnhance.Contrast(gray).enhance(1.4)
gray_dark = ImageEnhance.Sharpness(gray_dark).enhance(1.3)
dithered_dark = gray_dark.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
pixels_dark = dithered_dark.load()

gray_light = ImageEnhance.Contrast(gray).enhance(1.2)
gray_light = ImageEnhance.Sharpness(gray_light).enhance(1.2)
dithered_light = gray_light.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
pixels_light = dithered_light.load()

# Dither paths for Dark mode
runs_dark = []
for y in range(360):
    in_run = False
    run_start = 0
    for x in range(300):
        if pixels_dark[x, y] == 255:
            if not in_run:
                in_run = True
                run_start = x
        else:
            if in_run:
                runs_dark.append(f"M{run_start} {y}h{x - run_start}v1h-{x - run_start}z")
                in_run = False
    if in_run:
        runs_dark.append(f"M{run_start} {y}h{300 - run_start}v1h-{300 - run_start}z")

dark_path_d = "".join(runs_dark)

# Dither paths for Light mode
runs_light = []
for y in range(360):
    in_run = False
    run_start = 0
    for x in range(300):
        if pixels_light[x, y] == 0:
            if not in_run:
                in_run = True
                run_start = x
        else:
            if in_run:
                runs_light.append(f"M{run_start} {y}h{x - run_start}v1h-{x - run_start}z")
                in_run = False
    if in_run:
        runs_light.append(f"M{run_start} {y}h{300 - run_start}v1h-{300 - run_start}z")

light_path_d = "".join(runs_light)

py_blue = "M49.6 1.5c-12.7 0-21.8 5.6-21.8 16.4v12.2h22.2v3.1H20.7C9.3 33.2 0 42.5 0 54c0 11.4 9.6 20.3 20.7 20.3h7.2v-9.8c0-11.8 9.9-21.4 21.7-21.4h22.2V30.5c0-10.8-9.1-16.4-21.8-16.4h-.4zm-11.8 8.6c2.4 0 4.3 1.9 4.3 4.3 0 2.4-1.9 4.3-4.3 4.3-2.4 0-4.3-1.9-4.3-4.3 0-2.4 1.9-4.3 4.3-4.3z"
py_yellow = "M50.4 98.5c12.7 0 21.8-5.6 21.8-16.4V69.9H50V66.8h29.3c11.4 0 20.7-9.3 20.7-20.8 0-11.4-9.6-20.3-20.7-20.3h-7.2v9.8c0 11.8-9.9 21.4-21.7 21.4H28.2v12.6c0 10.8 9.1 16.4 21.8 16.4h.4zm11.8-8.6c-2.4 0-4.3-1.9-4.3-4.3 0-2.4 1.9-4.3 4.3-4.3 2.4 0 4.3 1.9 4.3 4.3 0 2.4-1.9 4.3-4.3 4.3z"

def build_slides_dark():
    return f'''
    <!-- SLIDE 1: PROFILE PHOTO -->
    <g id="slide-photo">
      <animate attributeName="opacity" values="1;1;0;0;0;0;0;1" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#0B0F17" stroke="#22D3EE" stroke-width="1.5" stroke-dasharray="8 4" opacity="0.6"/>
      <g fill="url(#avatar-glow)" opacity="0.95">
        <path d="{dark_path_d}"/>
      </g>
      <rect x="20" y="325" width="260" height="26" rx="6" fill="#030712" fill-opacity="0.85" stroke="#22D3EE" stroke-width="1"/>
      <text x="150" y="342" text-anchor="middle" fill="#22D3EE" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="2">FAHMI IDRIS</text>
    </g>

    <!-- SLIDE 2: JAVASCRIPT LOGO -->
    <g id="slide-js">
      <animate attributeName="opacity" values="0;0;1;1;0;0;0;0" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#0F172A" fill-opacity="0.95" stroke="#F7DF1E" stroke-width="1.5" stroke-opacity="0.8"/>
      <path d="M20 20h260v320h-260z" fill="none" stroke="#F7DF1E" stroke-width="0.5" stroke-opacity="0.2" stroke-dasharray="4 4"/>
      
      <g transform="translate(85, 45)">
        <rect x="0" y="0" width="130" height="130" rx="18" fill="#F7DF1E"/>
        <text x="110" y="112" text-anchor="end" fill="#000000" font-family="Arial, Helvetica, sans-serif" font-weight="900" font-size="78">JS</text>
      </g>
      
      <text x="150" y="215" text-anchor="middle" fill="#F7DF1E" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="800" letter-spacing="2">JAVASCRIPT</text>
      <text x="150" y="242" text-anchor="middle" fill="#E2E8F0" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600">TypeScript &#8226; Node.js</text>
      <text x="150" y="265" text-anchor="middle" fill="#94A3B8" font-family="'JetBrains Mono', monospace" font-size="11">Modern Full-Stack Ecosystem</text>
      
      <rect x="40" y="295" width="220" height="26" rx="6" fill="#030712" stroke="#F7DF1E" stroke-width="1" stroke-opacity="0.6"/>
      <text x="150" y="312" text-anchor="middle" fill="#F7DF1E" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="1.5">&#9670; TECH STACK 01 &#9670;</text>
    </g>

    <!-- SLIDE 3: PYTHON LOGO -->
    <g id="slide-py">
      <animate attributeName="opacity" values="0;0;0;0;1;1;0;0" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#0F172A" fill-opacity="0.95" stroke="#38BDF8" stroke-width="1.5" stroke-opacity="0.8"/>
      <path d="M20 20h260v320h-260z" fill="none" stroke="#38BDF8" stroke-width="0.5" stroke-opacity="0.2" stroke-dasharray="4 4"/>
      
      <g transform="translate(90, 45) scale(1.2)">
        <path d="{py_blue}" fill="#38BDF8"/>
        <path d="{py_yellow}" fill="#FACC15"/>
      </g>
      
      <text x="150" y="215" text-anchor="middle" fill="#38BDF8" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="800" letter-spacing="2">PYTHON</text>
      <text x="150" y="242" text-anchor="middle" fill="#E2E8F0" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600">Automation &#8226; Scripting</text>
      <text x="150" y="265" text-anchor="middle" fill="#94A3B8" font-family="'JetBrains Mono', monospace" font-size="11">Data Engineering &#8226; AI Backend</text>
      
      <rect x="40" y="295" width="220" height="26" rx="6" fill="#030712" stroke="#38BDF8" stroke-width="1" stroke-opacity="0.6"/>
      <text x="150" y="312" text-anchor="middle" fill="#38BDF8" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="1.5">&#9670; TECH STACK 02 &#9670;</text>
    </g>

    <!-- SLIDE 4: REACT LOGO -->
    <g id="slide-react">
      <animate attributeName="opacity" values="0;0;0;0;0;0;1;1" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#0F172A" fill-opacity="0.95" stroke="#61DAFB" stroke-width="1.5" stroke-opacity="0.8"/>
      <path d="M20 20h260v320h-260z" fill="none" stroke="#61DAFB" stroke-width="0.5" stroke-opacity="0.2" stroke-dasharray="4 4"/>
      
      <g transform="translate(150, 110)">
        <circle cx="0" cy="0" r="13" fill="#61DAFB"/>
        <g>
          <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/>
          <ellipse cx="0" cy="0" rx="55" ry="21" fill="none" stroke="#61DAFB" stroke-width="4.5" opacity="0.9"/>
          <ellipse cx="0" cy="0" rx="55" ry="21" fill="none" stroke="#61DAFB" stroke-width="4.5" opacity="0.9" transform="rotate(60)"/>
          <ellipse cx="0" cy="0" rx="55" ry="21" fill="none" stroke="#61DAFB" stroke-width="4.5" opacity="0.9" transform="rotate(120)"/>
        </g>
      </g>
      
      <text x="150" y="215" text-anchor="middle" fill="#61DAFB" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="800" letter-spacing="2">REACT.JS</text>
      <text x="150" y="242" text-anchor="middle" fill="#E2E8F0" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600">Next.js &#8226; Tailwind CSS</text>
      <text x="150" y="265" text-anchor="middle" fill="#94A3B8" font-family="'JetBrains Mono', monospace" font-size="11">Interactive UI &#8226; Web Apps</text>
      
      <rect x="40" y="295" width="220" height="26" rx="6" fill="#030712" stroke="#61DAFB" stroke-width="1" stroke-opacity="0.6"/>
      <text x="150" y="312" text-anchor="middle" fill="#61DAFB" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="1.5">&#9670; TECH STACK 03 &#9670;</text>
    </g>
'''

def build_slides_light():
    return f'''
    <!-- SLIDE 1: PROFILE PHOTO -->
    <g id="slide-photo">
      <animate attributeName="opacity" values="1;1;0;0;0;0;0;1" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.5" stroke-dasharray="8 4" opacity="0.6"/>
      <g fill="url(#avatar-glow)" opacity="0.95">
        <path d="{light_path_d}"/>
      </g>
      <rect x="20" y="325" width="260" height="26" rx="6" fill="#FFFFFF" fill-opacity="0.9" stroke="#0284C7" stroke-width="1"/>
      <text x="150" y="342" text-anchor="middle" fill="#0284C7" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="2">FAHMI IDRIS</text>
    </g>

    <!-- SLIDE 2: JAVASCRIPT LOGO -->
    <g id="slide-js">
      <animate attributeName="opacity" values="0;0;1;1;0;0;0;0" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#FFFFFF" fill-opacity="0.95" stroke="#EAB308" stroke-width="1.5" stroke-opacity="0.8"/>
      <path d="M20 20h260v320h-260z" fill="none" stroke="#EAB308" stroke-width="0.5" stroke-opacity="0.2" stroke-dasharray="4 4"/>
      
      <g transform="translate(85, 45)">
        <rect x="0" y="0" width="130" height="130" rx="18" fill="#F7DF1E"/>
        <text x="110" y="112" text-anchor="end" fill="#000000" font-family="Arial, Helvetica, sans-serif" font-weight="900" font-size="78">JS</text>
      </g>
      
      <text x="150" y="215" text-anchor="middle" fill="#CA8A04" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="800" letter-spacing="2">JAVASCRIPT</text>
      <text x="150" y="242" text-anchor="middle" fill="#1E293B" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600">TypeScript &#8226; Node.js</text>
      <text x="150" y="265" text-anchor="middle" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="11">Modern Full-Stack Ecosystem</text>
      
      <rect x="40" y="295" width="220" height="26" rx="6" fill="#FEFCE8" stroke="#CA8A04" stroke-width="1" stroke-opacity="0.6"/>
      <text x="150" y="312" text-anchor="middle" fill="#CA8A04" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="1.5">&#9670; TECH STACK 01 &#9670;</text>
    </g>

    <!-- SLIDE 3: PYTHON LOGO -->
    <g id="slide-py">
      <animate attributeName="opacity" values="0;0;0;0;1;1;0;0" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#FFFFFF" fill-opacity="0.95" stroke="#0284C7" stroke-width="1.5" stroke-opacity="0.8"/>
      <path d="M20 20h260v320h-260z" fill="none" stroke="#0284C7" stroke-width="0.5" stroke-opacity="0.2" stroke-dasharray="4 4"/>
      
      <g transform="translate(90, 45) scale(1.2)">
        <path d="{py_blue}" fill="#0284C7"/>
        <path d="{py_yellow}" fill="#EAB308"/>
      </g>
      
      <text x="150" y="215" text-anchor="middle" fill="#0284C7" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="800" letter-spacing="2">PYTHON</text>
      <text x="150" y="242" text-anchor="middle" fill="#1E293B" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600">Automation &#8226; Scripting</text>
      <text x="150" y="265" text-anchor="middle" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="11">Data Engineering &#8226; AI Backend</text>
      
      <rect x="40" y="295" width="220" height="26" rx="6" fill="#F0F9FF" stroke="#0284C7" stroke-width="1" stroke-opacity="0.6"/>
      <text x="150" y="312" text-anchor="middle" fill="#0284C7" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="1.5">&#9670; TECH STACK 02 &#9670;</text>
    </g>

    <!-- SLIDE 4: REACT LOGO -->
    <g id="slide-react">
      <animate attributeName="opacity" values="0;0;0;0;0;0;1;1" keyTimes="0;0.22;0.25;0.47;0.50;0.72;0.75;1" dur="16s" repeatCount="indefinite"/>
      <rect x="0" y="0" width="300" height="360" rx="10" fill="#FFFFFF" fill-opacity="0.95" stroke="#0284C7" stroke-width="1.5" stroke-opacity="0.8"/>
      <path d="M20 20h260v320h-260z" fill="none" stroke="#0284C7" stroke-width="0.5" stroke-opacity="0.2" stroke-dasharray="4 4"/>
      
      <g transform="translate(150, 110)">
        <circle cx="0" cy="0" r="13" fill="#0284C7"/>
        <g>
          <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/>
          <ellipse cx="0" cy="0" rx="55" ry="21" fill="none" stroke="#0284C7" stroke-width="4.5" opacity="0.9"/>
          <ellipse cx="0" cy="0" rx="55" ry="21" fill="none" stroke="#0284C7" stroke-width="4.5" opacity="0.9" transform="rotate(60)"/>
          <ellipse cx="0" cy="0" rx="55" ry="21" fill="none" stroke="#0284C7" stroke-width="4.5" opacity="0.9" transform="rotate(120)"/>
        </g>
      </g>
      
      <text x="150" y="215" text-anchor="middle" fill="#0284C7" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="800" letter-spacing="2">REACT.JS</text>
      <text x="150" y="242" text-anchor="middle" fill="#1E293B" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600">Next.js &#8226; Tailwind CSS</text>
      <text x="150" y="265" text-anchor="middle" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="11">Interactive UI &#8226; Web Apps</text>
      
      <rect x="40" y="295" width="220" height="26" rx="6" fill="#F0F9FF" stroke="#0284C7" stroke-width="1" stroke-opacity="0.6"/>
      <text x="150" y="312" text-anchor="middle" fill="#0284C7" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="1.5">&#9670; TECH STACK 03 &#9670;</text>
    </g>
'''

dark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="100%" height="100%">
<defs>
<linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#030712"/>
<stop offset="50%" stop-color="#0B0F17"/>
<stop offset="100%" stop-color="#0F172A"/>
</linearGradient>
<linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#22D3EE"/>
<stop offset="50%" stop-color="#818CF8"/>
<stop offset="100%" stop-color="#C084FC"/>
</linearGradient>
<linearGradient id="panel-border" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#22D3EE" stop-opacity="0.4"/>
<stop offset="100%" stop-color="#818CF8" stop-opacity="0.1"/>
</linearGradient>
<linearGradient id="avatar-glow" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#22D3EE"/>
<stop offset="100%" stop-color="#F8FAFC"/>
</linearGradient>
<filter id="glow8" x="-50%" y="-50%" width="200%" height="200%">
<feGaussianBlur stdDeviation="8" result="blur"/>
</filter>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
<path d="M 24 0 L 0 0 0 24" fill="none" stroke="rgba(148,163,184,0.04)" stroke-width="1"/>
</pattern>
</defs>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&amp;display=swap');
text {{ font-family: 'JetBrains Mono', monospace; }}
</style>
<rect width="1180" height="610" rx="20" fill="url(#bg)"/>
<rect width="1180" height="610" rx="20" fill="url(#grid)"/>

<!-- LEFT PANEL: SLIDESHOW (PHOTO -> JS -> PYTHON -> REACT) -->
<g>
<rect x="36" y="36" width="390" height="538" rx="14" fill="#0B0F17" fill-opacity="0.8" stroke="url(#panel-border)" stroke-width="1.5"/>
<line x1="36" y1="80" x2="426" y2="80" stroke="rgba(148,163,184,0.12)" stroke-width="1"/>
<circle cx="56" cy="58" r="4.5" fill="#EF4444" opacity="0.8"/>
<circle cx="72" cy="58" r="4.5" fill="#F59E0B" opacity="0.8"/>
<circle cx="88" cy="58" r="4.5" fill="#10B981" opacity="0.8"/>
<text x="231" y="63" font-size="11" fill="#94A3B8" text-anchor="middle" letter-spacing="1">PROFILE // TERMINAL</text>

<!-- Slides Container -->
<g transform="translate(81, 100)">
{build_slides_dark()}
</g>

<!-- Status Indicator -->
<g transform="translate(81, 480)">
  <rect x="0" y="0" width="300" height="34" rx="8" fill="#030712" stroke="#22D3EE" stroke-width="1" stroke-opacity="0.4"/>
  <circle cx="20" cy="17" r="4" fill="#10B981">
    <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="32" y="21" font-size="11" fill="#10B981" font-weight="700">ONLINE</text>
  <text x="85" y="21" font-size="11" fill="#94A3B8">&#8226; Full-Stack Specialist</text>
</g>
</g>

<!-- RIGHT PANEL: METADATA & SPECS -->
<g>
<rect x="442" y="36" width="702" height="538" rx="14" fill="#0B0F17" fill-opacity="0.8" stroke="url(#panel-border)" stroke-width="1.5"/>
<line x1="442" y1="80" x2="1144" y2="80" stroke="rgba(148,163,184,0.12)" stroke-width="1"/>
<text x="470" y="63" font-size="12" fill="#22D3EE" font-weight="600" letter-spacing="1">&gt; SYSTEM.INFO</text>
<text x="1116" y="63" font-size="11" fill="#94A3B8" text-anchor="end">v3.2 // ID: AN_GEOM</text>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.30s" fill="freeze"/><text x="470" y="112" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#94A3B8">- Identification </tspan><tspan fill="rgba(148,163,184,0.35)">---------------------------------------------------------------</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.42s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="0.42s" fill="freeze"/><text x="470" y="135" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Subject </tspan><tspan fill="rgba(148,163,184,0.35)">...........................................</tspan><tspan fill="#F8FAFC" font-weight="700"> Fahmi Idris Anjounghan</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.54s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="0.54s" fill="freeze"/><text x="470" y="158" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Role </tspan><tspan fill="rgba(148,163,184,0.35)">..............................................</tspan><tspan fill="#F8FAFC" font-weight="600"> Full-Stack Developer</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.66s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="0.66s" fill="freeze"/><text x="470" y="181" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Handle </tspan><tspan fill="rgba(148,163,184,0.35)">............................................</tspan><tspan fill="#F8FAFC" font-weight="600"> @angeom21 (AN_GEOM)</tspan></text></g>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.88s" fill="freeze"/><text x="470" y="212" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#94A3B8">- Capabilities &amp; Tooling </tspan><tspan fill="rgba(148,163,184,0.35)">------------------------------------------------------</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.00s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.00s" fill="freeze"/><text x="470" y="235" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">ToolChain </tspan><tspan fill="rgba(148,163,184,0.35)">.................................</tspan><tspan fill="#F8FAFC" font-weight="600"> VS Code, Git, Docker, Linux, Postman</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.12s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.12s" fill="freeze"/><text x="470" y="258" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Core.Lang </tspan><tspan fill="rgba(148,163,184,0.35)">...................................</tspan><tspan fill="#F8FAFC" font-weight="600"> JS, TS, PHP, Python, Shell</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.24s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.24s" fill="freeze"/><text x="470" y="281" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Core.Frontend </tspan><tspan fill="rgba(148,163,184,0.35)">...............................</tspan><tspan fill="#F8FAFC" font-weight="600"> React, Next.js, Tailwind CSS</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.36s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.36s" fill="freeze"/><text x="470" y="304" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Core.Backend </tspan><tspan fill="rgba(148,163,184,0.35)">................................</tspan><tspan fill="#F8FAFC" font-weight="600"> Node.js, Express, Laravel</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.48s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.48s" fill="freeze"/><text x="470" y="327" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Core.Database </tspan><tspan fill="rgba(148,163,184,0.35)">...............................</tspan><tspan fill="#F8FAFC" font-weight="600"> PostgreSQL, MySQL, Redis, MongoDB</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.60s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.60s" fill="freeze"/><text x="470" y="350" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Core.Infra </tspan><tspan fill="rgba(148,163,184,0.35)">..................................</tspan><tspan fill="#F8FAFC" font-weight="600"> Docker, CI/CD, Git, Linux VPS</tspan></text></g>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.82s" fill="freeze"/><text x="470" y="381" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#94A3B8">- Contact &amp; Connect </tspan><tspan fill="rgba(148,163,184,0.35)">-----------------------------------------------------------</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.94s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.94s" fill="freeze"/><text x="470" y="404" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Grid.LinkedIn </tspan><tspan fill="rgba(148,163,184,0.35)">...............................</tspan><tspan fill="#F8FAFC" font-weight="600"> fahmi-idris-anjounghan-023827283</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.06s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="2.06s" fill="freeze"/><text x="470" y="427" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Grid.Telegram </tspan><tspan fill="rgba(148,163,184,0.35)">...............................</tspan><tspan fill="#F8FAFC" font-weight="600"> @angeom21</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.18s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="2.18s" fill="freeze"/><text x="470" y="450" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Grid.GitHub </tspan><tspan fill="rgba(148,163,184,0.35)">.................................</tspan><tspan fill="#F8FAFC" font-weight="600"> @ANGEOM21</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.30s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="2.30s" fill="freeze"/><text x="470" y="473" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#22D3EE">Grid.Status </tspan><tspan fill="rgba(148,163,184,0.35)">.................................</tspan><tspan fill="#F8FAFC" font-weight="600"> Open for Collaboration &amp; Contracts</tspan></text></g>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="2.50s" fill="freeze"/>
<text x="470" y="525" font-size="14" fill="#94A3B8">&#9656; Full portfolio &amp; interactive projects below &#8595; <tspan fill="#22D3EE">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
</g>
</g>
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="3" opacity="0.55" filter="url(#glow8)"/>
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="1.6"/>
</svg>'''

light_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="100%" height="100%">
<defs>
<linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#F8FAFC"/>
<stop offset="50%" stop-color="#F1F5F9"/>
<stop offset="100%" stop-color="#E2E8F0"/>
</linearGradient>
<linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#0284C7"/>
<stop offset="50%" stop-color="#6366F1"/>
<stop offset="100%" stop-color="#9333EA"/>
</linearGradient>
<linearGradient id="panel-border" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#0284C7" stop-opacity="0.5"/>
<stop offset="100%" stop-color="#6366F1" stop-opacity="0.2"/>
</linearGradient>
<linearGradient id="avatar-glow" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#0F172A"/>
<stop offset="100%" stop-color="#334155"/>
</linearGradient>
<filter id="glow8" x="-50%" y="-50%" width="200%" height="200%">
<feGaussianBlur stdDeviation="8" result="blur"/>
</filter>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
<path d="M 24 0 L 0 0 0 24" fill="none" stroke="rgba(15,23,42,0.05)" stroke-width="1"/>
</pattern>
</defs>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&amp;display=swap');
text {{ font-family: 'JetBrains Mono', monospace; }}
</style>
<rect width="1180" height="610" rx="20" fill="url(#bg)"/>
<rect width="1180" height="610" rx="20" fill="url(#grid)"/>

<!-- LEFT PANEL: SLIDESHOW (PHOTO -> JS -> PYTHON -> REACT) -->
<g>
<rect x="36" y="36" width="390" height="538" rx="14" fill="#FFFFFF" fill-opacity="0.9" stroke="url(#panel-border)" stroke-width="1.5"/>
<line x1="36" y1="80" x2="426" y2="80" stroke="rgba(15,23,42,0.08)" stroke-width="1"/>
<circle cx="56" cy="58" r="4.5" fill="#EF4444" opacity="0.8"/>
<circle cx="72" cy="58" r="4.5" fill="#F59E0B" opacity="0.8"/>
<circle cx="88" cy="58" r="4.5" fill="#10B981" opacity="0.8"/>
<text x="231" y="63" font-size="11" fill="#64748B" text-anchor="middle" letter-spacing="1">PROFILE // TERMINAL</text>

<!-- Slides Container -->
<g transform="translate(81, 100)">
{build_slides_light()}
</g>

<!-- Status Indicator -->
<g transform="translate(81, 480)">
  <rect x="0" y="0" width="300" height="34" rx="8" fill="#F0FDF4" stroke="#16A34A" stroke-width="1" stroke-opacity="0.4"/>
  <circle cx="20" cy="17" r="4" fill="#16A34A">
    <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="32" y="21" font-size="11" fill="#16A34A" font-weight="700">ONLINE</text>
  <text x="85" y="21" font-size="11" fill="#475569">&#8226; Full-Stack Specialist</text>
</g>
</g>

<!-- RIGHT PANEL: METADATA & SPECS -->
<g>
<rect x="442" y="36" width="702" height="538" rx="14" fill="#FFFFFF" fill-opacity="0.9" stroke="url(#panel-border)" stroke-width="1.5"/>
<line x1="442" y1="80" x2="1144" y2="80" stroke="rgba(15,23,42,0.08)" stroke-width="1"/>
<text x="470" y="63" font-size="12" fill="#0284C7" font-weight="600" letter-spacing="1">&gt; SYSTEM.INFO</text>
<text x="1116" y="63" font-size="11" fill="#64748B" text-anchor="end">v3.2 // ID: AN_GEOM</text>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.30s" fill="freeze"/><text x="470" y="112" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#64748B">- Identification </tspan><tspan fill="rgba(15,23,42,0.25)">---------------------------------------------------------------</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.42s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="0.42s" fill="freeze"/><text x="470" y="135" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Subject </tspan><tspan fill="rgba(15,23,42,0.25)">...........................................</tspan><tspan fill="#0F172A" font-weight="700"> Fahmi Idris Anjounghan</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.54s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="0.54s" fill="freeze"/><text x="470" y="158" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Role </tspan><tspan fill="rgba(15,23,42,0.25)">..............................................</tspan><tspan fill="#0F172A" font-weight="600"> Full-Stack Developer</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.66s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="0.66s" fill="freeze"/><text x="470" y="181" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Handle </tspan><tspan fill="rgba(15,23,42,0.25)">............................................</tspan><tspan fill="#0F172A" font-weight="600"> @angeom21 (AN_GEOM)</tspan></text></g>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.88s" fill="freeze"/><text x="470" y="212" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#64748B">- Capabilities &amp; Tooling </tspan><tspan fill="rgba(15,23,42,0.25)">------------------------------------------------------</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.00s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.00s" fill="freeze"/><text x="470" y="235" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">ToolChain </tspan><tspan fill="rgba(15,23,42,0.25)">.................................</tspan><tspan fill="#0F172A" font-weight="600"> VS Code, Git, Docker, Linux, Postman</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.12s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.12s" fill="freeze"/><text x="470" y="258" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Core.Lang </tspan><tspan fill="rgba(15,23,42,0.25)">...................................</tspan><tspan fill="#0F172A" font-weight="600"> JS, TS, PHP, Python, Shell</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.24s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.24s" fill="freeze"/><text x="470" y="281" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Core.Frontend </tspan><tspan fill="rgba(15,23,42,0.25)">...............................</tspan><tspan fill="#0F172A" font-weight="600"> React, Next.js, Tailwind CSS</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.36s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.36s" fill="freeze"/><text x="470" y="304" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Core.Backend </tspan><tspan fill="rgba(15,23,42,0.25)">................................</tspan><tspan fill="#0F172A" font-weight="600"> Node.js, Express, Laravel</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.48s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.48s" fill="freeze"/><text x="470" y="327" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Core.Database </tspan><tspan fill="rgba(15,23,42,0.25)">...............................</tspan><tspan fill="#0F172A" font-weight="600"> PostgreSQL, MySQL, Redis, MongoDB</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.60s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.60s" fill="freeze"/><text x="470" y="350" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Core.Infra </tspan><tspan fill="rgba(15,23,42,0.25)">..................................</tspan><tspan fill="#0F172A" font-weight="600"> Docker, CI/CD, Git, Linux VPS</tspan></text></g>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.82s" fill="freeze"/><text x="470" y="381" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#64748B">- Contact &amp; Connect </tspan><tspan fill="rgba(15,23,42,0.25)">-----------------------------------------------------------</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.94s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="1.94s" fill="freeze"/><text x="470" y="404" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Grid.LinkedIn </tspan><tspan fill="rgba(15,23,42,0.25)">...............................</tspan><tspan fill="#0F172A" font-weight="600"> fahmi-idris-anjounghan-023827283</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.06s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="2.06s" fill="freeze"/><text x="470" y="427" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Grid.Telegram </tspan><tspan fill="rgba(15,23,42,0.25)">...............................</tspan><tspan fill="#0F172A" font-weight="600"> @angeom21</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.18s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="2.18s" fill="freeze"/><text x="470" y="450" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Grid.GitHub </tspan><tspan fill="rgba(15,23,42,0.25)">.................................</tspan><tspan fill="#0F172A" font-weight="600"> @ANGEOM21</tspan></text></g>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.30s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="2.30s" fill="freeze"/><text x="470" y="473" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="#0284C7">Grid.Status </tspan><tspan fill="rgba(15,23,42,0.25)">.................................</tspan><tspan fill="#0F172A" font-weight="600"> Open for Collaboration &amp; Contracts</tspan></text></g>

<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="2.50s" fill="freeze"/>
<text x="470" y="525" font-size="14" fill="#64748B">&#9656; Full portfolio &amp; interactive projects below &#8595; <tspan fill="#0284C7">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
</g>
</g>
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="3" opacity="0.55" filter="url(#glow8)"/>
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="1.6"/>
</svg>'''

with open(r"E:\pemograman\GITHUB\angeom21\dark.svg", "w", encoding="utf-8") as f:
    f.write(dark_svg)

with open(r"E:\pemograman\GITHUB\angeom21\light.svg", "w", encoding="utf-8") as f:
    f.write(light_svg)

ET.fromstring(dark_svg)
ET.fromstring(light_svg)
print("SUCCESS: dark.svg and light.svg generated and XML-validated successfully!")
