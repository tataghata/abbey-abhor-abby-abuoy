import numpy as np, math, ctypes, pathlib, struct,zlib,sys,time
B=pathlib.Path('/tmp/memoryx-word-atlas23/group-b')
lib=ctypes.CDLL(str(B/'raster.dylib'))
lib.render.argtypes=[ctypes.POINTER(ctypes.c_float),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_float,ctypes.POINTER(ctypes.c_uint8)]
parts=[]
COL={'gold':(.77,.48,.16),'pearl':(.78,.71,.63),'teal':(.14,.57,.51),'coral':(.78,.29,.24),'violet':(.49,.29,.67),'blue':(.22,.48,.78),'mint':(.48,.68,.43),'silver':(.46,.46,.57)}
def color(c):return np.array(COL[c] if isinstance(c,str) else c)
def norm(v):return v/np.maximum(np.linalg.norm(v,axis=-1,keepdims=True),1e-12)
def rot(x=0,y=0,z=0):
 a,b,c=np.cos([x,y,z]);d,e,f=np.sin([x,y,z])
 return np.array([[c,-f,0],[f,c,0],[0,0,1]])@np.array([[b,0,e],[0,1,0],[-e,0,b]])@np.array([[1,0,0],[0,a,-d],[0,d,a]])
def addgrid(p,n,c):
 if np.asarray(c).ndim==1: c=np.broadcast_to(c,p.shape)
 v=np.concatenate([p,n,c],axis=-1).astype(np.float32)
 parts.append(np.concatenate([np.stack([v[:-1,:-1],v[1:,:-1],v[1:,1:]],axis=-2).reshape(-1,3,9),np.stack([v[:-1,:-1],v[1:,1:],v[:-1,1:]],axis=-2).reshape(-1,3,9)]))
def tube(p,r,c,around=32,ripple=0):
 p=np.asarray(p);t=norm(np.gradient(p,axis=0));ref=np.broadcast_to([0,0,1.],t.shape).copy();ref[np.abs(t[:,2])>.95]=[0,1,0];n=norm(np.cross(t,ref));b=norm(np.cross(t,n))
 a=np.linspace(0,2*np.pi,around+1);rad=np.asarray(r);rad=np.full(len(p),r) if rad.ndim==0 else rad
 nn=n[:,None,:]*np.cos(a)[None,:,None]+b[:,None,:]*np.sin(a)[None,:,None]
 rr=rad[:,None]*(1+ripple*np.cos(a*8)[None,:]);pos=p[:,None,:]+nn*rr[:,:,None]
 if np.asarray(c).ndim==2:c=np.broadcast_to(np.asarray(c)[:,None,:],pos.shape)
 addgrid(pos,nn,color(c) if isinstance(c,str) else c)
def sphere(center,r,c,ridges=0,rotation=None,squash=(1,1,1)):
 nu,nv=(31,49) if r<.2 else (121,193)
 u=np.linspace(.00001,np.pi-.00001,nu);v=np.linspace(0,2*np.pi,nv)
 U,V=np.meshgrid(u,v,indexing='ij');base=np.stack([np.sin(U)*np.cos(V),np.cos(U),np.sin(U)*np.sin(V)],axis=-1)
 rr=r*(1+ridges*np.sin(U)**2*np.cos(18*V+2.2*np.sin(U*2)))
 p=base*rr[:,:,None]*np.array(squash)
 n=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)))
 outward=np.sum(n*base,axis=-1);n[outward<0]*=-1
 if rotation is not None:p=p@rotation.T;n=n@rotation.T
 addgrid(p+center,n,color(c))
def line(a,b,r,c):tube(np.linspace(a,b,80),r,color(c),24)
def ring(center,r,c,rotation=None,thick=.027,arc=(0,2*np.pi)):
 t=np.linspace(*arc,420);p=np.stack([r*np.cos(t),r*np.sin(t),np.zeros_like(t)],axis=-1)
 if rotation is not None:p=p@rotation.T
 tube(p+np.array(center),thick,color(c),24)
def cone(base,tip,r,c):
 base=np.array(base);tip=np.array(tip);v=norm(tip-base);n=norm(np.cross(v,[0,0,1]));
 if np.linalg.norm(n)<.5:n=norm(np.cross(v,[0,1,0]))
 b=np.cross(v,n);theta=np.linspace(0,2*np.pi,49);q=np.linspace(0,1,20)
 rr=r*(1-q);p=base[None,None,:]+q[:,None,None]*(tip-base)[None,None,:]+rr[:,None,None]*(np.cos(theta)[None,:,None]*n+np.sin(theta)[None,:,None]*b)
 radial=np.cos(theta)[None,:,None]*n+np.sin(theta)[None,:,None]*b
 no=norm(radial+v[None,None,:]*(r/np.linalg.norm(tip-base)));no=np.broadcast_to(no,p.shape)
 addgrid(p,no,color(c))
def arrow(a,b,r,c,head=.18):
 a=np.array(a);b=np.array(b);v=norm(b-a);line(a,b-v*head*.75,r,c);cone(b-v*head,b,r*2.8,c)
def ribbon(p,width,c,twist=0,phase=0):
 p=np.asarray(p);t=norm(np.gradient(p,axis=0));n=norm(np.cross(t,np.broadcast_to([0,0,1],t.shape)));b=norm(np.cross(t,n));u=np.linspace(-1,1,28);ang=np.linspace(0,twist,len(p))+phase
 side=n*np.cos(ang)[:,None]+b*np.sin(ang)[:,None];up=norm(np.cross(t,side))
 # Shallow arched cross-section and rolled edges make a satin-metal strip.
 pos=p[:,None,:]+width*u[None,:,None]*side[:,None,:]+(.10*width*(1-u*u))[None,:,None]*up[:,None,:]
 no=norm(np.cross(np.gradient(pos,axis=0),np.gradient(pos,axis=1)))
 # Double sided surface, with view-facing normals for the thin ribbon.
 no[no[:,:,2]<0]*=-1
 cc=np.broadcast_to(color(c),pos.shape).copy();cc*=((.93+.07*np.cos(u*np.pi*7))[None,:,None])
 addgrid(pos,no,cc)
 # Delicate rolled hem of the same alloy catches the studio light.
 tube(pos[:,0],.013,color(c),16);tube(pos[:,-1],.013,color(c),16)
def box(center,half,c,bevel=.06,rotation=None):
 center=np.asarray(center);half=np.asarray(half);core=half-bevel
 for axis in range(3):
  other=[q for q in range(3) if q!=axis]
  vals=[]
  for q in other:
   h=core[q];r=bevel;vals.append(np.array([-h-r,-h-r*.92,-h-r*.7,-h-r*.38,-h,-h*.5,0,h*.5,h,h+r*.38,h+r*.7,h+r*.92,h+r]))
  for sign in [-1,1]:
   U,V=np.meshgrid(*vals,indexing='ij');p=np.zeros(U.shape+(3,));p[:,:,axis]=sign*half[axis];p[:,:,other[0]]=U;p[:,:,other[1]]=V
   q=np.clip(p,-core,core);n=norm(p-q);p=q+bevel*n
   if rotation is not None:p=p@rotation.T;n=n@rotation.T
   addgrid(p+center,n,color(c))
def png(path,a):
 h,w,c=a.shape
 def chunk(k,d):return struct.pack('>I',len(d))+k+d+struct.pack('>I',zlib.crc32(k+d)&0xffffffff)
 comp=zlib.compressobj(6)
 with open(path,'wb') as f:
  f.write(b'\x89PNG\r\n\x1a\n');f.write(chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6 if c==4 else 2,0,0,0)))
  for row in a:
   d=comp.compress(b'\0'+row.tobytes())
   if d:f.write(chunk(b'IDAT',d))
  f.write(chunk(b'IDAT',comp.flush()));f.write(chunk(b'IEND',b''))
def save(stem,proof=False):
 tris=np.ascontiguousarray(np.concatenate(parts),dtype=np.float32)
 W,H=(1800,800) if proof else (7200,3200);a=np.zeros((H,W,4),np.uint8)
 print(stem,'triangles',len(tris),flush=True);t=time.time();lib.render(tris.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),len(tris),W,H,W/9.,a.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)))
 if not proof:png(B/(stem+'.png'),a)
 factor=1 if proof else 4
 # Downsample alpha-composited art in 200-row strips to bound memory use.
 rgb=np.empty((800,1800,3),np.uint8)
 for y in range(0,H,200*factor):
  aa=a[y:y+200*factor,:,3:4].astype(np.float32)/255
  b=a[y:y+200*factor,:,:3].astype(np.float32)*aa+np.array([32,26,50],np.float32)*(1-aa)
  if factor>1:b=b.reshape(len(b)//factor,factor,1800,factor,3).mean(axis=(1,3))
  rgb[y//factor:y//factor+len(b)]=np.rint(b).astype(np.uint8)
 png(B/(stem+'-preview.png'),rgb);print('saved',stem,round(time.time()-t,1),'seconds',flush=True)

def clinamen():
 x=np.linspace(-3.8,3.8,1200)
 for j,y in enumerate(np.linspace(-1.22,1.22,11)):
  p=np.stack([x,np.full_like(x,y),np.full_like(x,-.3)],axis=-1);tube(p,.022, np.array([.30,.32,.39])*(.85+.025*j),20)
  for k,xx in enumerate(np.linspace(-3.5,3.5,13)):
   sphere([xx,y,-.27],.037,'silver') if False else None
  # Small polished particles distributed at irregular, reproducible intervals.
  for xx in np.linspace(-3.5,3.5,8)+.04*np.sin(j*2.7):
   sphere([xx,y,-.20],.045,(.40,.43,.49))
 y=.02+.85/(1+np.exp(-(x-.2)*3))
 p=np.stack([x,y,.04+.2*np.sin((x+4)/8*np.pi)],axis=-1);tube(p,.062,'gold',40)
 for xx in [-3.4,-2.25,-1.1,.05,1.2,2.35,3.4]:
  yy=.02+.85/(1+np.exp(-(xx-.2)*3));sphere([xx,yy,.14],.104,'gold',0)
 # A second fine trajectory catches the collision-rich opening.

def consilience():
 t=np.linspace(0,1,1300);cols=['coral','violet','blue','teal','mint','pearl','gold']
 for k,c in enumerate(cols):
  y0=(k-3)*.42;phase=k*.95
  x=-3.8+5.7*t;y=y0*(1-t)**1.1+.19*np.sin(t*3*np.pi+phase)*np.sin(t*np.pi)
  z=.28*np.sin(phase+t*3*np.pi)*np.sin(t*np.pi)
  p=np.stack([x,y,z],axis=-1);tube(p,.055,color(c),32)
  # All strands are distinct at their origin, not duplicates of one source.
  sphere(p[0],.105,c)
 sphere([2.45,0,0],.76,'pearl',.055,rot(.2,.7,.1))
 ring([2.45,0,0],1.03,'gold',rot(.95,.55,.15),.035)
 for a in np.linspace(.2,5.8,5):
  p=np.array([1.03*np.cos(a),1.03*np.sin(a),0])@rot(.95,.55,.15).T+np.array([2.45,0,0]);sphere(p,.067,'gold')

def deixis():
 sphere([0,0,.1],.47,'pearl',.052,rot(.3,.6,.1));ring([0,0,.1],.7,'gold',rot(.5,-.5,0),.022)
 for center,ang,col in [((-2.95,-.45,0),.18,'coral'),((.2,1.08,-.15),-1.1,'violet'),((2.93,-.50,.05),2.75,'teal')]:
  ce=np.array(center);R=rot(.4,.3,ang)
  for axis in [[.8,0,0],[0,.72,0],[0,0,.62]]:arrow(ce,ce+np.array(axis)@R.T,.039,col,.15)
  sphere(ce,.12,col);ring(ce,.47,col,R,.020)
  dest=np.array([0,0,.1]);vec=dest-ce;end=dest-norm(vec)*.78
  # Slim arrows identify the demonstrative's target while frames stay distinct.
  arrow(ce+norm(vec)*.28,end,.027,col,.20)

def epoche():
 # Two rounded architectural brackets preserve the visible suspended object.
 for s in [-1,1]:
  x=s*2.18
  line([x,-1.25,0],[x,1.25,0],.115,'pearl')
  for y in [-1.25,1.25]:
   line([x,y,0],[x-s*.64,y,0],.115,'pearl');sphere([x,y,0],.115,'pearl');sphere([x-s*.64,y,0],.115,'pearl')
 sphere([0,0,.1],.84,'gold',.038,rot(.8,.35,.25))
 ring([0,0,.1],1.25,'violet',rot(.97,.3,-.28),.033)
 ring([0,0,.1],1.43,'pearl',rot(1.19,-.25,.24),.018)

def heteroglossia():
 x=np.linspace(-3.82,3.82,1600)
 for k,c in enumerate(['violet','gold','coral','teal','blue','pearl']):
  phase=k*2*np.pi/6;u=(x+3.82)/7.64;envelope=.75+.18*np.sin(u*np.pi)
  y=envelope*np.sin(u*np.pi*3.5+phase);z=.48*np.cos(u*np.pi*3.5+phase)
  p=np.stack([x,y,z],axis=-1)
  if k%2==0:ribbon(p,.13,c,twist=np.pi*2.5,phase=phase*.4)
  else:tube(p,.073,color(c),40,ripple=.07)

def hysteresis():
 # Qualitative magnetization-like cyclic loop: decreasing input follows upper branch.
 line([-3.8,0,-.22],[3.8,0,-.22],.014,(.30,.31,.40));cone([3.66,0,-.22],[3.88,0,-.22],.055,(.30,.31,.40))
 line([0,-1.55,-.22],[0,1.55,-.22],.014,(.30,.31,.40));cone([0,1.44,-.22],[0,1.66,-.22],.055,(.30,.31,.40))
 for xx in [-3,-1.5,1.5,3]:line([xx,-.052,-.2],[xx,.052,-.2],.012,(.40,.4,.49))
 for start,stop,col in [(0,np.pi,'gold'),(np.pi,2*np.pi,'teal')]:
  t=np.linspace(start,stop,1400);x=3.12*np.cos(t);y=1.15*np.tanh(2.2*np.cos(t)+.9*np.sin(t));z=np.zeros_like(t)
  p=np.stack([x,y,z],axis=-1);tube(p,.07,color(col),40)
  tt=(start+stop)/2-.40;tip=np.array([3.12*np.cos(tt+.045),1.15*np.tanh(2.2*np.cos(tt+.045)+.9*np.sin(tt+.045)),.015]);base=np.array([3.12*np.cos(tt-.03),1.15*np.tanh(2.2*np.cos(tt-.03)+.9*np.sin(tt-.03)),.015]);cone(base,tip,.14,col)
 for yy,c in [(1.15*np.tanh(.9),'gold'),(-1.15*np.tanh(.9),'teal')]:sphere([0,yy,.06],.125,c)

def hypallage():
 sphere([-2.20,0,0],.78,'silver',.014,rot(.1,.5,.25),(.96,1.09,.9))
 sphere([2.12,0,0],.84,'pearl',.047,rot(.2,-.6,-.25),(.96,1.03,.93))
 # A single continuous satin band leaves its first bearer and wraps the next.
 left=np.linspace(np.pi*1.47,np.pi*.5,850)
 pl=np.stack([-2.2+.85*np.cos(left),.95*np.sin(left),np.full_like(left,.33)],axis=-1)
 u=np.linspace(0,1,1200)
 pc=np.stack([-2.2+4.32*u,.95+.28*np.sin(np.pi*u)**2,.33+.26*np.sin(np.pi*u)**2],axis=-1)
 right=np.linspace(np.pi*.5,-np.pi*.47,850)
 pr=np.stack([2.12+.87*np.cos(right),.95*np.sin(right),np.full_like(right,.33)],axis=-1)
 p=np.concatenate([pl[:-1],pc[:-1],pr]);ribbon(p,.17,'gold',twist=np.pi*.30,phase=.10)

def liminality():
 R=rot(.15,-.55,-.06)
 def cb(c,h,col,bev=.06):box(np.array(c)@R.T,h,col,bev,R)
 cb([-1.82,-1.03,0],[1.52,.12,.81],'silver',.045)
 cb([1.82,-1.03,0],[1.52,.12,.81],'mint',.045)
 for x in [-2.8,-2.2,-1.6,-1.,1.,1.6,2.2,2.8]:
  cb([x,-.898,0],[.012,.008,.71],(.64,.64,.68),.004)
 # Portal lies across the path: the camera sees depth and both discontinuous platforms.
 for z in [-.69,.69]:cb([0,.06,z],[.17,1.10,.145],'pearl',.048)
 cb([0,1.19,0],[.17,.16,.83],'pearl',.048)
 for z in [-.54,.54]:
  a=np.array([.178,-.91,z])@R.T;b=np.array([.178,1.06,z])@R.T;line(a,b,.019,'gold')
 cb([0,-.88,0],[.20,.036,.54],'gold',.018)
 # A faint second threshold beyond the first locates the destination without closing it.

funcs={9:('09-clinamen',clinamen),10:('10-consilience',consilience),11:('11-deixis',deixis),12:('12-epoche',epoche),13:('13-heteroglossia',heteroglossia),14:('14-hysteresis',hysteresis),15:('15-hypallage',hypallage),16:('16-liminality',liminality)}
if __name__=='__main__':
 proof='--proof' in sys.argv
 args=[int(x) for x in sys.argv[1:] if x.isdigit()] or list(funcs)
 for key in args:
  parts.clear();name,f=funcs[key];f();save(name,proof)
