# Reset／流年等「報告」用：在 journey_kit 上加「純文字頁 text」版型＋自動斷行＋較大內文
# 用法：python3 report_build.py spec.json out/   （spec 格式同 spec_example.json，多一個 layout "text"）
# 封面姓名不要寫進 PNG（name 留空），改在 Canva 用 add_text 加，避免客人姓名進公開 repo
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import journey_kit as K
from PIL import ImageDraw
OUT = sys.argv[2] if len(sys.argv) > 2 else 'out'; os.makedirs(OUT, exist_ok=True)
K.N = 10  # 下面依 spec 頁數覆寫
BS, BL, QS, QL, VS, VL = 31, 56, 33, 54, 26, 46
_b = K.body
K.body = lambda p, x, y, txt, size=BS, lh=BL, fill=K.INK: _b(p, x, y, txt, size, lh, fill)
_q = K.quote
K.quote = lambda p, x, y, txt, who='— 島主', size=QS, lh=QL: _q(p, x, y, txt, who, size, lh)
def _view(p, x, y, txt, w=860):
    p.d.line((x, y, x + w, y), fill=K.GREY + (120,), width=1)
    p.sp(x, y + 22, 'ANOTHER VIEW　另一個角度', K.serif(18, 600), 4, K.RED)
    return p.lines(x, y + 60, txt, K.serif(VS, 400), VL, K.GREY)
K.view = _view

def wrap(txt, size, width=860, wght=400):
    f = K.serif(size, wght); out = []
    for para in txt.split('\n'):
        lines = ['']
        for ch in para:
            cur = lines[-1]
            if f.getlength(cur + ch) > width and cur:
                if ch in '，。、；：！？」』）…':   # 標點不放行首：黏在上一行
                    lines[-1] = cur + ch
                else: lines.append(ch)
            else: lines[-1] = cur + ch
        out += lines
    return '\n'.join(out)

def prep(pg):
    for k, s in (('body', BS), ('view', VS)):
        if pg.get(k): pg[k] = wrap(pg[k], s, 860)
    if pg.get('quote'): pg['quote'] = wrap(pg['quote'], QS, 860, 500)
    return pg

def textpage(pg):
    p = K.P(pg['no']); p.header()
    y = K.chapter_block(p, prep(pg), pg.get('text_y', 170))
    p.foot(pg.get('foot', ''), 'p.%02d' % pg['no']); p.endy = y; return p

spec = json.load(open(sys.argv[1], encoding='utf-8')); K.N = len(spec['pages'])
for i, pg in enumerate(spec['pages'], 1):
    pg['no'] = i; lay = pg['layout']
    if lay == 'text': p = textpage(pg)
    elif lay in ('full_top', 'full_bottom'):
        _cb = K.chapter_block; box = {}
        def cb(p, pg, y): r = _cb(p, pg, y); box['y'] = r; return r
        K.chapter_block = cb; p = getattr(K, lay)(prep(pg)); K.chapter_block = _cb; p.endy = box['y']
    elif lay == 'integration':
        pg['summary'] = wrap(pg['summary'], BS); pg['hw_steps'] = [wrap(s, 27, 820) for s in pg['hw_steps']]
        pg['hw_why'] = wrap(pg['hw_why'], 23); pg['next_note'] = wrap(pg['next_note'], 24); p = K.integration(pg)
    elif lay == 'cover': pg['intro'] = wrap(pg['intro'], 26, 860); p = K.cover(pg)
    else: p = K.LAYOUTS[lay](pg)
    p.im.save(f'{OUT}/p{i:02d}.png'); print(i, lay, getattr(p, 'endy', ''))
