import math, sys, time, struct, zlib
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline

OUT=Path('/tmp/memoryx-word-atlas23/group-a')
PROOF='--proof' in sys.argv
SCALE=1/4 if PROOF else 1
W,H=int(7200*SCALE),int(3200*SCALE)
K=1120*SCALE
GOLD=np.array([.76,.48,.23])
PEARL=np.array([.78,.78,.73])
LILAC=np.array([.49,.35,.69])
ICE=np.array([.31,.63,.72])
ROSE=np.array([.65,.30,.38])
JADE=np.array([.27,.57,.41])
NAVY=np.array([.17,.21,.34])

def norm(v):return v/np.maximum(np.linalg.norm(v,axis=-1,keepdims=True),1e-9)
LIGHTS=[(norm(np.array([-.5,-.68,.85])),1.05,np.array([1.,.93,.81]),.63),
        (norm(np.array([.7,.1,.58])),.35,np.array([.69,.76,1.]),.3),
        (norm(np.array([.08,.8,.35])),.28,np.array([.91,.58,.68]),.22)]

def png(path,a):
    h,w,c=a.shape
    def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    co=zlib.compressobj(6)
    with open(path,'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6 if c==4 else 2,0,0,0)))
        for row in a:
            x=co.compress(b'\0'+row.tobytes())
            if x:f.write(chunk(b'IDAT',x))
        f.write(chunk(b'IDAT',co.flush()));f.write(chunk(b'IEND',b''))

class Canvas:
    def __init__(self):
        self.a=np.zeros((H,W,4),np.uint8)
        self.z=np.full((H,W),-np.inf,np.float32)
    def point(self,p):return np.array([W/2+p[0]*K,H/2-p[1]*K,p[2]*K])
    def shade(self,n,base,emission=0):
        col=np.ones((len(n),3))*base*np.array([.14,.12,.19])
        for light,power,tint,spec in LIGHTS:
            nd=np.maximum(n@light,0)
            col+=base*nd[:,None]*power*tint
            half=norm(light+np.array([0,0,1.]))
            nh=np.maximum(n@half,0)
            col+=(nh**35)[:,None]*spec*power*tint
            col+=(nh**130)[:,None]*spec*.34*power*tint
        col+=(1-n[:,2:3])**4*np.array([.052,.045,.065])
        col+=emission*base
        col=col/(1+col*.23)
        return (np.clip(col,0,1)**.53*255).astype(np.uint8)
    def segment(self,p0,p1,r,base,emission=0):
        a=self.point(p0);b=self.point(p1);r*=K
        mn=np.floor(np.minimum(a[:2],b[:2])-r-1).astype(int)
        mx=np.ceil(np.maximum(a[:2],b[:2])+r+1).astype(int)
        x0=max(0,mn[0]);x1=min(W,mx[0]);y0=max(0,mn[1]);y1=min(H,mx[1])
        if x1<=x0 or y1<=y0:return
        yy,xx=np.mgrid[y0:y1,x0:x1].astype(np.float32);xx+=.5;yy+=.5
        vx=xx-a[0];vy=yy-a[1]
        d=b-a;l=np.linalg.norm(d)
        if l<1e-8:T=np.array([1.,0,0]);l=.0001
        else:T=d/l
        A=max(1-T[2]**2,1e-7);D=vx*T[0]+vy*T[1]
        B=-2*T[2]*D;C=vx*vx+vy*vy-D*D-r*r
        disc=B*B-4*A*C
        zr=(-B+np.sqrt(np.maximum(disc,0)))/(2*A)
        axial=D+zr*T[2]
        valid=(disc>=0)&(axial>=0)&(axial<=l)
        best=np.where(valid,a[2]+zr,-np.inf)
        nx=(vx-axial*T[0])/r;ny=(vy-axial*T[1])/r;nz=(zr-axial*T[2])/r
        for p in (a,b):
            dx=xx-p[0];dy=yy-p[1];ds=dx*dx+dy*dy
            zz=np.sqrt(np.maximum(r*r-ds,0))
            take=(ds<=r*r)&(p[2]+zz>best)
            best=np.where(take,p[2]+zz,best)
            nx=np.where(take,dx/r,nx);ny=np.where(take,dy/r,ny);nz=np.where(take,zz/r,nz)
        zsub=self.z[y0:y1,x0:x1];mask=best>zsub
        if not mask.any():return
        n=np.stack([nx[mask],ny[mask],nz[mask]],axis=-1)
        n=norm(n)
        col=self.shade(n,base,emission)
        dest=self.a[y0:y1,x0:x1]
        dest[mask,:3]=col;dest[mask,3]=255;zsub[mask]=best[mask]
    def tube(self,points,r,base,emission=0):
        points=np.asarray(points)
        for j in range(len(points)-1):
            self.segment(points[j],points[j+1],r,base,emission)
    def sphere(self,p,r,base,emission=0):self.segment(p,p,r,base,emission)
    def save(self,stem):
        if PROOF:
            rgb=self.a[:,:,:3].copy();alpha=self.a[:,:,3:4].astype(float)/255
            rgb=np.rint(rgb*alpha+np.array([32,26,50])*(1-alpha)).astype(np.uint8)
            png(OUT/(stem+'-proof.png'),rgb)
        else:
            png(OUT/(stem+'.png'),self.a)
            small=self.a.reshape(H//4,4,W//4,4,4).astype(np.float32).mean(axis=(1,3))
            alpha=small[:,:,3:4]/255
            # Premultiplied average already contains edge coverage.
            rgb=np.rint(small[:,:,:3]+np.array([32,26,50])*(1-alpha)).clip(0,255).astype(np.uint8)
            png(OUT/(stem+'-preview.png'),rgb)

def curve(points,n=200):
    p=np.asarray(points,float);t=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))]
    return CubicSpline(t,p,axis=0)(np.linspace(0,t[-1],n))

def arc(cx,cy,rx,ry,z,start=0,end=2*np.pi,n=180,tilt=.25):
    t=np.linspace(start,end,n)
    return np.stack([cx+rx*np.cos(t),cy+ry*np.sin(t),z+tilt*np.sin(t)],axis=-1)

def aporia(c):
    # A heavy circular maze suspended in oblique studio light.
    for i in range(9):
        rr=.30+i*.145
        gap=(i%4)*np.pi/2+.1
        c.tube(arc(-.15,-.05,rr*1.83,rr*.77,-i*.016,gap+.12,gap+2*np.pi-.18,250,tilt=.52),.038,GOLD*(.76+.022*i))
        # Wall at alternating ends makes the route repeatedly reverse.
        t=gap+.12
        if i>0:
            c.tube([[ -.15+(rr-.145)*1.83*np.cos(t),-.05+(rr-.145)*.77*np.sin(t),-i*.016+.52*np.sin(t)],
                    [ -.15+rr*1.83*np.cos(t),-.05+rr*.77*np.sin(t),-i*.016+.52*np.sin(t)]],.039,GOLD)
    c.sphere([-.15,-.05,.09],.12,PEARL)
    # A road from outside enters the maze and ends facing the unreachable core.
    path=curve([[-2.78,-.57,.15],[-2.30,-.39,.11],[-1.75,-.15,.10],[-1.42,.18,.40],[-1.16,.49,.44],[-.52,.50,.39]],200)
    c.tube(path,.024,ICE)
    c.sphere(path[-1],.042,ICE,.25)
    for k in range(9):
        rr=.34+k*.26
        c.tube(arc(-.15,-.05,rr,rr*.42,-.8,.1,2*np.pi+.1,120,tilt=.12),.0035,NAVY)

def apophasis(c):
    # Negative center enclosed by a staggered family of open crescents.
    for i in range(15):
        rr=.57+i*.044
        start=.22+.045*i;end=2*np.pi-.22-.036*i
        cx=(i-7)*.047
        p=arc(cx,0,rr*1.78,rr*.92,-i*.026,start,end,220,tilt=.28)
        col=LILAC*(.68+.024*i)
        c.tube(p,.0275,col)
        # Thin warm metal lip makes each omission tactile.
        c.tube(p[:20],.010,GOLD)
    # Two detached pieces make a refusal, rather than a complete contour.
    c.tube(arc(.16,0,1.23*1.78,1.23*.92,.18,-.39,.14,90,.28),.035,PEARL)
    c.tube(arc(-.16,0,1.32*1.78,1.32*.92,.04,np.pi-.20,np.pi+.20,70,.28),.022,GOLD)
    for r in (.67,.73,.79):
        c.tube(arc(0,0,r*1.58,r*.79,-1,0,2*np.pi,180,.15),.004,LILAC*.4)

def anagnorisis(c):
    # The pearl is visible through one peeled side of a fragmented shell.
    c.sphere([.23,.05,-.02],.66,PEARL)
    for i in range(16):
        rr=.74+i*.035
        start=.42+.028*i;end=2*np.pi-.75-.052*i
        p=arc(-.18-.027*i,-.025,rr*1.65,rr*.94,.14-i*.010,start,end,240,.28)
        c.tube(p,.034,NAVY*(1.16+.025*i))
        c.tube(p[:14],.014,GOLD)
    # Floating curved fragments radiate along the route of recognition.
    for i,(x,y) in enumerate([(1.61,.54),(2.09,.32),(2.53,.08)]):
        p=curve([[x-.12,y-.29,.25],[x+.04,y-.15,.31],[x+.11,y+.03,.30],[x+.12,y+.24,.21]],90)
        c.tube(p,.065-i*.009,GOLD*(1-i*.05))
    c.tube(arc(.23,.05,.74,.74,.1,-1.5,1.35,180,.20),.010,GOLD)

def anacoluthon(c):
    p=curve([[-2.76,-.35,0],[-2.34,-.34,.06],[-1.96,.38,.18],[-1.49,.67,.24],[-1.06,.38,.22],[-.65,-.12,.13],[-.27,-.10,.15]],340)
    c.tube(p,.13,ICE)
    q=curve([[.39,.72,.12],[.83,.72,.02],[1.18,.36,-.02],[1.17,-.36,.06],[1.55,-.72,.19],[2.15,-.62,.24],[2.75,-.30,.26]],330)
    c.tube(q,.094,GOLD)
    # The ghost of the expected continuation remains visibly unfulfilled.
    for i in range(8):
        x=.02+i*.16
        c.tube([[x,-.10,-.5],[x+.055,-.10,-.5]],.0055,ICE*.42)

def anastomosis(c):
    # Four major pathways repeatedly bifurcate and reunite.
    strands=[]
    for band in range(4):
        base_y=(band-1.5)*.52
        t=np.linspace(-2.75,2.75,330)
        y=base_y+.10*np.sin(t*2.1+band*.65)
        z=.08*np.sin(t*1.6+band)
        p=np.stack([t,y,z],axis=-1);strands.append(p)
        c.tube(p,.06+(.014 if band in (1,2) else 0),ROSE*(.71+band*.10))
    for band in range(3):
        for j in range(4):
            x=-2.10+j*1.30+band*.15
            y0=(band-1.5)*.52+.10*np.sin(x*2.1+band*.65)
            xe=x+.74
            y1=(band+1-1.5)*.52+.10*np.sin(xe*2.1+(band+1)*.65)
            p=curve([[x,y0,.08],[x+.18,y0+.04,.12],[x+.44,y1-.04,.17],[xe,y1,.09]],110)
            c.tube(p,.038,ROSE*(1.10 if (j+band)%2 else .94))
            for node in (p[0],p[-1]):c.sphere(node,.075,ROSE)
    # One pale route can be traced through the vascular weave.
    p=curve([[-2.73,-.71,.12],[-2.14,-.72,.18],[-1.77,-.41,.25],[-.94,-.30,.28],[-.60,.05,.31],[.40,.30,.27],[.75,.65,.3],[1.84,.81,.24],[2.74,.70,.2]],360)
    c.tube(p,.019,PEARL)

def apophenia(c):
    rng=np.random.default_rng(541093)
    pts=np.column_stack([rng.uniform(-2.85,2.85,115),rng.uniform(-1.12,1.12,115),rng.uniform(-.3,.05,115)])
    for p in pts:
        c.sphere(p,float(rng.uniform(.009,.026)),LILAC*.76)
    selected=np.array([[-2.2,-.25,.2],[-1.70,.72,.28],[-1.05,.34,.3],[-.52,-.48,.22],[.0,.39,.25],[.62,.76,.3],[.97,-.04,.25],[1.70,-.62,.2],[2.31,.35,.3]])
    pairs=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(2,4),(4,6),(6,8)]
    for a,b in pairs:c.tube([selected[a],selected[b]],.008,GOLD*.83)
    for p in selected:
        c.sphere(p,.055,PEARL,.17)
        c.tube(arc(p[0],p[1],.108,.108,p[2]-.07,0,2*np.pi,65,0),.003,GOLD*.58)
    # A number of plausible yet unchosen points share the same material.
    for p in [[-.65,.78,.1],[1.82,.68,.15],[-1.3,-.78,.17],[.25,-.83,.16]]:c.sphere(p,.036,PEARL*.74)

def autopoiesis(c):
    # Ribbed semipermeable membrane, open enough to expose production cycles.
    for j in range(26):
        t=2*np.pi*j/26
        x=2.1*np.cos(t);y=.86*np.sin(t);z=.28*np.sin(t)
        # boundary made from discontinuous curved structural components
        p=arc(0,0,2.10,.86,0,t+.018,t+2*np.pi/26-.018,32,.28)
        c.tube(p,.047,JADE*(.85+.15*np.sin(t)**2))
        c.sphere([x,y,z],.065,PEARL*.73)
    for rr in (1.0,1.05,1.10):
        c.tube(arc(0,0,2.10*rr,.86*rr,-.15,0,2*np.pi,300,.26),.011,JADE*.53)
    # Three nested catalytic loops and six links to the membrane.
    for cx,cy,r in [(-.92,.18,.35),(.03,-.18,.43),(.98,.22,.31)]:
        t=np.linspace(0,2*np.pi,240)
        p=np.stack([cx+r*1.3*np.cos(t),cy+r*.8*np.sin(t),.20+.23*np.sin(2*t)],axis=-1)
        c.tube(p,.043,JADE*1.3)
        c.sphere([cx,cy,.35],.11,GOLD)
        for i in range(5):
            a=i*2*np.pi/5
            c.sphere([cx+r*.54*np.cos(a),cy+r*.34*np.sin(a),.22],.026,PEARL)
    routes=[([[-.92,.46,.22],[-1.23,.62,.19],[-1.68,.51,.13]]),
            ([[-.92,-.07,.24],[-1.26,-.38,.1],[-1.62,-.54,-.1]]),
            ([[.03,.17,.28],[.1,.51,.23],[.17,.85,.28]]),
            ([[.03,-.52,.18],[.1,-.67,.12],[.34,-.84,-.27]]),
            ([[.98,.45,.28],[1.25,.61,.23],[1.62,.55,.19]]),
            ([[.98,-.03,.27],[1.30,-.30,.2],[1.84,-.42,-.14]])]
    for p in routes:c.tube(curve(p,90),.026,JADE)
    for p in [[[-.5,.18,.12],[-.30,.11,.2],[-.4,-.14,.28]],[[.58,-.18,.25],[.76,-.12,.35],[.61,.17,.24]]]:c.tube(curve(p,75),.030,PEARL*.75)
    for x,y,z in [(-2.55,.58,0),(-2.65,-.20,.1),(2.47,.12,.05),(2.7,-.43,.06)]:c.sphere([x,y,z],.052,JADE)

def chiasmus(c):
    # Two waves reverse their vertical roles at two articulated crossings.
    t=np.linspace(-2.65,2.65,510)
    for sign,base in ((1,ROSE),(-1,ICE)):
        y=sign*.77*np.sin(t*1.28)
        z=sign*.32*np.cos(t*1.28)
        p=np.stack([t,y,z],axis=-1)
        c.tube(p,.105,base)
        # Fine inlaid strands retain their identity through each crossing.
        for off in (-.033,.034):
            q=p.copy();q[:,1]+=off;q[:,2]+=.085
            c.tube(q,.0068,PEARL*.91)
    # Tiny paired terminals emphasize that roles trade places.
    for sign,base in ((1,ROSE),(-1,ICE)):
        for tt in (-2.65,2.65):
            p=[tt,sign*.77*np.sin(tt*1.28),sign*.32*np.cos(tt*1.28)]
            c.sphere(p,.13,base)
    for side in (-1,1):
        c.tube(arc(side*2.43,0,.17,.92,-.6,-np.pi/2,np.pi/2,140,.1),.005,PEARL*.28)

DRAWERS=[aporia,apophasis,anagnorisis,anacoluthon,anastomosis,apophenia,autopoiesis,chiasmus]
indices=[int(x) for x in sys.argv[1:] if x.isdigit()] or list(range(1,9))
for i in indices:
    t=time.time();c=Canvas();DRAWERS[i-1](c);stem=f'{i:02d}-{DRAWERS[i-1].__name__}'
    c.save(stem);print(stem,'done',round(time.time()-t,1),'sec',flush=True)
