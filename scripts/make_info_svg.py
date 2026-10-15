#!/usr/bin/env python3
"""Create self-contained animated SVG Neofetch-inspired card."""
from pathlib import Path
import html
import argparse


def render(path):
    labels=[
        ('name','Nattt'),
        ('study','Internet Engineering Technology'),
        ('focus','Web development / AI / Security'),
        ('tools','React · TypeScript · Python · Go'),
        ('security','CTF / Reverse engineering'),
        ('website','rblxlabs.vercel.app'),
    ]
    out=['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 550" width="560" height="550" role="img" aria-label="Animated Nattt profile information">
<title>Nattt / profile card</title>
<style><![CDATA[
@keyframes appear { 0% {opacity:0; transform:translateY(7px)} 100% {opacity:1;transform:translateY(0)} }
@keyframes scan { 0%{transform:translateX(-420px)} 100%{transform:translateX(0)} }
@keyframes blink { 50%{opacity:0} }
.row { opacity:0; animation:appear .7s cubic-bezier(.25,.7,.25,1) forwards }
.cursor { animation:blink 1.3s steps(1,end) infinite }
@media (prefers-reduced-motion:reduce) {.row {opacity:1;animation:none} .cursor {animation:none}}
]]></style>
<rect width="560" height="550" rx="9" fill="#10151b"/>
<rect x="0.5" y="0.5" width="559" height="549" rx="8.5" stroke="#2a333d" fill="none"/>
<text x="28" y="30" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" font-weight="600" letter-spacing="1.1" fill="#dce3eb">NATTT / SYSTEM</text>
<text x="532" y="30" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="9" fill="#708090">02 / 02</text>
<line x1="28" y1="46" x2="532" y2="46" stroke="#2a333d"/>
<g class="row" style="animation-delay:.16s">
<text x="28" y="96" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" fill="#83b9ad" letter-spacing="2">PROFILE</text>
<text x="28" y="153" font-family="Arial,Helvetica,sans-serif" font-size="52" font-weight="700" letter-spacing="-2" fill="#edf3f8">Nattt<tspan fill="#83b9ad">.</tspan></text>
<text x="29" y="183" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12" fill="#8b9aab">Internet engineering / developer</text>
</g>
<line x1="28" y1="208" x2="532" y2="208" stroke="#2a333d"/>
''']
    # compact rows (no wrapped content; widths measured for 560 px).
    for i,(key,value) in enumerate(labels):
        y=248+i*36
        delay=.56+i*.15
        out.append(f'''<g class="row" style="animation-delay:{delay:.2f}s"><text x="29" y="{y}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12" fill="#8292a3">{html.escape(key)}</text><text x="161" y="{y}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12" fill="#dce5ef">{html.escape(value)}</text></g>''')
    out.append('''<line x1="28" y1="485" x2="532" y2="485" stroke="#2a333d"/>
<g class="row" style="animation-delay:1.65s"><text x="29" y="519" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="#83b9ad">$</text><text x="48" y="519" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="#8fa2b4">nattt@github:~$</text><rect class="cursor" x="172" y="509" width="6" height="12" fill="#83b9ad"/></g>
</svg>''')
    target=Path(path);target.parent.mkdir(parents=True,exist_ok=True);target.write_text('\n'.join(out),encoding='utf-8');print('Wrote',target)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='assets/info.svg');args=ap.parse_args();render(args.output)
