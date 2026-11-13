# 內在旅程冊 9:16 文字層產生器（PAUSE SPACE）
# 用法：python3 journey_kit.py spec.json out/
# 產出每頁 1080x1920 透明／紙底 PNG，上傳 Canva 疊在插圖上（每次 update_fill 後補 crop_media 0,0,1080,1920）
import json, math, os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF = os.path.join(HERE, 'NotoSerifTC[wght].ttf')
FONT_URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/notoseriftc/NotoSerifTC%5Bwght%5D.ttf'
if not os.path.exists(SERIF):  # 字型已附在 repo；萬一不見才從 google/fonts 抓
    urllib.request.urlretrieve(FONT_URL, SERIF)

W, H = 1080, 1920
PAPER, INK, GREY, RED = (239, 235, 228), (40, 36, 32), (120, 114, 106), (190, 52, 40)
LINE = (122, 140, 132)
THIN = {400: 230, 500: 200, 600: 300}          # 島主要的「細」字重
N = 12

def serif(size, wght=400):
    f = ImageFont.truetype(SERIF, size)
    try: f.set_variation_by_axes([THIN.get(wght, wght)])
    except Exception: pass
    return f

class P:
    def __init__(s, no, hole=None, clear=False):
        s.im = Image.new('RGBA', (W, H), PAPER + (0 if clear else 255,))
        if hole: x, y, w, h = hole; s.im.paste((0, 0, 0, 0), (x, y, x + w, y + h))
        s.d = ImageDraw.Draw(s.im); s.no = no
    def header(s):
        s.sp(64, 70, 'PAUSE SPACE  ／  INNER JOURNEY', serif(17, 500), 4, GREY)
        t = 'No.%02d ／ %d' % (s.no, N); f = serif(17, 500)
        s.sp(W - 64 - s.wid(t, f, 4), 70, t, f, 4, GREY)
        s.d.line((64, 104, W - 64, 104), fill=GREY + (110,), width=1)
    def wid(s, t, f, sp): return sum(f.getlength(c) + sp for c in t) - sp
    def sp(s, x, y, t, f, sp=0, fill=INK):
        for c in t: s.d.text((x, y), c, font=f, fill=fill); x += f.getlength(c) + sp
    def lines(s, x, y, txt, f, lh, fill=INK):
        for ln in txt.split('\n'): s.d.text((x, y), ln, font=f, fill=fill); y += lh
        return y
    def foot(s, left, right):
        s.d.line((64, 1800, W - 64, 1800), fill=GREY + (110,), width=1)
        s.sp(64, 1824, left, serif(17, 500), 3, GREY)
        f = serif(17, 500); s.sp(W - 64 - s.wid(right, f, 4), 1824, right, f, 4, GREY)

def veil(p, top, bottom, A=215, fe=220):
    """字後面墊一層紙色霧，往外漸淡（畫在字的下面）"""
    g = Image.new('L', (1, H), 0)
    for y in range(H):
        if top <= y <= bottom: a = A
        elif top - fe < y < top: a = A * ((y - (top - fe)) / fe) ** 1.3
        elif bottom < y < bottom + fe: a = A * (1 - (y - bottom) / fe) ** 1.3
        else: a = 0
        g.putpixel((0, y), int(a))
    lay = Image.new('RGBA', (W, H), PAPER + (0,)); lay.putalpha(g.resize((W, H)))
    p.im = Image.alpha_composite(lay, p.im); p.d = ImageDraw.Draw(p.im)

def chap(p, x, y, label, title, hs=56):
    p.sp(x, y, label, serif(20, 500), 6, RED)
    return p.lines(x, y + 44, title, serif(hs, 500), int(hs * 1.45)) + 16
def body(p, x, y, txt, size=24, lh=42, fill=INK): return p.lines(x, y, txt, serif(size, 400), lh, fill)
def quote(p, x, y, txt, who='— 島主', size=28, lh=44):
    y = p.lines(x, y, txt, serif(size, 500), lh, RED)
    if who: p.sp(x, y + 6, who, serif(18, 400), 2, GREY); y += 36
    return y + 10
def view(p, x, y, txt, w=860):
    p.d.line((x, y, x + w, y), fill=GREY + (120,), width=1)
    p.sp(x, y + 22, 'ANOTHER VIEW　另一個角度', serif(16, 600), 4, RED)
    return p.lines(x, y + 56, txt, serif(22, 400), 40, GREY)

def chapter_block(p, pg, y):
    y = chap(p, 110, y, pg['label'], pg['title'], pg.get('title_size', 56))
    y = body(p, 110, y, pg['body'])
    if pg.get('quote'): y = quote(p, 110, y + 16, pg['quote'])
    if pg.get('view'): y = view(p, 110, y + 8, pg['view'])
    return y

# ---------- 版型 ----------
def cover(pg):  # 插圖放 (0,570,1080,1350)
    p = P(1, (0, 570, W, 1350)); p.header()
    p.sp(110, 150, pg['name'], serif(92, 500), 22, INK)
    p.sp(112, 282, pg['sub'], serif(16, 500), 4, GREY)
    p.d.text((110, 350), pg['line'], font=serif(44, 500), fill=INK)
    p.d.line((110, 450, 170, 450), fill=INK, width=1)
    body(p, 110, 640, pg['intro'], 26, 48)
    veil(p, 570, 640 + 48 * pg['intro'].count('\n') + 60, 150, 120)
    p.foot('島主項項', pg.get('foot', '')); return p

def collage(pg):  # 紙底＋框圖，hole=[x,y,w,h]，字從 text_y 開始
    p = P(pg['no'], tuple(pg['hole'])); p.header()
    chapter_block(p, pg, pg.get('text_y', 870)); p.foot(pg.get('foot', ''), 'p.%02d' % pg['no']); return p

def full_top(pg):  # 滿版插圖，字在上方
    p = P(pg['no'], clear=True); p.header()
    y = chapter_block(p, pg, pg.get('text_y', 180)); veil(p, 0, y + 20, 215, 240)
    veil(p, 1720, 1920, 200, 80); p.foot(pg.get('foot', ''), 'p.%02d' % pg['no']); return p

def full_bottom(pg):  # 滿版插圖，字在下方
    p = P(pg['no'], clear=True)
    y0 = pg.get('text_y', 900); chapter_block(p, pg, y0)
    veil(p, 0, 120, 190, 80); veil(p, y0 - 30, 1920, 205, 140)
    p.header(); p.foot(pg.get('foot', ''), 'p.%02d' % pg['no']); return p

def journey_map(pg):  # stations: [[章, 名, 關鍵字], ...]；剪影另外在 Canva 放
    p = P(pg['no']); p.header()
    p.d.text((610, 170), '旅程地圖', font=serif(56, 500), fill=INK)
    p.sp(612, 252, 'THE JOURNEY MAP', serif(16, 500), 6, GREY)
    p.d.text((612, 284), pg.get('sub', '那天，你走過的章節。'), font=serif(22, 400), fill=GREY)
    st = pg['stations']; n = len(st)
    XL, XR, R = 300, 760, 46; top = 450; step = min(160, (1700 - top) // max(1, n - 1)) if n > 1 else 0
    ys = [top + i * step for i in range(n)]; xs = [XL if i % 2 == 0 else XR for i in range(n)]
    pts = [(XL, 104)]
    for i in range(n):
        pts.append((xs[i], ys[i]))
        if i < n - 1: ym = ys[i] + step / 2; pts += [(xs[i], ym), (xs[i + 1], ym)]
    pts.append((xs[-1], 1780))
    seg = lambda a, b: p.d.line((a, b), fill=LINE, width=3)
    path = [pts[0]]; sg = lambda v: (v > 0) - (v < 0)
    for k in range(1, len(pts) - 1):
        a, b, c = pts[k - 1], pts[k], pts[k + 1]
        if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]): continue
        d1 = (sg(b[0] - a[0]), sg(b[1] - a[1])); d2 = (sg(c[0] - b[0]), sg(c[1] - b[1]))
        s1 = (b[0] - d1[0] * R, b[1] - d1[1] * R); s2 = (b[0] + d2[0] * R, b[1] + d2[1] * R)
        seg(path[-1], s1); cx, cy = s1[0] + d2[0] * R, s1[1] + d2[1] * R
        a0 = math.atan2(s1[1] - cy, s1[0] - cx); a1 = math.atan2(s2[1] - cy, s2[0] - cx)
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        p.d.line([(cx + R * math.cos(a0 + da * t / 20), cy + R * math.sin(a0 + da * t / 20)) for t in range(21)], fill=LINE, width=3, joint='curve')
        path.append(s2)
    seg(path[-1], pts[-1])
    sizes = [40, 50, 44, 58, 54, 62, 64, 58, 48, 52, 46, 56]
    for i, (lab, name, sub) in enumerate(st):
        x, y, r = xs[i], ys[i], sizes[i % len(sizes)]
        p.d.ellipse((x - r, y - r, x + r, y + r), fill=RED)
        nf, sf = serif(30, 400), serif(19, 400); wd = max(nf.getlength(name), sf.getlength(sub))
        tx = x + 96 if x == XL else x - 96 - wd
        p.sp(tx, y - 52, lab, serif(18, 600), 4, RED); p.d.text((tx, y - 24), name, font=nf, fill=INK)
        p.d.text((tx, y + 18), sub, font=sf, fill=GREY)
    p.foot('THE ROAD YOU WALKED.', 'p.%02d' % pg['no']); return p

def integration(pg):  # 整合＋回家功課＋下次見面
    p = P(pg['no']); p.header()
    p.sp(110, 170, 'INTEGRATION　整合', serif(17, 600), 5, RED)
    y = p.lines(110, 214, '這一次，你做了什麼', serif(46, 500), 70)
    y = body(p, 110, y + 10, pg['summary'])
    p.d.line((110, y + 30, 970, y + 30), fill=GREY + (110,), width=1); y += 70
    p.sp(110, y, 'HOMEWORK　回家功課', serif(17, 600), 5, RED)
    p.d.text((110, y + 40), pg['hw_title'], font=serif(52, 500), fill=INK); y += 140
    for step in pg['hw_steps']:
        p.d.ellipse((110, y + 12, 132, y + 34), fill=RED); y = body(p, 150, y, step, 27, 48)
    if pg.get('hw_why'): y = body(p, 110, y + 24, pg['hw_why'], 23, 42, GREY)
    p.d.text((110, y + 24), pg['hw_dates'], font=serif(22, 500), fill=INK); y += 90
    p.d.line((110, y, 970, y), fill=GREY + (110,), width=1)
    p.sp(110, y + 30, 'NEXT　下一次見面', serif(17, 600), 5, RED)
    p.d.text((110, y + 70), pg['next_week'], font=serif(36, 500), fill=RED)
    body(p, 110, y + 136, pg['next_note'], 24, 44)
    p.d.text((W - 64, 1770), '本冊圖像為旅程意象重現，非現場照片', font=serif(15, 400), fill=GREY, anchor='ra')
    p.foot('NEXT JOURNEY, STILL YOU.', 'p.%02d' % pg['no']); return p

LAYOUTS = dict(cover=cover, collage=collage, full_top=full_top, full_bottom=full_bottom, map=journey_map, integration=integration)

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    N = len(spec['pages'])
    for i, pg in enumerate(spec['pages'], 1):
        pg.setdefault('no', i); LAYOUTS[pg['layout']](pg).im.save(os.path.join(out, 'p%02d.png' % i))
    print('ok', N, 'pages →', out)
