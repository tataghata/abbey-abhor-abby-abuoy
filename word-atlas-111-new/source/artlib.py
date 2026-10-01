"""Local concept sculpture renderer. No AI image service is used.
Coordinates: x in [-4.5,4.5], y in [-2,2]. Native art: 7200 x 3200 RGBA.
"""
import numpy as np, math, ctypes, pathlib, struct, zlib, sys, time, json
SOURCE=pathlib.Path(__file__).resolve().parent
B=SOURCE/'art'
PROOFS=SOURCE/'proofs'
LIB=pathlib.Path('/tmp/memoryx-word-atlas111/raster.dylib')
lib=ctypes.CDLL(str(LIB))
lib.render.argtypes=[ctypes.POINTER(ctypes.c_float),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_float,ctypes.POINTER(ctypes.c_uint8)]
lib.render.restype=None
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
 if not parts: raise ValueError('Empty sculpture: '+stem)
 tris=np.ascontiguousarray(np.concatenate(parts),dtype=np.float32)
 if not np.isfinite(tris).all():raise ValueError('Nonfinite mesh: '+stem)
 bounds=np.max(np.abs(tris[:,:,:2]),axis=(0,1))
 fit=min(1.,4.18/max(bounds[0],1e-9),1.78/max(bounds[1],1e-9))
 if fit<1:
  tris[:,:,:3]*=fit
  print(stem,'fitted by',round(float(fit),3),flush=True)
 W,H=(1800,800) if proof else (7200,3200)
 a=np.zeros((H,W,4),np.uint8)
 print(stem,'triangles',len(tris),flush=True);t=time.time()
 lib.render(tris.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),len(tris),W,H,W/9.,a.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)))
 if not proof:png(B/(stem+'.png'),a)
 factor=1 if proof else 4
 rgb=np.empty((800,1800,3),np.uint8)
 for y in range(0,H,200*factor):
  aa=a[y:y+200*factor,:,3:4].astype(np.float32)/255
  b=a[y:y+200*factor,:,:3].astype(np.float32)*aa+np.array([32,26,50],np.float32)*(1-aa)
  if factor>1:b=b.reshape(len(b)//factor,factor,1800,factor,3).mean(axis=(1,3))
  rgb[y//factor:y//factor+len(b)]=np.rint(b).astype(np.uint8)
 png(PROOFS/(stem+('-proof.png' if proof else '-art-preview.png')),rgb)
 metadata={'stem':stem,'triangles':len(tris),'dimensions':[W,H],'fit':float(fit),'coverage':float(np.count_nonzero(a[:,:,3]))/(W*H),'render_seconds':round(time.time()-t,2),'method':'local-procedural-3d'}
 (PROOFS/(stem+('-proof.json' if proof else '-art.json'))).write_text(json.dumps(metadata,indent=2)+'\n')
 print('SAVED',stem,W,H,round(time.time()-t,1),'seconds',flush=True)
