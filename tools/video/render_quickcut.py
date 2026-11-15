import numpy as np, cv2, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
W,H,FPS,D=1080,1920,24,43.0
B='/tmp/claude-0/-home-claude/9490c0ee-3ad7-5a04-b5a6-044fa1ccc0ad/scratchpad/vid/n1114/'
REC='/mnt/user-data/uploads/ScreenRecording_11-15-2026_02-45-30_1.mp4'
FONT='/home/claude/pausespace/tools/journey/NotoSerifTC[wght].ttf'
PREVIEW=len(sys.argv)>1
rng=np.random.default_rng(5)
FULL=(170,2622,0,1206); LB=(507,2114,0,990); WIDE=(239,2382,0,1206)
def rec(a,b,crop):
    y0,y1,x0,x1=crop; w,h=x1-x0,(y1-y0)//2*2
    p=subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-to',str(b),'-i',REC,'-vf',f'crop={w}:{h}:{x0}:{y0},fps={FPS}','-pix_fmt','bgr24','-f','rawvideo','-'],capture_output=True)
    fr=np.frombuffer(p.stdout,np.uint8); k=len(fr)//(w*h*3); return list(fr[:k*w*h*3].reshape(k,h,w,3))
def mov(n,a,b,speed=1.0):
    tmp=B+'probe_'+n+'.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-i',B+'src/'+n+'.MOV','-frames:v','1',tmp],check=True)
    h,w=cv2.imread(tmp).shape[:2]
    p=subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-to',str(b),'-i',B+'src/'+n+'.MOV','-vf','scale=%d:%d,fps=%g'%(w,h,FPS*speed),'-pix_fmt','bgr24','-f','rawvideo','-'],capture_output=True)
    fr=np.frombuffer(p.stdout,np.uint8); k=len(fr)//(w*h*3); return list(fr[:k*w*h*3].reshape(k,h,w,3))
# (start,end,src,kf[(u,cx,cy,zoom,rot)],opts)
S=[
 (0.0,1.6,('rec',128.2,130.0,WIDE),[(0,.5,.45,1.05,-2),(1,.52,.40,1.25,1)],{}),
 (1.6,3.0,('img','IMG_2167'),[(0,.45,.45,1.1,-6),(1,.62,.55,1.35,4)],{}),
 (3.0,4.6,('rec',1.0,2.8,FULL),[(0,.45,.40,1.1,0),(1,.52,.36,1.3,-1.5)],{}),
 (4.6,6.3,('rec',12.0,14.6,LB),[(0,.48,.55,1.0,1.5),(1,.52,.48,1.2,-1)],{}),
 (6.3,8.4,('img','IMG_2181'),[(0,.42,.55,2.0,-3),(0.5,.46,.47,1.7,1),(1,.50,.38,1.4,0)],{}),
 (8.4,10.4,('rec',130.0,132.0,FULL),[(0,.5,.40,1.05,0),(1,.46,.34,1.25,-1.5)],{}),
 (10.4,12.3,('rec',132.0,134.6,FULL),[(0,.40,.62,1.15,1),(1,.48,.58,1.3,-1)],{}),
 (12.3,15.9,('rec',172.0,176.2,FULL),[(0,.5,.45,1.05,0),(0.5,.55,.58,1.35,-2),(1,.45,.62,1.6,1)],{}),
 (15.9,18.0,('rec',9.0,11.4,LB),[(0,.5,.5,1.0,-1),(1,.46,.55,1.25,1.5)],{}),
 (18.0,19.4,('img','IMG_2157'),[(0,.55,.35,1.6,-2),(1,.60,.25,1.9,1)],{}),
 (19.4,22.3,('mov','IMG_2180',0,4.4,0.75),[(0,.45,.5,1.0,90),(0.5,.55,.45,1.1,93),(1,.5,.55,1.2,87)],{'step':2}),
 (22.3,24.8,('img','IMG_2182'),[(0,.46,.36,1.55,-2),(0.5,.40,.52,1.5,1.5),(1,.48,.68,1.9,0)],{}),
 (24.8,27.0,('rec',141.0,143.6,FULL),[(0,.45,.60,1.1,1),(1,.55,.55,1.3,-1)],{}),
 (27.0,29.0,('img','IMG_2158'),[(0,.60,.26,1.6,3),(0.5,.55,.32,1.85,-1),(1,.62,.22,2.1,1)],{'step':2}),
 (29.0,31.0,('rec',146.5,148.9,FULL),[(0,.5,.40,1.1,-1),(1,.52,.33,1.35,1)],{}),
 (31.0,33.0,('img','IMG_2169'),[(0,.62,.45,1.15,2),(1,.46,.52,1.3,-2)],{}),
 (33.0,34.6,('img','IMG_2173'),[(0,.55,.45,1.15,-5),(1,.50,.42,1.4,4)],{}),
 (34.6,36.6,('rec',143.6,145.9,FULL),[(0,.5,.55,1.1,1),(1,.45,.50,1.3,-1)],{}),
 (36.6,38.8,('img','IMG_2160'),[(0,.56,.22,1.8,0),(0.5,.50,.30,1.5,-2),(1,.50,.42,1.15,1)],{}),
]
SUBS=[(3.2,7.7,'算命、聽缽、喝酒'),(8.9,12.2,'今夜的台北，你想做什麼？'),(14.1,16.0,'用數字窺探命運'),(16.9,19.5,'用聲音觸碰靈魂'),(20.6,21.9,'再用一杯雞尾酒'),(22.6,24.9,'試試人生的滋味'),(25.9,27.0,'有人想找答案'),(27.0,30.0,'有人只想找個痛快'),(31.7,34.2,'畢竟酒與人生一樣'),(35.0,38.0,'永遠不會剛剛好')]
def catmull(kf,u):
    us=[k[0] for k in kf]; P=np.array([k[1:] for k in kf],float)
    if len(kf)==2: s=u*u*(3-2*u); return P[0]*(1-s)+P[1]*s
    i=max(0,min(len(kf)-2,np.searchsorted(us,u)-1)); u0,u1=us[i],us[i+1]; s=(u-u0)/(u1-u0+1e-9)
    p0=P[max(i-1,0)];p1=P[i];p2=P[i+1];p3=P[min(i+2,len(P)-1)]
    return 0.5*((2*p1)+(-p0+p2)*s+(2*p0-5*p1+4*p2-p3)*s*s+(-p0+3*p1-3*p2+p3)*s**3)
def frame_from(src,cx,cy,z,rot,dx=0,dy=0):
    h,w=src.shape[:2]; a=np.deg2rad(rot); ca,sa=abs(np.cos(a)),abs(np.sin(a))
    ew,eh=w*ca+h*sa,w*sa+h*ca; base=min(ew/9,eh/16); ww=9*base/z; s=W/ww
    hw=ww/2*ca+16*base/z/2*sa; hh=ww/2*sa+16*base/z/2*ca
    cx=float(np.clip(cx*w,min(hw,w/2),max(w-hw,w/2)))+dx; cy=float(np.clip(cy*h,min(hh,h/2),max(h-hh,h/2)))+dy
    M=cv2.getRotationMatrix2D((cx,cy),rot,s); M[0,2]+=W/2-cx; M[1,2]+=H/2-cy
    return cv2.warpAffine(src,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
x=np.linspace(0,1,256)
def scurve(v,k): c=1/(1+np.exp(-k*(v-0.5))); return (c-c[0])/(c[-1]-c[0])
base=scurve(x,6.2)
LUT=np.stack([np.clip(base*0.95+0.02,0,1),np.clip(base*0.97+0.01,0,1),np.clip(base*1.0+0.0,0,1)],1)  # BGR
yy,xx=np.mgrid[0:H,0:W]; vig=(1-0.28*(((xx-W/2)/(W*0.7))**2+((yy-H/2)/(H*0.7))**2)).clip(0.6,1)[...,None].astype(np.float32)
def grade(f):
    f=f.astype(np.float32)/255
    f=f*0.92
    g=f.mean(2,keepdims=True); f=np.clip(g+(f-g)*1.25,0,1)
    idx=(f*255).astype(np.uint8); o=np.stack([LUT[idx[...,c],c] for c in range(3)],2).astype(np.float32)
    lum=o.mean(2,keepdims=True)
    sh=np.clip(1-lum*2.2,0,1); hi=np.clip((lum-0.45)*1.8,0,1)
    o+=sh*np.array([0.10,0.05,-0.025],np.float32)   # teal-blue shadows
    o+=hi*np.array([-0.05,0.005,0.06],np.float32)    # amber highlights
    bloom=cv2.GaussianBlur(np.clip(o-0.7,0,1),(0,0),14)*np.array([0.35,0.6,1.0],np.float32)
    return np.clip(o+bloom*0.6,0,1)
def dirblur(img,L,ang):
    L=int(max(1,L)); k=np.zeros((L*2+1,L*2+1),np.float32); c=L
    dx,dy=np.cos(ang),np.sin(ang)
    for i in range(-L,L+1): k[int(round(c+i*dy)),int(round(c+i*dx))]=1
    k/=k.sum(); return cv2.filter2D(img,-1,k,borderType=cv2.BORDER_REFLECT)
def lighttrails(o,L,ang,amt):
    small=cv2.resize(o,(W//3,H//3)); hl=np.clip(small-0.6,0,1)*2.2
    hl=dirblur(hl,max(2,L//3),ang); hl=cv2.GaussianBlur(hl,(0,0),1.2)
    return cv2.resize(hl,(W,H))*amt
GR=[rng.standard_normal((H//2,W//2)).astype(np.float32) for _ in range(6)]
def font(sz,wt):
    f=ImageFont.truetype(FONT,sz)
    try: f.set_variation_by_axes([wt])
    except Exception: pass
    return f
def text_layer(items):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for (txt,f,y,col,ls) in items:
        ws=[d.textlength(c,font=f) for c in txt]; tw=sum(ws)+ls*(len(txt)-1); xx=(W-tw)/2
        for c,wd in zip(txt,ws): d.text((xx,y),c,font=f,fill=col); xx+=wd+ls
    a=np.asarray(im).astype(np.float32)/255
    sh=cv2.GaussianBlur(a[...,3],(0,0),6)*0.75; al=np.maximum(a[...,3],sh)
    rgb=a[...,:3]*a[...,3:]/np.maximum(al,1e-4)[...,None]
    return np.dstack([rgb[...,::-1],al])
F_SUB=font(58,420); F_T=font(104,320); F_S=font(34,380)
SUBL={t:text_layer([(t,F_SUB,1480,(250,244,232,255),6)]) for a,b,t in SUBS}
TITLE=text_layer([('數字酒夜',F_T,800,(252,246,236,255),30),('11.14 SAT  ·  TAIPEI NIGHT',F_S,955,(255,196,140,255),8)])
logo=Image.open(B+'../../dsys/project/assets/Marks/logo-circle.png').convert('RGBA').resize((520,520),Image.LANCZOS)
OUT=Image.new('RGBA',(W,H),(0,0,0,0)); OUT.paste(logo,((W-520)//2,610),logo)
dd=ImageDraw.Draw(OUT); txt='城市裡的隱藏小島'; f=F_S; ls=10
tw=sum(dd.textlength(c,font=f) for c in txt)+ls*(len(txt)-1); xx=(W-tw)/2
for c in txt: dd.text((xx,1220),c,font=f,fill=(240,230,212,255)); xx+=dd.textlength(c,font=f)+ls
OA=np.asarray(OUT).astype(np.float32)/255; OUTRO=np.dstack([OA[...,:3][...,::-1],OA[...,3]])
def over(o,L,al):
    return o*(1-L[...,3:]*al)+L[...,:3]*L[...,3:]*al
CACHE={}
def src(sh):
    k=str(sh[2])
    if k in CACHE: return CACHE[k]
    CACHE.clear()
    s=sh[2]
    if s[0]=='img': v=cv2.imread(B+'jpg/'+s[1]+'.jpg')
    elif s[0]=='rec': v=rec(s[1],s[2],s[3])
    else: v=mov(s[1],s[2],s[3],s[4])
    CACHE[k]=v; return v
def pose(sh,t):
    s0,s1,_,kf,op=sh; u=np.clip((t-s0)/(s1-s0),0,1); return catmull(kf,u)
NF=int(D*FPS)
frames=range(NF) if not PREVIEW else [int(float(v)*FPS) for v in sys.argv[1].split(',')]
if not PREVIEW:
    ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',B+'mix2.wav','-c:v','libx264','-preset','medium','-crf','21','-maxrate','14M','-bufsize','28M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',B+'out2.mp4'],stdin=subprocess.PIPE)
cuts=[s[0] for s in S[1:]]
for fi in frames:
    t=fi/FPS; sh=next((s for s in S if s[0]<=t<s[1]),None)
    if sh:
        s0,s1,sr,kf,op=sh; step=op.get('step',1)
        tq=s0+((int(round((t-s0)*FPS))//step)*step)/FPS if step>1 else t
        u=(tq-s0)/(s1-s0); v=src(sh)
        im=v[min(len(v)-1,int(u*(len(v)-1)))] if isinstance(v,list) else v
        cx,cy,z,rot=pose(sh,tq)
        # camera velocity for light trails
        c2=pose(sh,tq+1/FPS); vel=np.array([(c2[0]-cx)*W*z,(c2[1]-cy)*H*z]); sp=np.hypot(*vel)
        # whip near cuts
        dcut=min([abs(t-c) for c in cuts]+[9]); whip=max(0,1-dcut/0.17)
        ci=int(np.argmin([abs(t-c) for c in cuts])); wang=[0.35,2.7,-0.4,2.9,0.2,-2.8][ci%6]
        dx=dy=0
        if whip>0:
            sgn=-1 if t<cuts[ci] else 1
            dx=np.cos(wang)*whip*sgn*0.18*im.shape[1]; dy=np.sin(wang)*whip*sgn*0.18*im.shape[0]
        f=frame_from(im,cx,cy,z,rot,dx,dy)
        o=grade(f)
        if whip>0:
            o=dirblur(o,int(whip*90),wang)*1.0
            o=o+lighttrails(o,int(whip*160),wang,0.9*whip)
        ang=np.arctan2(vel[1],vel[0]) if sp>0.5 else 0.6
        o=o+lighttrails(o,int(18+sp*6),ang,0.22)
        if s0==0: o*=min(1,t/0.6)
    else:
        o=np.zeros((H,W,3),np.float32)+np.array([0.09,0.06,0.03],np.float32)
    o=o*vig
    g=cv2.resize(GR[fi%6],(W,H))[...,None]; o=o+g*0.012
    for (a,b,txt) in SUBS:
        if a<=t<b: o=over(o,SUBL[txt],min(1,(t-a)/0.2,(b-t)/0.2))
    if 0.5<=t<2.9: o=over(o,TITLE,min(1,(t-0.5)/0.4,(2.9-t)/0.3))
    if t>=38.8:
        k=min(1,(t-38.8)/0.4); bg=np.array([0.09,0.06,0.03],np.float32)+g*0.012
        o=o*(1-k)+bg*k
        al=np.clip((t-39.2)/0.8,0,1); o=over(o,OUTRO,al); o*=min(1,(D-t)/0.8)
    out=(np.clip(o,0,1)*255).astype(np.uint8)
    if PREVIEW: cv2.imwrite(B+f'p2_{t:05.2f}.jpg',out)
    else: ff.stdin.write(out.tobytes())
if not PREVIEW: ff.stdin.close(); ff.wait()
