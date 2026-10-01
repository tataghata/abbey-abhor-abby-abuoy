import os,sys,math,time,struct,zlib
from pathlib import Path
import numpy as np

OUT=Path('/tmp/memoryx-word-atlas23/group-c')
PI=np.pi
def unit(a):return a/np.maximum(np.linalg.norm(a,axis=-1,keepdims=True),1e-15)
def rx(a):return np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
def ry(a):return np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
def rz(a):return np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
def hexcol(s):return np.array([int(s[i:i+2],16) for i in (0,2,4)])/255

def png(path,a):
    h,w,c=a.shape
    def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    z=zlib.compressobj(6)
    with open(path,'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n');f.write(chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6 if c==4 else 2,0,0,0)))
        for row in a:
            b=z.compress(b'\0'+row.tobytes())
            if b:f.write(chunk(b'IDAT',b))
        f.write(chunk(b'IDAT',z.flush()));f.write(chunk(b'IEND',b''))

class Scene:
    def __init__(self,rotation=np.eye(3)):
        self.meshes=[];self.rotation=rotation
    def mesh(self,p,base,rough=.33,metal=.45,normal=None,ao=1):
        p=p@self.rotation.T
        if normal is None:
            du=np.gradient(p,axis=0);dv=np.gradient(p,axis=1)
            n=unit(np.cross(du,dv))
        else:n=unit(normal@self.rotation.T)
        base=np.broadcast_to(np.array(base),p.shape).copy()
        ao=np.broadcast_to(np.asarray(ao),p.shape[:-1])
        self.meshes.append((p,n,base,rough,metal,ao))
    def sphere(self,center,radius,color,scale=(1,1,1),ripples=0):
        u,v=np.meshgrid(np.linspace(.00001,PI-.00001,61),np.linspace(0,2*PI,121),indexing='ij')
        r=radius*(1+ripples*np.cos(18*v)*np.sin(u)**2)
        p=np.stack([r*np.sin(u)*np.cos(v),r*np.cos(u),r*np.sin(u)*np.sin(v)],-1)*scale+center
        self.mesh(p,color,.34,.30,ao=1-abs(ripples)*2*(1-np.cos(18*v))/2)
    def tube(self,path,radius,color,segments=14,rough=.3,metal=.65):
        path=np.asarray(path)
        t=np.gradient(path,axis=0)
        if np.linalg.norm(path[0]-path[-1])<1e-8:
            t[0]=t[-1]=(path[1]-path[-2])/2
        t=unit(t)
        # Use a single stable reference normal for the whole curve. Switching
        # bases near a tangent pole makes circular meshes visibly twist.
        _,eig=np.linalg.eigh(t.T@t)
        ref=np.tile(eig[:,0],(len(t),1))
        bad=np.abs(np.sum(t*ref,axis=1))>.985
        if bad.any():
            candidates=np.eye(3)
            ref[bad]=candidates[np.argmin(np.abs(t[bad]),axis=1)]
        e1=unit(np.cross(t,ref));e2=unit(np.cross(t,e1))
        a=np.linspace(0,2*PI,segments+1)
        nn=e1[:,None,:]*np.cos(a)[None,:,None]+e2[:,None,:]*np.sin(a)[None,:,None]
        rr=np.broadcast_to(np.asarray(radius),len(path))
        self.mesh(path[:,None,:]+rr[:,None,None]*nn,color,rough,metal,normal=nn)
    def torus(self,center,R,r,color,rotation=np.eye(3),wave=0):
        u,v=np.meshgrid(np.linspace(0,2*PI,201),np.linspace(0,2*PI,33),indexing='ij')
        rr=r*(1+.08*np.sin(10*u))
        p=np.stack([(R+rr*np.cos(v))*np.cos(u),(R+rr*np.cos(v))*np.sin(u),rr*np.sin(v)+wave*np.sin(3*u)],-1)
        self.mesh(p@rotation.T+center,color,.25,.55)
    def ribbon(self,path,width,color,twist=.8):
        path=np.asarray(path);t=unit(np.gradient(path,axis=0))
        e1=unit(np.cross(t,np.tile([0.,0.,1.],(len(t),1))));e2=unit(np.cross(t,e1))
        phase=np.linspace(0,twist*2*PI,len(path))
        normal=e1*np.cos(phase)[:,None]+e2*np.sin(phase)[:,None]
        v=np.linspace(-1,1,21)
        p=path[:,None,:]+normal[:,None,:]*v[None,:,None]*width
        self.mesh(p,color,.30,.68)
        for sign in (-1,1):self.tube(path+normal*width*sign,.018,hexcol('F1D7A3'),10)
    def render(self,slug,proof=False):
        W,H=(1800,800) if proof else (7200,3200)
        t0=time.time()
        allp=np.concatenate([p.reshape(-1,3) for p,n,b,r,m,a in self.meshes])
        dist=24.
        projected=allp[:,:2]*(dist/(dist-allp[:,2]))[:,None]
        lo=projected.min(0);hi=projected.max(0)
        sc=min(W*.91/(hi[0]-lo[0]),H*.90/(hi[1]-lo[1]));mid=(lo+hi)/2
        canvas=np.zeros((H,W,4),np.uint8);zb=np.full((H,W),-np.inf,np.float32)
        lights=[(unit(np.array([-.55,.85,1.3])),.96,np.array([1,.92,.82])),(unit(np.array([.8,.15,.85])),.47,np.array([.70,.78,1.])),(unit(np.array([-.2,-.8,.45])),.28,np.array([.89,.61,.93]))]
        for mi,(p,n,base,rough,metal,ao) in enumerate(self.meshes):
            view=unit(np.array([0,0,dist])-p)
            n=np.where(np.sum(n*view,axis=-1,keepdims=True)<0,-n,n)
            color=base*np.array([.16,.12,.20])*ao[:,:,None]
            for light,power,tint in lights:
                nd=np.maximum(np.sum(n*light,axis=-1),0)
                color+=base*nd[:,:,None]*power*tint*ao[:,:,None]
                half=unit(view+light);nh=np.maximum(np.sum(n*half,axis=-1),0)
                spec_color=(1-metal)*tint+metal*(base*.7+tint*.3)
                color+=nh[:,:,None]**(12+70*(1-rough))*power*.48*spec_color
                color+=nh[:,:,None]**(110+200*(1-rough))*power*.50*spec_color
            fres=(1-np.maximum(np.sum(n*view,axis=-1),0))**3
            color+=fres[:,:,None]*np.array([.08,.08,.14])
            color=np.clip(color/(1+color*.16),0,1)**.70*255
            xy=p[:,:,:2]*(dist/(dist-p[:,:,2]))[:,:,None]
            xy=(xy-mid)*sc;xy[:,:,0]+=W/2;xy[:,:,1]=H/2-xy[:,:,1]
            for i in range(p.shape[0]-1):
                for j in range(p.shape[1]-1):
                    for ids in (((i,j),(i+1,j),(i,j+1)),((i+1,j),(i+1,j+1),(i,j+1))):
                        P=np.array([xy[a,b] for a,b in ids]);Z=np.array([p[a,b,2] for a,b in ids]);C=np.array([color[a,b] for a,b in ids])
                        x0=max(0,int(P[:,0].min()));x1=min(W-1,int(P[:,0].max()+1));y0=max(0,int(P[:,1].min()));y1=min(H-1,int(P[:,1].max()+1))
                        if x1<x0 or y1<y0:continue
                        den=(P[1,1]-P[2,1])*(P[0,0]-P[2,0])+(P[2,0]-P[1,0])*(P[0,1]-P[2,1])
                        if abs(den)<1e-10:continue
                        yy,xx=np.ogrid[y0:y1+1,x0:x1+1]
                        a=((P[1,1]-P[2,1])*(xx+.5-P[2,0])+(P[2,0]-P[1,0])*(yy+.5-P[2,1]))/den
                        b=((P[2,1]-P[0,1])*(xx+.5-P[2,0])+(P[0,0]-P[2,0])*(yy+.5-P[2,1]))/den;c=1-a-b
                        z=a*Z[0]+b*Z[1]+c*Z[2]
                        mask=(a>=-1e-6)&(b>=-1e-6)&(c>=-1e-6)&(z>zb[y0:y1+1,x0:x1+1])
                        if not mask.any():continue
                        col=a[:,:,None]*C[0]+b[:,:,None]*C[1]+c[:,:,None]*C[2]
                        dest=canvas[y0:y1+1,x0:x1+1];dest[mask,:3]=np.clip(col[mask],0,255).astype(np.uint8);dest[mask,3]=255
                        zb[y0:y1+1,x0:x1+1][mask]=z[mask]
            if mi%25==0:print(slug,'mesh',mi,'/',len(self.meshes),'elapsed',round(time.time()-t0,1),flush=True)
        if proof:
            a=canvas[:,:,3:4].astype(np.float32)/255
            rgb=canvas[:,:,:3]*a+np.array([32,26,50])*(1-a)
            png(OUT/(slug+'-proof.png'),rgb.astype(np.uint8))
        else:
            png(OUT/(slug+'.png'),canvas)
            # Composite before downsampling for correct antialiasing against the page.
            rgb=np.empty((800,1800,3),np.uint8)
            for y in range(800):
                block=canvas[y*4:y*4+4].astype(np.float32);a=block[:,:,3:4]/255
                col=block[:,:,:3]*a+np.array([32,26,50])*(1-a)
                rgb[y]=np.rint(col.reshape(4,1800,4,3).mean((0,2))).astype(np.uint8)
            png(OUT/(slug+'-preview.png'),rgb)
        print('DONE',slug,W,H,round(time.time()-t0,1),flush=True)

GOLD=hexcol('CDA15E');IVORY=hexcol('DCCDB8');JADE=hexcol('67AAA6');LILAC=hexcol('B08AC5');BLUE=hexcol('7C9FB8')

def rounded_polygon(vertices,rounding=.14,nline=32,ncurve=20):
    vertices=np.array(vertices,dtype=float);out=[]
    for i,b in enumerate(vertices):
        a=vertices[(i-1)%len(vertices)];c=vertices[(i+1)%len(vertices)]
        p=b*(1-rounding)+a*rounding;q=b*(1-rounding)+c*rounding
        t=np.linspace(0,1,ncurve,endpoint=False)[:,None]
        out.extend((1-t)**2*p+2*t*(1-t)*b+t*t*q)
        end=c*(1-rounding)+b*rounding
        t=np.linspace(0,1,nline,endpoint=False)[:,None]
        out.extend(q*(1-t)+end*t)
    return np.vstack([out,out[0]])

def metalepsis():
    s=Scene(rz(-.045)@ry(-.63)@rx(.17))
    for i,x in enumerate((-2.15,0,2.15)):
        contour=rounded_polygon([[x,-1.2,-1.02],[x,-1.2,1.02],[x,1.2,1.02],[x,1.2,-1.02]],.13)
        s.tube(contour,.135,[IVORY,LILAC,BLUE][i],20,.28,.63)
        inset=contour.copy();inset[:,1:]*=.89;inset[:,0]+=.10
        s.tube(inset,.025,GOLD,10)
    t=np.linspace(-3.55,3.55,420)
    path=np.stack([t,.55*np.sin(t*1.55),.49*np.cos(t*1.55)],-1)
    s.ribbon(path,.21,GOLD,.76)
    return s

def palimpsest():
    s=Scene(rz(-.16)@ry(-.23)@rx(.61))
    def page(x,y,z):
        u,v=np.meshgrid(np.linspace(-1.65,1.65,85),np.linspace(-1.18,1.18,61),indexing='ij')
        curl=.11*u*u+.07*v*v+.045*np.sin(u*1.3+v)
        return np.stack([u+x,v+y,curl+z],-1)
    specs=[(-1.5,-.15,-.42,hexcol('7C7896')),(0,0,0,hexcol('AEA4BC')),(1.5,.15,.42,IVORY)]
    for layer,(x,y,z,col) in enumerate(specs):
        p=page(x,y,z);s.mesh(p,col,.56,.10)
        for edge in (p[:,0],p[:,-1],p[0,:],p[-1,:]):s.tube(edge,.018,GOLD,8)
        for row in range(7):
            # Deliberately nonalphabetic traces: this is no fabricated manuscript.
            uu=np.linspace(-1.40,1.40,320)
            vv=-.90+row*.27+.027*np.sin(uu*15+row)+.018*np.sin(uu*31+.7*row)
            zz=.11*uu*uu+.07*vv*vv+.045*np.sin(uu*1.3+vv)+z+.018
            tr=np.stack([uu+x,vv+y,zz],-1)
            color=[hexcol('B8A6B9'),hexcol('676079'),hexcol('91816F')][layer]
            s.tube(tr,.0125,color,6,.62,.04)
            # Intermittent gestural loops give the traces a manuscript rhythm.
            for k in range(7):
                t=np.linspace(0,2*PI,36);cx=-1.18+k*.38
                uu=cx+.045*np.sin(t);vv=-.9+row*.27+.05*(1-np.cos(t))
                zz=.11*uu*uu+.07*vv*vv+.045*np.sin(uu*1.3+vv)+z+.022
                s.tube(np.stack([uu+x,vv+y,zz],-1),.008,color,5,.62,.05)
    return s

def parataxis():
    s=Scene(rz(.015)@rx(.11))
    s.sphere((-3.4,-.05,0),.72,IVORY,scale=(.87,1.18,.9),ripples=.03)
    s.torus((-1.7,-.15,0),.53,.205,JADE,ry(.42))
    # A softly beveled superellipsoid supplies a stable independent block.
    u,v=np.meshgrid(np.linspace(1e-14,PI-1e-14,71),np.linspace(0,2*PI,121),indexing='ij')
    sp=lambda a:np.sign(a)*np.abs(a)**.30
    p=np.stack([sp(np.sin(u))*sp(np.cos(v)),sp(np.cos(u)),sp(np.sin(u))*sp(np.sin(v))],-1)*.66
    s.mesh(p@ry(.3).T+np.array([0,-.24,0]),LILAC,.36,.20)
    u,v=np.meshgrid(np.linspace(-.78,.78,101),np.linspace(0,2*PI,121),indexing='ij')
    r=.36+.13*np.cos(u*4)+.075*np.cos(7*v)*(1-(u/.9)**2)
    p=np.stack([r*np.cos(v)+1.7,u-.12,r*np.sin(v)],-1);s.mesh(p,BLUE,.34,.35)
    # Bowl rims are real closed rings, not a stray exposed mesh boundary.
    for sign in(-1,1):
        v=np.linspace(0,2*PI,181);r=.36+.13*np.cos(.78*4)+.075*np.cos(7*v)*(1-(.78/.9)**2)
        s.tube(np.stack([r*np.cos(v)+1.7,np.full_like(v,sign*.78-.12),r*np.sin(v)],-1),.026,IVORY,10)
    # A cut crystal-like form shares the same visual baseline.
    pts=np.array([[0,.82,0],[.67,0,0],[0,0,.61],[-.67,0,0],[0,0,-.61],[0,-.78,0]])
    faces=[(0,1,2),(0,2,3),(0,3,4),(0,4,1),(5,2,1),(5,3,2),(5,4,3),(5,1,4)]
    for a,b,c in faces:
        pp=np.array([[pts[a],pts[b]],[pts[c],pts[c]]])+np.array([3.4,-.12,0])
        s.mesh(pp,GOLD,.25,.70)
    return s

def quiddity():
    s=Scene(rx(.07))
    path=rounded_polygon([[0,1.13,0],[-1.02,-.78,0],[1.02,-.78,0]],.12,60,35)
    for i,x in enumerate((-2.65,0,2.65)):
        rot=rz([-.08,.04,.10][i])@ry([-.35,.25,.54][i])
        p=path@rot.T+np.array([x,0,0]);s.tube(p,.19,[IVORY,GOLD,JADE][i],32,.28 if i else .45,.75 if i else .10)
        # Fine second contour reads as crafted inlay following the same geometry.
        pp=path*.91;pp[:,2]+=.18
        s.tube(pp@rot.T+np.array([x,0,0]),.017,[GOLD,IVORY,IVORY][i],10)
    return s

def semiosis():
    s=Scene(rx(.10))
    positions=[np.array([-2.25,-.67,0]),np.array([0,1.05,0]),np.array([2.25,-.67,0])]
    # Three directed links, each with an unmistakable but restrained arrowhead.
    for i in range(3):
        a=positions[i];b=positions[(i+1)%3];d=unit(b-a)
        start=a+d*.70;end=b-d*.72
        t=np.linspace(0,1,130);bow=np.cross(d,[0,0,1])*.12
        path=start[None,:]*(1-t[:,None])+end[None,:]*t[:,None]+np.sin(t*PI)[:,None]*bow
        path[:,2]-=.16
        s.tube(path[:-7],.028,GOLD,12)
        tangent=unit(path[-1]-path[-2]);u=np.linspace(0,1,25);v=np.linspace(0,2*PI,25)
        ref=unit(np.cross(tangent,[0,0,1]));side=unit(np.cross(tangent,ref))
        cone=path[-1][None,None,:]-tangent[None,None,:]*u[:,None,None]*.22+(ref[None,None,:]*np.cos(v)[None,:,None]+side[None,None,:]*np.sin(v)[None,:,None])*u[:,None,None]*.10
        s.mesh(cone,GOLD,.3,.6)
    s.sphere(positions[0],.64,IVORY,ripples=.023)
    # A folded triangular signboard and a loop are intentionally unlike the sphere.
    p=rounded_polygon([[0,.57,0],[-.57,-.43,0],[.57,-.43,0]],.11,45,20)+positions[1]
    s.tube(p,.18,BLUE,24,.29,.4)
    s.torus(positions[2],.45,.20,LILAC,ry(.38),wave=.11)
    return s

def synecdoche():
    s=Scene(rz(-.05)@rx(.10))
    center=np.array([-1.15,0,0]);R=1.38
    nt,nv=7,16
    def patch(t0,t1,v0,v1,r=R):
        t,v=np.meshgrid(np.linspace(t0,t1,13),np.linspace(v0,v1,15),indexing='ij')
        return np.stack([r*np.sin(t)*np.cos(v),r*np.cos(t),r*np.sin(t)*np.sin(v)],-1)
    missing=[]
    for i in range(nt):
        for j in range(nv):
            t0=i*PI/nt+.006;t1=(i+1)*PI/nt-.006;v0=j*2*PI/nv+.008;v1=(j+1)*2*PI/nv-.008
            detached=i in (2,3,4) and j in (1,2,3)
            if detached:continue
            p=patch(t0,t1,v0,v1)+center
            col=IVORY*(.85+.12*np.cos(i*1.2+j*.6))+LILAC*.03
            s.mesh(p,col,.40,.30)
            for e in(p[:,0],p[:,-1],p[0],p[-1]):s.tube(e,.009,GOLD,6)
    # Dark inner surface preserves a tangible shell where its face is absent.
    t,v=np.meshgrid(np.linspace(.001,PI-.001,51),np.linspace(0,2*PI,101),indexing='ij')
    p=np.stack([np.sin(t)*np.cos(v),np.cos(t),np.sin(t)*np.sin(v)],-1)*(R-.10)+center
    s.mesh(p,hexcol('504356'),.65,.1)
    t0=2*PI/nt+.004;t1=5*PI/nt-.004;v0=2*PI/nv+.004;v1=4*2*PI/nv-.004
    p=patch(t0,t1,v0,v1)
    centroid=p.reshape(-1,3).mean(0);rot=ry(-.12)@rz(.08)
    shift=np.array([2.05,.18,.2])
    outer=(p-centroid)@rot.T+shift;s.mesh(outer,GOLD,.28,.75)
    inner=((p*(R-.1)/R)-centroid)@rot.T+shift;s.mesh(inner,hexcol('887077'),.44,.25)
    for a,b in zip((outer[:,0],outer[:,-1],outer[0],outer[-1]),(inner[:,0],inner[:,-1],inner[0],inner[-1])):
        s.mesh(np.stack([a,b],axis=1),IVORY,.35,.3);s.tube(a,.018,IVORY,10)
    # Internal engraved divisions keep the extracted segment visibly related.
    for i in(3,4):
        p=patch(i*PI/nt,i*PI/nt,v0,v1)[0]
        s.tube((p-centroid)@rot.T+shift,.009,IVORY,8)
    for j in(2,3):
        p=patch(t0,t1,j*2*PI/nv,j*2*PI/nv)[:,0]
        s.tube((p-centroid)@rot.T+shift,.009,IVORY,8)
    return s

def tmesis():
    s=Scene(rz(.065)@ry(-.12)@rx(.10))
    def shell(xs,shift):
        x,v=np.meshgrid(xs,np.linspace(0,2*PI,145),indexing='ij')
        r=.97*np.sqrt(np.maximum(0,1-(x/2.50)**2))
        r*=1+.025*np.cos(16*v)
        p=np.stack([x+shift,r*np.cos(v),r*np.sin(v)],-1);s.mesh(p,IVORY,.38,.25)
        idx=-1 if shift<0 else 0
        edge=p[idx];s.tube(edge,.046,GOLD,14)
        # A recessed dark end closes the shell behind its tactile cut rim.
        v=np.linspace(0,2*PI,145);rads=np.linspace(0,.91,25)
        xx=float(xs[idx])+shift+(.06 if shift>0 else-.06)
        vv,rr=np.meshgrid(v,rads,indexing='ij')
        pp=np.stack([np.full_like(vv,xx),rr*np.cos(vv),rr*np.sin(vv)],-1)
        s.mesh(pp,hexcol('615168'),.6,.10)
    shell(np.linspace(-2.50,-.50,110),-.38);shell(np.linspace(.50,2.50,110),.38)
    # A foreign, fluted insert has its own visual grammar and occupies the seam.
    x,v=np.meshgrid(np.linspace(-.43,.43,100),np.linspace(0,2*PI,181),indexing='ij')
    r=(.91+.06*np.cos(12*PI*x))*(1+.025*np.cos(24*v))
    p=np.stack([x,r*np.cos(v),r*np.sin(v)],-1)
    ao=.8+.2*(np.cos(12*PI*x)+1)/2
    s.mesh(p,hexcol('B7738C'),.29,.70,ao=ao)
    for xx in(-.43,.43):
        v=np.linspace(0,2*PI,200);r=.91+.06*np.cos(12*PI*xx)
        s.tube(np.stack([np.full_like(v,xx),r*np.cos(v),r*np.sin(v)],-1),.025,GOLD,12)
    return s

if __name__=='__main__':
    funcs={17:('metalepsis',metalepsis),18:('palimpsest',palimpsest),19:('parataxis',parataxis),20:('quiddity',quiddity),21:('semiosis',semiosis),22:('synecdoche',synecdoche),23:('tmesis',tmesis)}
    ids=[int(a) for a in sys.argv[1:] if a.isdigit()] or list(funcs)
    for i in ids:
        name,fun=funcs[i];fun().render(f'{i:02d}-{name}','--proof' in sys.argv)
