"""讀流年卡 文字層：讖語（大）＋四季四個建議＋落款。兩色：墨綠＋珊瑚。輸出 1080x1920 透明 PNG。
用法：python3 liunian.py spec.json   spec = {"out","motto":[行1,行2],"tips":[["Q1","東・老鷹","建議"],...],"green":"#1f3d33","coral":"#e8644f"}"""
import sys, json, numpy as np
sys.argv=[sys.argv[0],sys.argv[1],'5']
import poem
from PIL import Image as I
W,H,S=poem.W,poem.H,poem.S
spec=json.load(open(sys.argv[1],encoding='utf8'))
hexc=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))
G=hexc(spec.get('green','#1f3d33')); C=hexc(spec.get('coral','#e8644f'))
g=np.zeros((H*S,W*S)); c=np.zeros((H*S,W*S))
def tw(t,k,size):
    f=poem.F(k,size); return sum(f.getlength(ch) for ch in t)/S
# 讖語：置中，粗宋
y=1050
for i,line in enumerate(spec['motto']):
    sz=min(70,int(860/max(1,len(line))))
    x=(W-tw(line,'bold',sz))/2; g,_=poem.run_text(g,x,y,line,'bold',sz,0.5); y+=int(sz*1.35)
y+=18; c=poem.dashes(c,180,W-180,y,0.9); y+=46
# 四個建議：左欄珊瑚色（季度＋力量動物），右欄墨綠建議
for q,who,tip in spec['tips']:
    c,_=poem.run_text(c,100,y,q,'bold',34,0.3); c,_=poem.run_text(c,100,y+44,who,'semi',26,0.2)
    words=list(tip); line=''; lines=[]
    for ch in words:
        if tw(line+ch,'sans',33)>W-90-290: lines.append(line); line=ch
        else: line+=ch
    lines.append(line); yy=y+4
    for ln in lines: g,_=poem.run_text(g,290,yy,ln,'sans',33,0); yy+=48
    y=max(y+92,yy+18)
# 落款：簽名＋｜讀流年
sig=I.open(poem.SIG).convert('L'); sh=int(70*S); sw=int(sig.width*sh/sig.height); sig=sig.resize((sw,sh),I.LANCZOS)
tag='｜讀流年'; tot=sw/S+10+tw(tag,'sans',30); X=int((W-tot)/2*S); Y=int(max(y+6,1660)*S)
g[Y:Y+sh,X:X+sw]=np.maximum(g[Y:Y+sh,X:X+sw],np.asarray(sig,dtype=float)/255)
g,_=poem.run_text(g,X/S+sw/S+10,Y/S+20,tag,'sans',30,0)
print('bottom y',Y/S+sh/S)
a=np.clip(g+c,0,1); wc=np.where(a>0,c/np.maximum(a,1e-6),0)[...,None]
rgb=(np.array(G)*(1-wc)+np.array(C)*wc)
img=np.dstack([rgb,a*255]).astype('uint8')
I.fromarray(img,'RGBA').resize((W,H),I.LANCZOS).save(spec['out'])
