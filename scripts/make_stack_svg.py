#!/usr/bin/env python3
"""Editorial animated stack panel. Pure SVG, no network or inline README styles."""
from pathlib import Path
from html import escape
import argparse

W, H = 1068, 335
MONO = 'ui-monospace,Menlo,Consolas,Liberation Mono,monospace'
SANS = 'Inter,Arial,Helvetica,sans-serif'
C = {'bg':'#10151b','border':'#2a333d','primary':'#e8eef4','muted':'#8a9aa9','accent':'#83b9ad','rule':'#26313b'}
ROWS = [
 ('01','FRONTEND','TypeScript   React   Next.js   Tailwind CSS'),
 ('02','BACKEND','Node.js   Python   Laravel   PostgreSQL   Go'),
 ('03','SECURITY','Kali Linux   Burp Suite   Wireshark   Ghidra'),
 ('04','WORKFLOW','Docker   Git   Linux'),
]

def render(output):
    out=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Nattt tech stack: TypeScript, React, Next.js, Tailwind, Node.js, Python, Laravel, PostgreSQL, Go, Kali Linux, Burp Suite, Wireshark, Ghidra, Docker, Git and Linux">
<title>Nattt / toolkit</title>
<style><![CDATA[
@keyframes arrive {{ 0%{{opacity:0;transform:translateY(10px)}} 100%{{opacity:1;transform:translateY(0)}} }}
@keyframes show {{ 0%,9%{{opacity:.17}} 13%,70%{{opacity:1}} 85%,100%{{opacity:.17}} }}
@keyframes travel {{ from{{transform:translateX(-190px)}} to{{transform:translateX(1030px)}} }}
@keyframes cursor {{ 50%{{opacity:.2}} }}
.group{{opacity:0;animation:arrive .7s ease-out forwards}} .pulse{{animation:show 6.5s ease-in-out infinite}} .trace{{animation:travel 9s linear infinite}} .cursor{{animation:cursor 1.35s step-end infinite}}
@media (prefers-reduced-motion:reduce){{.group{{opacity:1;animation:none}}.pulse,.trace,.cursor{{animation:none}}}}
]]></style>
<defs><clipPath id="rail"><rect x="31" y="307" width="1006" height="5"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="9" fill="{C['bg']}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8.5" stroke="{C['border']}" fill="none"/>
<text x="31" y="37" font-family="{MONO}" font-size="12" font-weight="600" letter-spacing="1.1" fill="{C['primary']}">NATTT / TOOLKIT</text>
<text x="1036" y="37" font-family="{MONO}" font-size="10" text-anchor="end" letter-spacing=".7" fill="{C['muted']}">04 / GROUPS</text>
<line x1="31" y1="53" x2="1036" y2="53" stroke="{C['border']}"/>
''']
    for i,(num,name,technologies) in enumerate(ROWS):
        y=98 + i*66
        delay= .15 + i*.24
        out.append(f'''<g class="group" style="animation-delay:{delay:.2f}s">
<text x="31" y="{y}" font-family="{MONO}" font-size="11" fill="{C['accent']}" letter-spacing=".4">{num}</text>
<text x="80" y="{y}" font-family="{MONO}" font-size="12" font-weight="700" fill="{C['primary']}" letter-spacing="1.4">{escape(name)}</text>
<line x1="240" y1="{y-5}" x2="240" y2="{y+5}" stroke="{C['border']}"/>
<text x="265" y="{y+1}" font-family="{SANS}" font-size="19" fill="{C['primary']}" letter-spacing=".1">{escape(technologies)}</text>
<line x1="31" y1="{y+23}" x2="1036" y2="{y+23}" stroke="{C['rule']}" />
</g>''')
    out.extend([f'<line x1="31" y1="309" x2="1036" y2="309" stroke="{C["border"]}" />',
                '<g clip-path="url(#rail)"><rect class="trace" x="31" y="307" width="194" height="3" fill="#83b9ad" opacity=".75"/></g>',
                f'<text x="31" y="329" font-family="{MONO}" font-size="8.5" fill="{C["muted"]}" letter-spacing="1.2">LANGUAGES / FRAMEWORKS / TOOLS</text>',
                f'<text x="1036" y="329" font-family="{MONO}" text-anchor="end" font-size="8.5" fill="{C["accent"]}">ACTIVE STACK <tspan class="cursor">_</tspan></text>',
                '</svg>'])
    dest=Path(output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text('\n'.join(out),encoding='utf-8');print('Wrote',dest)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='assets/stack.svg');a=p.parse_args();render(a.output)
