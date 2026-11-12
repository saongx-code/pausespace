"""Render a 1080x1920 transparent overlay: retro-print title + handwritten 落款 + slashes."""
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os; D=os.path.dirname(os.path.abspath(__file__))+'/'
SERIF='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
HAND=D+'KleeOne-SemiBold.ttf'
INK=(0x22,0x34,0x5e)
W,H=1080,1920; S=2  # supersample
rng=np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 7)

def smooth_noise(w,h,scale,lo,hi):
    a=rng.random((max(2,h//scale),max(2,w//scale)))
    n=np.asarray(Image.fromarray((a*255).astype('uint8')).resize((w,h),Image.BICUBIC),dtype=float)/255
    return lo+(hi-lo)*n

def glyph_mask(ch,font,size,rot):
    f=ImageFont.truetype(font,size*S, index=3 if font.endswith('.ttc') else 0)
    b=f.getbbox(ch); pad=size*S//4
    im=Image.new('L',(b[2]-b[0]+2*pad,b[3]-b[1]+2*pad),0)
    ImageDraw.Draw(im).text((pad-b[0],pad-b[1]),ch,font=f,fill=255)
    return im.rotate(rot,resample=Image.BICUBIC,expand=True)

def distress(m, strength=1.0):
    a=np.asarray(m,dtype=float)/255; h,w=a.shape
    # rough edges: blur + grain then re-threshold
    bl=np.asarray(m.filter(ImageFilter.GaussianBlur(1.6*S)),dtype=float)/255
    grain=rng.random((h,w))
    edge=np.clip((bl+ (grain-0.5)*0.55*strength -0.45)*6,0,1)
    # uneven ink density (low-freq) + fine speckle holes
    dens=smooth_noise(w,h,22*S,0.62,1.0)
    holes=(rng.random((h,w))>0.035*strength).astype(float)
    holes=np.asarray(Image.fromarray((holes*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6)),dtype=float)/255
    return np.clip(edge*dens*(0.7+0.3*holes),0,1)

def paste(canvas,alpha,x,y):
    h,w=alpha.shape; X,Y=x*S,y*S
    sub=canvas[Y:Y+h,X:X+w]; a=alpha[:sub.shape[0],:sub.shape[1]]
    canvas[Y:Y+h,X:X+w]=1-(1-sub)*(1-a)

def render(spec,out):
    cv=np.zeros((H*S,W*S))
    for it in spec['glyphs']:   # {ch,font,size,x,y,rot,ink}
        font=SERIF if it.get('font','serif')=='serif' else HAND
        m=glyph_mask(it['ch'],font,it['size'],it.get('rot',0))
        a=distress(m,it.get('rough',1.0))*it.get('ink',1.0)
        paste(cv,a,it['x'],it['y'])
    for s in spec.get('slashes',[]):  # x1,y1,x2,y2,w
        im=Image.new('L',(W*S,H*S),0)
        ImageDraw.Draw(im).line([(s[0]*S,s[1]*S),(s[2]*S,s[3]*S)],fill=255,width=int(s[4]*S))
        a=distress(im,0.6)*0.9
        cv=1-(1-cv)*(1-a)
    A=Image.fromarray((cv*255).astype('uint8')).resize((W,H),Image.LANCZOS)
    rgba=Image.new('RGBA',(W,H),INK+(0,)); rgba.putalpha(A); rgba.save(out)

if __name__=='__main__':
    spec=json.load(open(sys.argv[1])); render(spec,spec['out'])
