#!/usr/bin/env python3
"""Turn a supplied image (or public GitHub avatar) into an animated ASCII SVG.

If neither is supplied, emit a clearly labeled placeholder typography for preview.
"""
import argparse
import html
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont, ImageFilter

DARK_TO_LIGHT = '@%#*+=-:. '
W, H = 67, 43
SVG_WIDTH, SVG_HEIGHT = 490, 550
X, Y, ADV, LINE = 24, 84, 6.6, 10.2


def get_image(source, username, fetch_avatar):
    if source and Path(source).is_file():
        return Image.open(source).convert('RGBA'), f'PHOTO / {Path(source).name.upper()}', False
    if fetch_avatar:
        import requests
        url = f'https://github.com/{username}.png?size=800'
        response = requests.get(url, timeout=25, headers={'User-Agent': 'Nattt-Readme-Generator/1.0'})
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert('RGBA'), 'PHOTO / GITHUB AVATAR', False
    # No pretend portrait: this is only a placeholder that renders from the word NATTT.
    im = Image.new('RGBA', (720, 780), (250, 250, 250, 255))
    draw = ImageDraw.Draw(im)
    for font in ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
                 '/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf']:
        if Path(font).exists():
            font = ImageFont.truetype(font, 152)
            break
    else:
        font = ImageFont.load_default()
    lines = ['NATTT']
    if isinstance(font, ImageFont.FreeTypeFont):
        font = ImageFont.truetype(font.path, 202)
    for j, l in enumerate(lines):
        bb = draw.textbbox((0, 0), l, font=font)
        draw.text(((720-(bb[2]-bb[0]))/2, 310+j*190), l, font=font, fill=(18, 20, 24))
    return im, 'PREVIEW ONLY / REPLACE WITH YOUR PHOTO', True


def make_ascii(image):
    image = ImageOps.exif_transpose(image)
    bg = Image.new('RGBA', image.size, (255,255,255,255))
    image = Image.alpha_composite(bg, image)
    # Use contain rather than crop, preserving head/shoulders from a selfie.
    grayscale = ImageOps.contain(image.convert('L'), (W, H), Image.Resampling.LANCZOS)
    canvas = Image.new('L', (W, H), 255)
    canvas.paste(grayscale, ((W-grayscale.width)//2, (H-grayscale.height)//2))
    canvas = ImageOps.autocontrast(canvas, cutoff=2)
    canvas = ImageEnhance.Contrast(canvas).enhance(1.3)
    # Non-inverted grayscale mapping: background white -> blank.
    rows=[]
    for y in range(H):
        row=[]
        for x in range(W):
            value = canvas.getpixel((x, y))
            idx = round(value/255 * (len(DARK_TO_LIGHT)-1))
            row.append(DARK_TO_LIGHT[idx])
        rows.append(''.join(row).rstrip())
    return rows


def render(source, output, username, fetch_avatar):
    image, origin, is_placeholder = get_image(source, username, fetch_avatar)
    lines=make_ascii(image)
    body=[]
    body.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-label="Animated ASCII portrait for Nattt">
  <title>Nattt / ASCII portrait</title>
  <rect width="490" height="550" rx="9" fill="#10151b"/>
  <rect x="0.5" y="0.5" width="489" height="549" rx="8.5" stroke="#2a333d" fill="none"/>
  <text x="24" y="29" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" font-weight="600" letter-spacing="1.1" fill="#dce3eb">NATTT / PORTRAIT</text>
  <text x="466" y="29" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="9" fill="#708090">01 / 02</text>
  <line x1="24" y1="46" x2="466" y2="46" stroke="#2a333d"/>
  <defs>''')
    for index,_ in enumerate(lines):
        yy=Y+(index*LINE)-LINE*0.85
        start=0.55+index*0.095
        body.append(f'''<clipPath id="reveal-{index}"><rect x="24" y="{yy:.1f}" width="0" height="{LINE+2:.1f}"><animate attributeName="width" from="0" to="446" begin="{start:.2f}s" dur="0.48s" fill="freeze" /></rect></clipPath>''')
    body.append('</defs>')
    for index,row in enumerate(lines):
        yy=Y+(index*LINE)
        # xml:space preserves interior ASCII whitespace exactly.
        body.append(f'<text x="{X}" y="{yy:.1f}" xml:space="preserve" clip-path="url(#reveal-{index})" font-family="DejaVu Sans Mono,Menlo,Consolas,Liberation Mono,monospace" font-size="10.85" fill="#c6d1dc">{html.escape(row)}</text>')
    body.append(f'''<line x1="24" x2="466" y1="503" y2="503" stroke="#2a333d"/>
  <circle cx="28" cy="526" r="3" fill="#83b9ad"/>
  <text x="40" y="530" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="9.5" fill="#8292a3">{html.escape(origin)}</text>
  <text x="465" y="530" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="9" fill="#5e6d7a">{W} × {H} CHARS</text>
</svg>''')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text('\n'.join(body),encoding='utf-8')
    print(f'Wrote {output}  |  source={origin}  |  placeholder={is_placeholder}')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--image', default='',help='Local photo path; preferred over avatar')
    ap.add_argument('--username', default='RahmatHadinata23758051')
    ap.add_argument('--fetch-avatar',action='store_true',help='Download your public GitHub profile image')
    ap.add_argument('--output',default='assets/portrait.svg')
    args=ap.parse_args()
    render(args.image,args.output,args.username,args.fetch_avatar)
