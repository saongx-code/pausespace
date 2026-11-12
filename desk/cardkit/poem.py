"""抓周卡 v3 文字層：下方詩句（關鍵字粗斑駁、其他細字）＋虛線＋大主題字＋手寫落款。輸出 1080x1920 透明 PNG。"""
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
NOTO='/usr/share/fonts/opentype/noto/'
FONTS={'bold':(NOTO+'NotoSerifCJK-Black.ttc',3),'semi':(NOTO+'NotoSerifCJK-Bold.ttc',3),'reg':(NOTO+'NotoSerifCJK-Regular.ttc',3),'hand':(D+'YujiMai-Regular.ttf',0)}
INK=(0x22,0x34,0x5e); W,H=1080,1920; S=2
rng=np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 11)
def F(k,size):
    p,i=FONTS[k]; return ImageFont.truetype(p,size*S,index=i)
def noise(w,h,sc,lo,hi):
    a=rng.random((max(2,h//sc),max(2,w//sc)))
    return lo+(hi-lo)*np.asarray(Image.fromarray((a*255).astype('uint8')).resize((w,h),Image.BICUBIC),dtype=float)/255
def distress(m,amt):
    a=np.asarray(m,dtype=float)/255
    if amt<=0: return a
    h,w=a.shape
    bl=np.asarray(m.filter(ImageFilter.GaussianBlur(1.2*S)),dtype=float)/255
    edge=np.clip((bl+(rng.random((h,w))-0.5)*0.5*amt-0.45)*6,0,1)
    holes=noise(w,h,4*S,0,1)  # 斑駁：少量小缺墨點
    hole=np.clip((holes-(1-0.10*amt))*10,0,1)
    edgezone=np.clip((0.95-bl)*4,0,1)  # 缺墨多出現在筆畫邊緣
    hole=hole*(0.35+0.65*edgezone)
    dens=noise(w,h,30*S,0.75,1.0)
    return np.clip(edge*(1-hole)*dens,0,1)
def run_text(cv,x,y,t,k,size,amt,sp=0):
    f=F(k,size); im=Image.new('L',(W*S,H*S),0); d=ImageDraw.Draw(im); X=x*S
    for ch in t:
        d.text((X,y*S),ch,font=f,fill=255); X+=d.textlength(ch,font=f)+sp*S
    a=distress(im,amt); return np.maximum(cv,a), X/S
def dashes(cv,x0,x1,y,alpha=0.45):
    im=Image.new('L',(W*S,H*S),0); d=ImageDraw.Draw(im); x=x0
    while x<x1:
        seg=rng.choice([6,10,14,3]); gap=rng.choice([8,14,22,30])
        if rng.random()<0.08: d.line([(x*S,(y-5)*S),(x*S,(y+5)*S)],fill=255,width=2*S)
        d.line([(x*S,y*S),((x+seg)*S,y*S)],fill=255,width=2*S); x+=seg+gap
    return np.maximum(cv,np.asarray(im,dtype=float)/255*alpha)
def render(spec,out):
    cv=np.zeros((H*S,W*S))
    for line in spec['lines']:   # [{y, x, runs:[[text,kind,size,amt]]}]
        x=line['x']
        for t,k,size,amt in line['runs']:
            base=line['y']+(line.get('base',0)-size if line.get('base') else 0)
            cv,x=run_text(cv,x,base,t,k,size,amt,line.get('sp',2)); x+=6
    for dl in spec.get('dashes',[]): cv=dashes(cv,*dl)
    A=Image.fromarray((np.clip(cv,0,1)*255).astype('uint8')).resize((W,H),Image.LANCZOS)
    o=Image.new('RGBA',(W,H),INK+(0,)); o.putalpha(A); o.save(out)


# ---------- 自動排版（v3 母版）----------
# spec: {"out":"x.png","title":"你值得自由","lines":[[["自由","b"],["不用一直飛","r"]], ...3–5 行], "seed":7}
# b = 粗斑駁關鍵字（58px），r = 細字（30px）。行會左右錯開、往下排，第一行後和最後一行後各一條淡虛線。
def auto(spec):
    from PIL import Image as I, ImageDraw as DD
    global rng
    rng=np.random.default_rng(spec.get('seed',7))
    cv=np.zeros((H*S,W*S)); d=DD.Draw(I.new('L',(10,10)))
    def width(runs):
        t=0
        for txt,k,size in runs:
            f=F(k,size); t+=sum(d.textlength(c,font=f)+2*S for c in txt)/S+6
        return t-6
    def put(runs,base,x):
        nonlocal cv
        for txt,k,size in runs:
            amt=1.0 if k=='bold' else 0
            cv,x=run_text(cv,x,base-size*1.08,txt,k,size,amt,2); x+=6
    rows=[[(t,'bold' if k=='b' else 'reg',58 if k=='b' else 30) for t,k in ln] for ln in spec['lines']]
    gaps=[78 if any(k=='bold' for _,k,_ in r) else 66 for r in rows]
    if len(rows)>2: gaps[1]+=34  # 第一行後的虛線留空間
    end=1588; ys=[]; y=end
    for g in reversed(gaps): ys.insert(0,y); y-=g
    offs=[-40,-90,-60,-20,-50,10]
    for i,(r,b) in enumerate(zip(rows,ys)):
        x=540-width(r)/2+offs[i%len(offs)]+30; put(r,b,x)
        if i==0 and len(rows)>2: cv=dashes(cv,290,800,b+30)
    cv=dashes(cv,330,770,end+38)
    tsize=spec.get('title_size',120 if len(spec['title'])<=5 else max(80,int(600/len(spec['title']))))
    tr=[(spec['title'],'bold',tsize)]; x=540-width(tr)/2
    cv,_=run_text(cv,x,1790-tsize*1.08,spec['title'],'bold',tsize,1.3,2)
    sg=[('島主項項','hand',56),('｜','reg',28),('精油抓周','reg',26)]; x=540-width(sg)/2
    for txt,k,size in sg:
        cv,x=run_text(cv,x,1876-size*1.08,txt,k,size,0,2); x+=6
    A=I.fromarray((np.clip(cv,0,1)*255).astype('uint8')).resize((W,H),I.LANCZOS)
    o=I.new('RGBA',(W,H),INK+(0,)); o.putalpha(A); o.save(spec['out'])

if __name__=='__main__':
    sp=json.load(open(sys.argv[1]))
    auto(sp) if 'title' in sp else render(sp,sp['out'])
