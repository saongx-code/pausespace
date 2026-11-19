"""自媒體工廠：把封面字放到 9:16 圖上（島主風格手冊「自媒體封面」）
用法：python3 tools/cover/cover.py spec.json
spec：{"img":"底圖.png","out":"成品_1.png","title":"冬季戀歌","sub":"你想問誰的心？","en":"WINTER LOVE SONG｜12.06",
       "style":"film" 或 "hand","pos":"top" 或 "bottom"}
- film：電影海報感，細高的襯線大標題（直排或橫排自動），角落小英文註記
- hand：手寫字（Klee One），白色或米色，配小星星
底圖會自動裁成 1080×1920；字的顏色依底圖亮暗自動選深或淺。
"""
import sys, json, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
W, H = 1080, 1920
NOTO = '/usr/share/fonts/opentype/noto/'


def font(kind, size):
    if kind == 'hand':
        return ImageFont.truetype(os.path.join(REPO, 'desk/cardkit/KleeOne-SemiBold.ttf'), size)
    for name, idx in (('NotoSerifCJK-Light.ttc', 3), ('NotoSerifCJK-Regular.ttc', 3)):
        if os.path.exists(NOTO + name):
            return ImageFont.truetype(NOTO + name, size, index=idx)
    return ImageFont.truetype(os.path.join(REPO, 'tools/journey/NotoSerifTC[wght].ttf'), size)


def fit(im):
    im = ImageOps.exif_transpose(im).convert('RGB')
    return ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, 0.45))


def tone(im, box):
    g = im.crop(box).convert('L').resize((40, 40))
    avg = sum(i * n for i, n in enumerate(g.histogram())) / 1600
    return ((32, 30, 28), (250, 246, 238, 150)) if avg > 150 else ((250, 246, 238), (20, 18, 16, 140))


def shadow_text(base, xy, text, f, fill, glow, anchor='la', spacing=0):
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.multiline_text(xy, text, font=f, fill=glow, anchor=anchor, spacing=spacing, align='center')
    lay = lay.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(lay)
    ImageDraw.Draw(base).multiline_text(xy, text, font=f, fill=fill, anchor=anchor, spacing=spacing, align='center')


def film(im, sp):
    top = sp.get('pos', 'top') != 'bottom'
    y0 = 150 if top else 1400
    ink, glow = tone(im, (100, y0, 980, y0 + 380))
    base = im.convert('RGBA')
    t = sp.get('title', '')
    size = 150 if len(t) <= 4 else 120 if len(t) <= 6 else max(70, int(780 / max(1, len(t))))
    f = font('serif', size)
    shadow_text(base, (W / 2, y0 + size), t, f, ink, glow, anchor='ms')
    if sp.get('sub'):
        shadow_text(base, (W / 2, y0 + size + 90), sp['sub'], font('serif', 46), ink, glow, anchor='ms')
    if sp.get('en'):
        fe = font('serif', 26)
        d = ImageDraw.Draw(base)
        d.text((60, 60), sp['en'], font=fe, fill=ink)
        d.text((W - 60, H - 70), 'PAUSE SPACE', font=fe, fill=ink, anchor='ra')
    return base


def hand(im, sp):
    top = sp.get('pos', 'top') != 'bottom'
    y0 = 170 if top else 1380
    ink, glow = tone(im, (80, y0, 1000, y0 + 400))
    base = im.convert('RGBA')
    t = sp.get('title', '')
    f = font('hand', 120 if len(t) <= 6 else 96)
    # 手寫感：每個字微微上下、旋轉
    x = W / 2 - sum(f.getlength(c) for c in t) / 2
    rnd = random.Random(sp.get('seed', 7))
    for c in t:
        g = Image.new('RGBA', (220, 220), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((110, 110), c, font=f, fill=ink, anchor='mm')
        g = g.rotate(rnd.uniform(-6, 6), resample=Image.BICUBIC)
        base.alpha_composite(g, (int(x + f.getlength(c) / 2 - 110), int(y0 + rnd.uniform(-12, 12))))
        x += f.getlength(c)
    if sp.get('sub'):
        shadow_text(base, (W / 2, y0 + 250), sp['sub'], font('hand', 48), ink, glow, anchor='ms')
    d = ImageDraw.Draw(base)
    for _ in range(5):  # 小星星
        cx, cy = rnd.choice([rnd.randint(80, 260), rnd.randint(820, 1000)]), y0 + rnd.randint(-40, 260)
        r = rnd.randint(10, 18)
        d.line([(cx - r, cy), (cx + r, cy)], fill=ink, width=3)
        d.line([(cx, cy - r), (cx, cy + r)], fill=ink, width=3)
    if sp.get('en'):
        d.text((W / 2, H - 80), sp['en'], font=font('hand', 30), fill=ink, anchor='ms')
    return base


if __name__ == '__main__':
    sp = json.load(open(sys.argv[1], encoding='utf-8'))
    im = fit(Image.open(sp['img']))
    out = (hand if sp.get('style') == 'hand' else film)(im, sp)
    out.convert('RGB').save(sp.get('out', 'cover.png'), quality=92)
    print('已輸出', sp.get('out', 'cover.png'))
