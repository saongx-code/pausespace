import struct,sys,subprocess,os,tempfile
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
def boxes(b,s,e):
    while s<e:
        sz,t=struct.unpack('>I4s',b[s:s+8]);h=8
        if sz==1: sz=struct.unpack('>Q',b[s+8:s+16])[0];h=16
        if sz==0: sz=e-s
        yield t.decode('latin1'),s+h,s+sz; s+=sz
def conv(src,dst,maxside=2400):
    b=open(src,'rb').read()
    meta=[x for x in boxes(b,0,len(b)) if x[0]=='meta'][0]
    M={t:(s,e) for t,s,e in boxes(b,meta[1]+4,meta[2])}
    # pitm
    s,e=M['pitm']; v=b[s]; pitm=struct.unpack('>H' if v==0 else '>I',b[s+4:s+6 if v==0 else s+8])[0]
    # iinf
    s,e=M['iinf']; v=b[s]; p=s+4; n=struct.unpack('>H' if v==0 else '>I',b[p:p+(2 if v==0 else 4)])[0]; p+=2 if v==0 else 4
    types={}
    for t,cs,ce in boxes(b,p,e):
        iv=b[cs]; q=cs+4
        if iv>=2:
            iid=struct.unpack('>H' if iv==2 else '>I',b[q:q+(2 if iv==2 else 4)])[0]; q+=(2 if iv==2 else 4)+2
            types[iid]=b[q:q+4].decode('latin1')
    # iloc
    s,e=M['iloc']; v=b[s]; p=s+4
    os_,ls=b[p]>>4,b[p]&15; bs,isz=b[p+1]>>4,b[p+1]&15; p+=2
    rd=lambda n:(int.from_bytes(b[p:p+n],'big') if n else 0)
    cnt=struct.unpack('>H' if v<2 else '>I',b[p:p+(2 if v<2 else 4)])[0]; p+=2 if v<2 else 4
    loc={}
    for _ in range(cnt):
        iid=struct.unpack('>H' if v<2 else '>I',b[p:p+(2 if v<2 else 4)])[0]; p+=2 if v<2 else 4
        cm=0
        if v in(1,2): cm=b[p+1]&15; p+=2
        p+=2 # dref
        base=rd(bs); p+=bs
        ec=struct.unpack('>H',b[p:p+2])[0]; p+=2; ex=[]
        for _ in range(ec):
            if v in(1,2) and isz: p+=isz
            off=rd(os_); p+=os_; ln=rd(ls); p+=ls; ex.append((base+off+(M['idat'][0] if cm==1 else 0),ln))
        loc[iid]=ex
    data=lambda iid:b''.join(b[o:o+l] for o,l in loc[iid])
    # iref
    s,e=M['iref']; v=b[s]; dimg={}
    for t,cs,ce in boxes(b,s+4,e):
        w=2 if v==0 else 4; q=cs
        f=int.from_bytes(b[q:q+w],'big'); q+=w; c=struct.unpack('>H',b[q:q+2])[0]; q+=2
        refs=[int.from_bytes(b[q+i*w:q+i*w+w],'big') for i in range(c)]
        if t=='dimg': dimg[f]=refs
    # iprp
    s,e=M['iprp']; P={t:(cs,ce) for t,cs,ce in boxes(b,s,e)}
    props=list(boxes(b,*P['ipco']))
    s,e=P['ipma']; v=b[s]; fl=int.from_bytes(b[s+1:s+4],'big'); p=s+4
    ec=struct.unpack('>I',b[p:p+4])[0]; p+=4; assoc={}
    for _ in range(ec):
        iid=struct.unpack('>H' if v<1 else '>I',b[p:p+(2 if v<1 else 4)])[0]; p+=2 if v<1 else 4
        c=b[p]; p+=1; L=[]
        for _ in range(c):
            if fl&1: x=struct.unpack('>H',b[p:p+2])[0]&0x7fff; p+=2
            else: x=b[p]&0x7f; p+=1
            L.append(x)
        assoc[iid]=L
    def prop(iid,name):
        for i in assoc.get(iid,[]):
            t,cs,ce=props[i-1]
            if t==name: return cs,ce
    def hvcc(iid):
        cs,ce=prop(iid,'hvcC'); q=cs+22; na=b[q]; q+=1; out=b''
        for _ in range(na):
            q+=1; nn=struct.unpack('>H',b[q:q+2])[0]; q+=2
            for _ in range(nn):
                l=struct.unpack('>H',b[q:q+2])[0]; q+=2; out+=b'\0\0\0\1'+b[q:q+l]; q+=l
        return out
    def annexb(d):
        o=b'';q=0
        while q<len(d):
            l=struct.unpack('>I',d[q:q+4])[0]; o+=b'\0\0\0\1'+d[q+4:q+4+l]; q+=4+l
        return o
    if types[pitm]=='grid':
        g=data(pitm); fl=g[1]; rows,cols=g[2]+1,g[3]+1
        W,H=(struct.unpack('>HH',g[4:8]) if not fl&1 else struct.unpack('>II',g[4:12]))
        tiles=dimg[pitm]
    else:
        tiles=[pitm]; rows=cols=1; W=H=None
    stream=hvcc(tiles[0])+b''.join(annexb(data(t)) for t in tiles)
    td=tempfile.mkdtemp()
    open(td+'/s.hevc','wb').write(stream)
    subprocess.run(['ffmpeg','-v','error','-y','-f','hevc','-i',td+'/s.hevc','-vsync','0',td+'/t%03d.png'],check=True)
    ims=[Image.open(f'{td}/t{i+1:03d}.png') for i in range(len(tiles))]
    tw,th=ims[0].size
    if W is None: W,H=tw,th
    canvas=Image.new('RGB',(tw*cols,th*rows))
    for i,im in enumerate(ims): canvas.paste(im,((i%cols)*tw,(i//cols)*th))
    canvas=canvas.crop((0,0,W,H))
    r=prop(pitm,'irot')
    if r: canvas=canvas.rotate(90*(b[r[0]]&3),expand=True)
    m=prop(pitm,'imir')
    if m: canvas=canvas.transpose(Image.FLIP_TOP_BOTTOM if b[m[0]]&1==0 else Image.FLIP_LEFT_RIGHT)
    canvas.thumbnail((maxside,maxside))
    canvas.save(dst,quality=92)
    return canvas.size
for f in sys.argv[2:]:
    try: print(f,conv(f,os.path.join(sys.argv[1],os.path.basename(f).rsplit('.',1)[0]+'.jpg')))
    except Exception as ex: print(f,'ERR',ex)
