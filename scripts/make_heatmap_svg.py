#!/usr/bin/env python3
"""Render an SVG contribution calendar from verified public data, or a labeled placeholder."""
import argparse,json,html
from datetime import date,timedelta
from pathlib import Path

PAL=['#26323c','#325247','#407762','#60a287','#9ad7b9']

def render(source,out):
    file=Path(source)
    data=json.loads(file.read_text(encoding='utf-8')) if file.is_file() else None
    real=bool(data and len(data.get('days',{}))>=250)
    if real:
        days=data['days'];last=max(date.fromisoformat(s) for s in days)
    else:
        days={};last=date.today()
    first=last-timedelta(days=last.weekday()+52*7)
    for d in range(7):
        if first.weekday()==0:break
        first-=timedelta(days=1)
    out_svg=['''<svg xmlns="http://www.w3.org/2000/svg" width="1068" height="255" viewBox="0 0 1068 255" role="img" aria-label="GitHub contribution activity">
<title>Nattt / contributions</title>
<style><![CDATA[
@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.day{opacity:0;animation:rise .38s ease-out forwards}
@media(prefers-reduced-motion:reduce){.day{opacity:1;animation:none}}
]]></style>
<rect width="1068" height="255" rx="9" fill="#10151b"/>
<rect x=".5" y=".5" width="1067" height="254" rx="8.5" stroke="#2a333d" fill="none"/>
<text x="30" y="37" font-family="ui-monospace,Menlo,Consolas,monospace" fill="#dce3eb" font-weight="600" font-size="12" letter-spacing="1">NATTT / CONTRIBUTIONS</text>
<text x="1038" y="37" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace" fill="#8192a4" font-size="11">53 WEEKS</text>
<line x1="30" x2="1038" y1="53" y2="53" stroke="#2a333d"/>''']
    cell=12;gap=6;x0=63;y0=78
    for col in range(53):
        for row in range(7):
            dt=first+timedelta(days=col*7+row)
            if dt>last:continue
            level=days.get(dt.isoformat(),0)
            fill=PAL[level] if real else '#26323c'
            delay=0.18+col*.033+row*.035
            x=x0+col*(cell+gap);y=y0+row*(cell+gap)
            out_svg.append(f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{fill}" style="animation-delay:{delay:.3f}s"><title>{dt.isoformat()}: level {level if real else "not loaded"}</title></rect>')
    out_svg.append('<line x1="30" y1="223" x2="1038" y2="223" stroke="#2a333d"/>')
    if real:
        footer=f'PUBLIC GITHUB DATA / UPDATED {html.escape(data.get("retrieved_at", ""))}'
    else:
        footer='PREVIEW / RUN GITHUB ACTION TO LOAD REAL DATA'
    out_svg.append(f'<text x="30" y="244" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" fill="#8192a4">{footer}</text>')
    out_svg.append('<text x="1038" y="244" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" fill="#9caebe">LESS / MORE</text></svg>')
    dest=Path(out);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('\n'.join(out_svg),encoding='utf-8');print('Wrote',dest,'real_data=',real)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--data',default='data/contributions.json');a.add_argument('--output',default='assets/contributions.svg');args=a.parse_args();render(args.data,args.output)
