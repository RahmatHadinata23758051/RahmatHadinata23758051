#!/usr/bin/env python3
"""Minimal kinetic-type outro, self-contained SVG for GitHub's image renderer."""
from pathlib import Path
from html import escape
import argparse
import math

W,H=1068,224
MONO='ui-monospace,Menlo,Consolas,Liberation Mono,monospace'

def build(output):
    out=[f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Nattt animated footer signature">
<title>Nattt / end of file</title>
<style><![CDATA[
@keyframes flow{{ from{{stroke-dashoffset:540}}to{{stroke-dashoffset:0}} }}
@keyframes fadeup{{from{{opacity:0;transform:translateY(9px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes flicker{{0%,84%,100%{{opacity:.21}} 88%,93%{{opacity:1}}}}
@keyframes nudge{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(14px)}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:.15}}}}
.path{{stroke-dasharray:8 24;animation:flow 18s linear infinite}}
.label{{opacity:0;animation:fadeup 1s ease-out forwards}}
.dot{{animation:flicker 7s step-end infinite}}
.nudge{{animation:nudge 6s ease-in-out infinite}}.cursor{{animation:blink 1.35s steps(1,end) infinite}}
@media(prefers-reduced-motion:reduce){{.path,.label,.dot,.nudge,.cursor{{animation:none}}.label{{opacity:1}}}}
]]></style>
<defs>
  <linearGradient id="word" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0f6fa"/><stop offset="1" stop-color="#869bab"/></linearGradient>
  <clipPath id="clip"><rect x="28" y="45" width="1011" height="131"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="9" fill="#10151b"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8.5" stroke="#2a333d" fill="none"/>
<text x="32" y="29" font-family="{MONO}" font-size="10.5" font-weight="600" letter-spacing="1.4" fill="#a8b8c6">NATTT / SIGNATURE</text>
<text x="1035" y="29" font-family="{MONO}" font-size="10" text-anchor="end" letter-spacing="1" fill="#8195a5">END OF FILE</text>
<line x1="31" y1="43" x2="1036" y2="43" stroke="#2a333d"/>
<g clip-path="url(#clip)">''']
    # restrained wire/ASCII field, inspired by monospaced artwork not stock waves
    for k in range(7):
        yy= 70+k*17
        pts=[]
        for x in range(590,1038,12):
            offset=7.5*math.sin((x-580)*.017 + k*.7)+2.5*math.sin((x-580)*.051+k*1.2)
            pts.append((x,yy+offset))
        path='M '+ ' L '.join(f'{x},{y:.1f}' for x,y in pts)
        out.append(f'<path d="{path}" class="path" stroke="#83b9ad" stroke-opacity="{.16+(6-k)*.045:.3f}" stroke-width="1.05" fill="none" style="animation-delay:-{k*1.4:.1f}s"/>')
    for i in range(33):
        x=620+i*13.2
        y=86 + 48*math.sin(i*.39)**2
        out.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{1.05 if i%3 else 1.6}" fill="#b9dacf" style="animation-delay:-{(i*.47):.2f}s"/>')
    out.extend(['</g>',
    '<g class="label" style="animation-delay:.15s"><text x="28" y="148" font-family="Inter,Arial,Helvetica,sans-serif" font-size="108" font-weight="800" letter-spacing="-7" fill="url(#word)">Nattt<tspan fill="#83b9ad">.</tspan></text></g>',
    '<line x1="31" y1="183" x2="1036" y2="183" stroke="#2a333d"/>',
    f'<text x="31" y="207" font-family="{MONO}" font-size="10.8" fill="#8c9daa">RAHMAT HADINATA</text>',
    f'<text x="435" y="207" font-family="{MONO}" font-size="10" fill="#738797">INTERNET ENGINEERING TECHNOLOGY</text>',
    f'<text x="1035" y="207" text-anchor="end" font-family="{MONO}" font-size="10.8" fill="#a6c9c0">EOF <tspan class="cursor">▌</tspan></text>',
    '</svg>'])
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(out),encoding='utf-8');print('Wrote',p)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='assets/footer.svg');a=p.parse_args();build(a.output)
