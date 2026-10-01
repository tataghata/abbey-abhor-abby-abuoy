"""Thirty-seven original concept sculptures, authored for atlas 111 (local mesh rendering)."""
import sys, math
import numpy as np
from artlib import parts, tube, sphere, line, ring, cone, arrow, ribbon, box, rot, norm, color, addgrid, save
pi=np.pi
G='gold';P='pearl';T='teal';C='coral';V='violet';B='blue';S='silver';M='mint'

def ell(c,r,col,scale=(1,1,1),R=None,ruffle=0):
 u,v=np.meshgrid(np.linspace(.0001,pi-.0001,49),np.linspace(0,2*pi,73),indexing='ij')
 n=np.stack([np.sin(u)*np.cos(v),np.cos(u),np.sin(u)*np.sin(v)],-1)
 p=n*r*(1+ruffle*np.sin(8*v)*np.sin(u)**2)[...,None]*np.array(scale)
 nn=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)));nn[np.sum(nn*n,axis=-1)<0]*=-1
 if R is not None:p=p@R.T;nn=nn@R.T
 addgrid(p+np.array(c),nn,color(col))
def curve(points,col=G,r=.04,n=140):
 points=np.asarray(points,float)
 if len(points)==3:
  t=np.linspace(0,1,n)[:,None];p=(1-t)**2*points[0]+2*t*(1-t)*points[1]+t*t*points[2]
 else:p=points
 tube(p,r,col,20)
def loop(c,r,col=G,R=None,th=.03,arc=(0,2*pi)):
 t=np.linspace(*arc,190);p=np.stack([r*np.cos(t),r*np.sin(t),np.zeros_like(t)],-1)
 if R is not None:p=p@R.T
 tube(p+np.array(c),th,col,20)
def leaf(c,scale,col,R=None):
 u,v=np.meshgrid(np.linspace(0,1,75),np.linspace(-1,1,21),indexing='ij')
 p=np.stack([scale[0]*(2*u-1),scale[1]*v*np.sin(pi*u),scale[2]*(1-v*v)*np.sin(pi*u)],-1)
 nn=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)));nn[nn[...,2]<0]*=-1
 if R is not None:p=p@R.T;nn=nn@R.T
 addgrid(p+np.array(c),nn,color(col))
def frame(c,w,h,col=G):
 x,y,z=c
 for a,b in [((-w,-h),(w,-h)),((w,-h),(w,h)),((w,h),(-w,h)),((-w,h),(-w,-h))]:line([x+a[0],y+a[1],z],[x+b[0],y+b[1],z],.035,col)
def plate(c,w,h,col=P,R=None):box(c,[w,h,.07],col,.035,R)
def branch(c,sz=1,col=T):
 x,y,z=c;curve([[x,y,z],[x-.12*sz,y+.65*sz,z+.08],[x,y+1.3*sz,z]],col,.055*sz)
 for k in range(4):
  yy=y+.2*sz+k*.25*sz;s=(-1)**k
  leaf([x+s*.22*sz,yy,z+.1],(.35*sz,.13*sz,.05*sz),col,rot(0,0,s*.6))
def person(c,col=P,angle=0,sz=1):
 x,y,z=c;ell([x,y+.55*sz,z],.17*sz,col)
 tube(np.array([[x,y+.3*sz,z],[x+.04*sz,y,z],[x,y-.45*sz,z]]),.09*sz,col,24)
 for s in [-1,1]:
  curve([[x,y+.2*sz,z],[x+s*.25*sz,y-.02*sz,z],[x+s*.3*sz,y-.2*sz,z+angle]],col,.052*sz)
  line([x,y-.4*sz,z],[x+s*.19*sz,y-.8*sz,z],.063*sz,col)
def vase(c,sz=1,col=P,open_top=True):
 x,y,z=c;u,v=np.meshgrid(np.linspace(0,1,85),np.linspace(0,2*pi,99),indexing='ij')
 rr=sz*(.22+.22*np.sin(pi*u)**.65);p=np.stack([rr*np.cos(v)+x,(u-.5)*sz*1.4+y,rr*np.sin(v)+z],-1)
 nn=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)));nn[nn[...,2]<0]*=-1
 addgrid(p,nn,color(col));loop([x,y+.7*sz,z],.22*sz,G,rot(pi/2,0,0),.025)
def arch(c,w,h,col=P):
 x,y,z=c;line([x-w,y,z],[x-w,y+h*.58,z],.09,col);line([x+w,y,z],[x+w,y+h*.58,z],.09,col)
 t=np.linspace(0,pi,150);tube(np.stack([x+w*np.cos(t),y+h*.58+h*.42*np.sin(t),np.full_like(t,z)],-1),.09,col,28)
def helix(x0,x1,y=0,z=0,r=.4,turns=3,col=G,th=.04):
 t=np.linspace(0,1,500);p=np.stack([x0+(x1-x0)*t,y+r*np.sin(t*2*pi*turns),z+r*np.cos(t*2*pi*turns)],-1);tube(p,th,col,24);return p

def holophrasis():
 ell([-3.05,0,.3],.32,P,ruffle=.04);loop([-3.05,0,.3],.55,G,rot(.35,.5,0),.026)
 for j in range(7):
  yy=(j-3)*.39;dest=[1.3+.18*j,yy,0]
  curve([[-2.7,0,.2],[-.7,yy*.75,.05],dest],G if j%2==0 else T,.026)
  plate([dest[0]+.35,yy,0],.46,.14,P,rot(0,-.12,.035*(j-3)))
 arch([2.9,-1.5,.15],.72,3,P)
 for y in [-1.15,-.76,-.37,.02,.41,.80,1.19]:line([2.37,y,.28],[3.44,y,.28],.012,G)

def homoioteleuton():
 for j in range(5):
  yy=1.25-j*.61
  intervals=[(-3.7,2.72)] if j!=2 else [(-3.7,-1.35),(1.6,2.72)]
  for a,b in intervals:
   x=np.linspace(a,b,170);p=np.stack([x,np.full_like(x,yy),.06*np.sin(x*1.7)],-1);ribbon(p,.072,P)
  loop([3.07,yy,.04],.19,G,th=.036)
  for x in np.arange(-3.4,2.4,.44):
   if j==2 and -1.35<x<1.6:continue
   line([x,yy-.075,.12],[x+.08,yy+.075,.12],.018,T)
 curve([[3.07,.83,.3],[3.86,0,.85],[3.07,-.59,.3]],C,.045)
 cone([3.18,-.49,.35],[3.06,-.59,.3],.105,C)
 curve([[-1.22,.03,.15],[.1,.58,.32],[1.45,.03,.15]],G,.018)

def hypostasis():
 box([0,-1.28,0],[3.4,.22,.42],P,.12)
 for x in [-2.2,0,2.2]:
  arch([x,-1.06,0],.75,2.25,P)
  curve([[x-.72,-.95,.1],[x,1.34,-.2],[x+.72,-.95,.1]],G,.032)
  ell([x,.05,-.08],.27,G,scale=(.75,1.8,.7))
 t=np.linspace(-3.45,3.45,450);tube(np.stack([t,-1.31+.04*np.sin(3*t),np.full_like(t,.43)],-1),.024,T,20)

def hypotaxis():
 box([0,1.14,0],[1.13,.23,.28],P,.08)
 for x in [-2.7,0,2.7]:
  curve([[0,.89,0],[x,.91,-.08],[x,.15,0]],G,.045)
  box([x,-.05,0],[.78,.18,.22],T,.05)
  for off in [-.44,.44]:
   xx=x+off;line([xx,-.23,0],[xx,-.94,0],.028,P);box([xx,-1.09,.04],[.27,.13,.19],V,.045)
   line([xx,-1.24,0],[xx+.12,-1.47,0],.015,G)

def iconotext():
 for k in range(7):
  y=(k-3)*.27;box([-2.65,y,0],[.9,.043,.045],P,.025)
  x=np.linspace(-1.74,.72,350);p=np.stack([x,y*(1-(x+1.74)/4)+.08*np.sin(3*x+k),.12*np.sin(3*x+k)],-1);ribbon(p,.05,G if k%2 else P)
 for j in range(3):
  leaf([2.3,.78-j*.8,.08],(.86,.32,.1),[T,C,V][j],rot(0,.2,-.23+j*.3))
  curve([[1.53,.78-j*.8,.1],[.9,-.7+j*.7,.3],[-.6,.6-j*.5,.1]],[T,C,V][j],.09)
 frame([0,0,-.3],3.85,1.45,S)

def illeism():
 person([-2.65,.07,.04],P,angle=.25,sz=1.35)
 plate([1.57,-1.15,0],1.25,.17,S);person([1.57,.01,.1],G,angle=.25,sz=1.13)
 frame([1.57,.14,-.15],1.15,1.4,P)
 curve([[-2.2,.66,.25],[-.2,1.3,.48],[1.35,.67,.12]],T,.036)
 cone([1.14,.79,.14],[1.39,.65,.1],.11,T)
 for k in range(5):ell([-.9+k*.24,-.73,.2],.04,S)

def immanence():
 u,v=np.meshgrid(np.linspace(-3.7,3.7,230),np.linspace(-1.15,1.15,83),indexing='ij')
 z=.45*np.cos(u*1.4)*np.cos(v*1.6)+.20*np.sin(3*u)*np.cos(v*2)
 p=np.stack([u,v,z],-1);nn=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)))
 cc=np.broadcast_to(color(T),p.shape).copy();cc*= (.75+.25*(z-z.min())/(z.max()-z.min()))[...,None];addgrid(p,nn,cc)
 for y in np.linspace(-1.15,1.15,11):
  x=np.linspace(-3.7,3.7,430);zz=.45*np.cos(x*1.4)*np.cos(y*1.6)+.20*np.sin(3*x)*np.cos(y*2)
  tube(np.stack([x,np.full_like(x,y),zz+.014],-1),.018,G,16)
 for x in [-2.6,0,2.6]:
  zz=.45*np.cos(x*1.4)+.2*np.sin(3*x);ell([x,0,zz+.09],.1,G)

def incommensurability():
 frame([-1.35,0,0],1.25,1.25,P)
 line([-2.6,-1.25,.07],[-.1,1.25,.07],.064,T)
 line([-2.6,-1.25,.07],[-.1,-1.25,.07],.064,G)
 for k in range(11):
  xx=-2.6+.25*k;line([xx,-1.39,.1],[xx,-1.12,.1],.012,G)
  p=np.array([-2.6,-1.25,.1])+k/10*np.array([2.5,2.5,0]);line(p+[-.08,.08,0],p+[.08,-.08,0],.014,T)
 for j in range(3):
  y=1.0-j*.75
  line([.65,y,0],[3.72,y,0],.02,S)
  for x in np.arange(.65,3.73,.41/(j+1)):line([x,y-.1,0],[x,y+.1,0],.01,S)
  line([.65,y+.18,.1],[3.15,y+.18,.1],.04,G)
  line([.65,y-.18,.1],[3.65,y-.18,.1],.04,T)

def indexicality():
 for x in [-2.65,2.65]:
  plate([x,-.6,-.18],.97,.61,S,rot(.36,.1,0))
  for off in [-.32,.32]:
   loop([x+off,-.56,.02],.18,T,rot(.65,0,0),.04)
   ell([x+off,-.8,.01],.15,T,scale=(1,.52,.5))
 ell([0,.37,.25],.62,P,ruffle=.025)
 for s in [-1,1]:
  curve([[s*.59,.37,.1],[s*1.55,.82,.2],[s*2.63,-.18,.02]],G,.026)
  cone([s*2.5,-.02,.06],[s*2.65,-.23,.02],.10,G)
  for j in range(5):ell([s*(.9+j*.24),-1.16,.1],.045,G)
 loop([0,.37,.12],.91,G,rot(.35,.1,0),.02)

def interpellation():
 for r in [.45,.77,1.1,1.43]:loop([-3.43,.13,0],r,G,th=.025,arc=(-.85,.85))
 person([.28,.15,.2],P,angle=.45,sz=1.2)
 frame([2.59,.05,-.1],.74,1.32,T)
 person([2.59,.1,-.05],S,sz=1.1)
 curve([[.66,.44,.25],[1.29,.87,.4],[2.06,.72,0]],G,.04)
 cone([1.89,.79,.03],[2.15,.7,0],.12,G)
 plate([.28,-1.17,.04],.68,.13,G)

def isomorphism():
 left=np.array([[-2.9,.95,0],[-1.6,1.04,0],[-1.05,-.33,.1],[-2.18,-1.13,0],[-3.48,-.45,0]])
 right=np.array([[1.05,-1.03,.1],[3.45,-.91,0],[1.1,1.08,0],[3.44,1.05,0],[2.25,.08,.28]])
 edges=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,2),(1,4)]
 cols=[G,T,C,V,P]
 for pts in [left,right]:
  for a,b in edges:line(pts[a],pts[b],.028,S)
  for k,p in enumerate(pts):ell(p,.15,cols[k])
 for y in [-.15,.15]:line([-.55,y,0],[.5,y,0],.035,G)

def kairos():
 for x in [-1.42,1.42]:
  for j in range(11):
   a=(j+1)*2*pi/12;R=rot(.45,.12,a)
   c=np.array([.82*np.cos(a),.82*np.sin(a),0])+[x,0,0]
   leaf(c,(.48,.16,.10),P,R)
  loop([x,0,0],1.31,G,rot(.15,0,0),.024,arc=(.27,2*pi-.27))
 curve([[-3.85,.01,.35],[0,0,.4],[3.8,0,.4]],T,.047)
 cone([3.37,0,.4],[3.85,0,.4],.17,T)
 for x in [-2.2,0,2.2]:ell([x,.02,.45],.08,G)

def kenosis():
 vase([-2.05,.46,.05],1.4,P)
 # A flowing strip leaves a tilted lip and enters a low, open vessel.
 t=np.linspace(0,1,430);p=np.stack([-1.77+3.37*t,1.44-2.19*t+.58*np.sin(pi*t),.4+.09*np.sin(2*pi*t)],-1)
 ribbon(p,.11,G,twist=.7)
 vase([1.89,-.67,0],.92,T)
 for j in range(6):ell([1.66+.09*np.cos(j),-.57+.16*j,.32],.035,G)
 loop([-2.05,.38,.1],.31,S,rot(pi/2,0,0),.016)

def logopoeia():
 for j,x in enumerate([-3.1,-1.55,0,1.55,3.1]):
  box([x,-.81,0],[.49,.28,.28],S,.06)
  if j!=2:
   box([x,.17,0],[.14,.71,.14],P,.04);box([x,.99,0],[.58,.10,.24],P,.04)
  else:
   t=np.linspace(0,1,490);p=np.stack([.38*np.sin(t*8*pi),-.5+1.44*t,.28*np.cos(t*8*pi)],-1);tube(p,.067,G,24)
   box([0,1.0,.02],[.58,.10,.24],C,.04,rot(0,0,.13))
   ell([0,1.28,.12],.15,G)
 for x in [-2.3,-.77,.77,2.3]:ell([x,.32,.2],.045,T)

def mereology():
 center=np.array([-1.3,0,0]);loop(center,1.31,P,rot(.2,.3,0),.105)
 for a in np.linspace(0,2*pi,9)[:-1]:
  p=center+np.array([1.25*np.cos(a),1.25*np.sin(a),.1]);line(center,p,.044,T)
 ell(center,.24,G)
 loop([1.73,0,.08],.67,T,rot(.2,.3,0),.085);ell([1.73,0,.1],.18,G)
 for a in np.linspace(0,2*pi,6)[:-1]:line([1.73,0,.1],[1.73+.64*np.cos(a),.64*np.sin(a),.1],.035,P)
 line([2.87,-.85,.1],[3.6,.88,.1],.054,P)
 curve([[-.29,.71,.1],[.51,1.45,.2],[1.52,.64,.1]],G,.022)
 curve([[2.36,.13,.1],[2.76,.62,.2],[3.24,.06,.1]],G,.022)

def metanoia():
 x=np.linspace(-3.72,.4,340);p=np.stack([x,np.full_like(x,-.91),np.zeros_like(x)],-1);ribbon(p,.18,S)
 t=np.linspace(-pi/2,pi/2,400);p=np.stack([.4+1.05*np.cos(t),.14+1.05*np.sin(t),.05+.2*np.cos(t)],-1);ribbon(p,.18,G)
 x=np.linspace(.4,-.65,180);p=np.stack([x,np.full_like(x,1.19),np.full_like(x,.05)],-1);ribbon(p,.18,G)
 cone([-.35,1.19,.07],[-.78,1.19,.07],.15,G)
 for xx in [-3.3,-2.55,-1.8]:box([xx,-.55,0],[.19,.18,.17],S,.03)
 branch([2.65,-.9,0],1.6,T)

def metempsychosis():
 cols=[P,T,C];xs=[-2.65,0,2.65]
 for j,x in enumerate(xs):
  for k in range(5):loop([x,0,-.15],.88+.055*k,cols[j],rot(.22+k*.14,.17*j,0),.017,arc=(.22,2*pi-.22))
  if j==0:person([x,.22,.1],P,sz=.73)
  if j==1:
   leaf([x-.25,.1,.1],(.5,.22,.07),T,rot(0,0,-.65));leaf([x+.25,.1,.1],(.5,.22,.07),T,rot(0,0,.65))
  if j==2:branch([x,-.52,.1],.8,C)
 helix(-3.7,3.7,0,.35,.15,1.5,G,.05)

def mimesis():
 x=np.linspace(-3.8,-.48,480);y=.74*np.sin((x+3.8)*2.55)
 tube(np.stack([x,y,np.zeros_like(x)],-1),.085,T,28)
 for xx in np.linspace(-3.7,-.62,20):ell([xx,.74*np.sin((xx+3.8)*2.55),.03],.037,P)
 arch([2.0,-1.21,-.05],1.65,2.65,P)
 box([2,-1.26,.05],[1.8,.11,.30],G,.045)
 x=np.linspace(.51,3.47,380);y=.6*np.sin((x-.51)*2.55)
 ribbon(np.stack([x,y,np.full_like(x,.28)],-1),.11,C,twist=.5)
 curve([[-.45,1.0,.1],[.1,1.5,.3],[.68,1.11,.1]],G,.024)

def monadology():
 for j,(x,y,sz) in enumerate([(-3.1,0,.58),(-1.56,.71,.48),(-1.55,-.71,.48),(0,0,.77),(1.6,.71,.48),(1.6,-.71,.48),(3.12,0,.58)]):
  ell([x,y,0],sz,[P,V,T,G,T,V,P][j],scale=(1,1.12,.8),ruffle=.035)
  for r in [.32,.52,.73]:
   loop([x,y,.50*sz],sz*r,S if j==3 else G,rot(.14,.45,0),.014,arc=(.18,pi*1.7))

def noesis():
 branch([2.87,-.77,0],1.35,T)
 for j,(yy,col) in enumerate([(-1.04,C),(0,G),(1.04,V)]):
  ell([-3.16,yy,.1],.17,col)
  x=np.linspace(-2.98,2.12,500);t=(x+2.98)/5.10
  y=yy*(1-t)+(.15 if j==1 else .25)*np.sin((j+1)*pi*t)
  z=.1+.12*np.sin(t*2*pi+j)
  p=np.stack([x,y,z],-1);tube(p,.043,col,24)
  cone(p[-18],p[-1]+[.13,0,0],.1,col)
  if j==2:loop([-1.8,yy*.72,.08],.22,col,th=.022)

def noema():
 for j,x in enumerate([-2.7,0,2.7]):
  frame([x,0,-.17],1.02,1.38,[P,V,T][j])
  branch([x,-.86,.12],1.3,[P,V,T][j])
  for off in [-.35,.35]:
   if j==1:curve([[x+off,-1.07,.25],[x+off+.15,0,.4],[x+off,1.1,.25]],S,.015)
  if j==2:
   for y in np.linspace(-1.0,1.06,8):line([x-.92,y,.31],[x+.92,y,.31],.009,G)

def noumenon():
 # The artwork shows a boundary of access; it does not depict a knowable noumenal object.
 for j,x in enumerate(np.linspace(-2.9,2.9,26)):
  y=np.linspace(-1.44,1.44,180);z=.18*np.sin(x*4.2)+.06*np.cos(y*3)
  p=np.stack([np.full_like(y,x),y,z],-1);ribbon(p,.07,P if j%2 else S)
 frame([0,0,-.18],3.12,1.53,G)
 for x in [-3.75,3.75]:
  loop([x,0,.1],.25,T,th=.02)
  line([x+(-.35 if x<0 else .35),0,.1],[x,0,.1],.03,T)

def ontogenesis():
 xs=[-3.0,-1.4,.38,2.56]
 ell([xs[0],0,0],.30,G,ruffle=.04)
 for k in range(4):
  a=k*pi/2;ell([xs[1]+.21*np.cos(a),.21*np.sin(a),0],.245,T)
 for k in range(7):
  a=k*2*pi/7;leaf([xs[2]+.23*np.cos(a),.23*np.sin(a),.1],(.50,.20,.06),M,rot(0,.2,a))
 branch([xs[3],-1.21,0],1.75,T)
 for x in [-2.16,-.42,1.48]:arrow([x-.15,0,.15],[x+.15,0,.15],.024,G,.1)

def paradiastole():
 # One unchanged faceted object straddles two evaluative colored frames.
 frame([-1.09,0,-.15],1.24,1.28,C);frame([1.09,0,-.15],1.24,1.28,T)
 for k in range(6):
  a=k*pi/3;leaf([.53*np.cos(a),.53*np.sin(a),.2],(.95,.26,.22),P,rot(.16,.1,a))
 ell([0,0,.32],.31,G)
 for x,c in [(-3.35,C),(3.35,T)]:
  loop([x,0,.1],.4,c,th=.04)
  curve([[x+(.35 if x<0 else -.35),0,.1],[x/2,.45,.35],[x/4,.32,.4]],c,.025)

def paronomasia():
 for yy,col in [(-.61,T),(.61,G)]:
  x=np.linspace(-3.7,1.08,650);p=np.stack([x,yy+.25*np.sin((x+3.7)*5.5),np.full_like(x,.1)],-1);tube(p,.05,col,28)
 loop([2.5,.62,.15],.35,G,th=.066)
 line([2.18,.62,.15],[1.43,.62,.15],.07,G)
 line([1.51,.62,.15],[1.51,.9,.15],.055,G)
 branch([2.52,-1.3,.1],.78,T)
 curve([[1.05,-.61,.1],[1.7,-.9,.1],[2.46,-.75,.1]],T,.045)

def peripeteia():
 p=np.array([[-3.75,-.6,0],[-1.9,-.6,0],[-.4,.08,.02]])
 curve(p,G,.085)
 t=np.linspace(-pi/2,pi*1.16,460);p=np.stack([.08+1.08*np.cos(t),.40+1.08*np.sin(t),.16+.16*np.cos(t)],-1);tube(p,.085,G,28)
 curve([p[-1],[-1.8,1.06,.2],[-3.47,1.06,.2]],C,.085)
 cone([-3.08,1.06,.2],[-3.57,1.06,.2],.20,C)
 box([2.38,-.82,0],[1.22,.12,.25],S,.045,rot(0,0,-.19))
 cone([2.13,-1.39,0],[2.13,-.6,0],.37,P)
 ell([3.24,-.61,.05],.30,G)

def pharmakon():
 vase([0,.2,0],1.38,P)
 for s,col in [(-1,T),(1,C)]:
  curve([[s*.28,.9,.18],[s*1.5,1.05,.26],[s*2.41,-.64,.1]],G,.078)
 if True:
  branch([-2.66,-1.24,.1],1.51,T)
  for j in range(8):
   x=2.14+.20*(j%3);y=-1.15+.34*(j//3)
   box([x,y,.1+.03*j],[.14,.14,.13],C,.025,rot(.1*j,.11*j,.16*j))
  for j in range(8):ell([2.78+.1*np.sin(j),-.46+.19*j,.06],.075-.006*j,C)

def pleroma():
 for j in range(7):
  a=j*2*pi/7;c=[1.09*np.cos(a),.74*np.sin(a),-.08]
  loop(c,.65,P,rot(.30,.20,a),.045)
  loop(c,.56,G,rot(.45,.18,a),.017)
 ell([0,0,.23],.52,G,ruffle=.025)
 for s in [-1,1]:
  for j in range(4):
   x=s*(2.18+.32*j);leaf([x,0,-.08],(.8,.35-.025*j,.12),P,rot(.2,.22,s*pi/2))
 loop([0,0,-.12],1.42,T,rot(.4,0,0),.028)

def prosopopoeia():
 for row in range(5):
  for col in range(6):
   x=-3.28+col*.74+(row%2)*.19;y=-1.23+row*.57
   if row==3 and col in [2,4]:continue
   if row==1 and col in [2,3,4]:continue
   box([x,y,-.12],[.35,.26,.18],P,.043)
 for x in [-1.8,-.35]:leaf([x,.49,.13],(.32,.075,.06),G)
 curve([[-1.93,-.59,.21],[-.92,-1.06,.3],[.28,-.6,.21]],G,.047)
 for j in range(4):
  x=np.linspace(.5,3.63,270);y=-.44+.26*j+.15*np.sin(x*2+j)
  tube(np.stack([x,y,np.full_like(x,.16)],-1),.025 if j%2 else .042,T if j%2 else G,20)

def prolepsis():
 x=np.linspace(-3.72,3.72,650);p=np.stack([x,-.8+.10*np.sin(x),np.zeros_like(x)],-1);ribbon(p,.16,P)
 for j,xx in enumerate([-3.1,-1.0,1.05,3.15]):
  if j<3:branch([xx,-.59,.1],.73,T)
  else:
   line([xx,-.57,.1],[xx,.5,.1],.045,S)
   for yy in [-.19,.1,.32]:line([xx,yy,.1],[xx-.3,yy+.23,.1],.032,S)
 curve([[3.1,.57,.15],[.31,1.89,.4],[-2.55,.54,.3]],G,.028)
 frame([-2.52,.76,.36],.35,.37,G)
 for a,b in [((0,-.25),(0,.22)),((0,0),(-.18,.15)),((0,.13),(.17,.3))]:line([-2.52+a[0],.76+a[1],.4],[-2.52+b[0],.76+b[1],.4],.021,S)

def prohairesis():
 for j in range(7):
  x=np.linspace(-3.85,3.85,600);y=(j-3)*.44+.09*np.sin(x*3+j)
  # Storm curves bow around the limited protected region.
  y+=np.sign(y)*.26*np.exp(-x*x)
  tube(np.stack([x,y,np.full_like(x,-.2)],-1),.013,S,16)
 loop([0,0,.12],.92,G,rot(.25,.2,0),.045,arc=(.22,2*pi-.22))
 leaf([-.76,-.06,.2],(.94,.22,.13),P,rot(0,.4,pi/2+.14));leaf([.76,-.06,.2],(.94,.22,.13),P,rot(0,-.4,pi/2-.14))
 box([0,-.57,.17],[.29,.11,.19],G,.045)
 leaf([0,.08,.2],(.56,.17,.13),G,rot(0,0,pi/2))
 leaf([.045,.04,.34],(.28,.072,.02),P,rot(0,0,pi/2))

def rhizome():
 xs=np.linspace(-3.6,3.6,650);p=np.stack([xs,.24*np.sin(xs*2),.15*np.sin(xs*1.2)],-1);tube(p,.13,G,30)
 for j,x in enumerate(np.linspace(-3.15,3.15,9)):
  y=.24*np.sin(x*2);ell([x,y,.1],.19,G,scale=(1.35,.88,.95))
  s=(-1)**j
  curve([[x,y,.05],[x+s*.6,y-.7,-.1],[x+s*.43,-1.39,.05]],T,.036)
  curve([[x,y,.1],[x-.35,y+.6,.1],[x+.14,1.14+.1*np.cos(j),.1]],M,.04)
  leaf([x+.13,1.02+.1*np.cos(j),.18],(.3,.13,.05),M,rot(0,0,.6*(-1)**j))
 for a,b in [(-2.2,-.7),(.2,1.8)]:curve([[a,.18,.1],[(a+b)/2,-.8,.15],[b,-.18,.1]],G,.085)

def house(c,sz=1,col=P):
 x,y,z=c;box([x,y-.18*sz,z],[.45*sz,.37*sz,.2*sz],col,.04*sz)
 for s in [-1,1]:line([x+s*.52*sz,y+.19*sz,z+.1],[x,y+.68*sz,z+.1],.065*sz,G)
 box([x,y-.27*sz,z+.22*sz],[.10*sz,.22*sz,.025*sz],T,.018*sz)
def simulacrum():
 house([0,.2,.24],.82,G);frame([0,.24,.04],.79,.98,P)
 for x,y,sz in [(-2.77,-.1,1.16),(2.77,-.1,1.16),(-1.31,1.05,.46),(1.31,1.05,.46)]:house([x,y,-.05],sz,P)
 for s in [-1,1]:
  curve([[s*.79,-.6,.1],[s*1.5,-1.42,.2],[s*2.68,-.85,.1]],G,.03)
  cone([s*2.50,-.93,.1],[s*2.7,-.83,.1],.09,G)
 for x in [-2.77,2.77]:loop([x,-1.08,0],.53,S,rot(pi/2,0,0),.017)

def syncretism():
 cols=[G,T,C]
 for j,col in enumerate(cols):
  yy=(j-1)*1.14;t=np.linspace(0,1,700);x=-3.83+7.66*t
  env=(1-np.minimum(t*2,1))*yy;y=env+.32*np.sin(t*5*pi+j*2*pi/3)*np.minimum(t*2,1)
  z=.25*np.cos(t*5*pi+j*2*pi/3)*np.minimum(t*2,1)
  p=np.stack([x,y,z],-1)
  if j==0:ribbon(p,.09,col,twist=1.6)
  else:tube(p,.066,col,28,ripple=.05*j)
  for u in [.08,.25,.50,.75,.95]:
   k=int(u*(len(p)-1));ell(p[k],.11,col,scale=(1.3,.9,.9))

def syzygy():
 ell([-2.91,.05,0],1.08,G,ruffle=.015)
 for r in [1.2,1.32,1.45]:loop([-2.91,.05,-.1],r,G,rot(.1,.06,0),.009)
 ell([.41,.05,0],.57,B,ruffle=.007)
 for j in range(4):
  loop([.41,.05,.04],.58,T,rot(.5+j*.36,.42,0),.02,arc=(.2,2.9))
 ell([2.92,.05,0],.25,P,ruffle=.035)
 for x0,x1 in [(-1.65,-.32),(1.12,2.56)]:
  line([x0,.05,-.22],[x1,.05,-.22],.013,S)
 for a in [-1,1]:curve([[.41+a*.63,-.2,.06],[.41+a*.96,.05,.06],[.41+a*.63,.31,.06]],T,.018)

def teleopoiesis():
 for s in [-1,1]:
  box([s*3.27,-.83,0],[.70,.18,.42],P,.065)
  for k in range(4):line([s*(2.76+.33*k),-1.08,0],[s*(2.76+.33*k),-1.54,0],.038,S)
 for j in range(7):
  x=-2.76+.4*j;y=-.45+.19*j-.022*j*j
  R=rot(.1,-.2,(-1)**j*.21)
  plate([x,y,.18],.22,.23,P,R)
  line([x-.18,y+.19,.23],[x+.18,y-.19,.23],.01,G)
 for j in range(6):ell([.40+j*.17,.23-.035*j,.2],.038-.003*j,G)
 leaf([2.94,-.14,.1],(.42,.2,.05),T,rot(.1,0,.28))
 curve([[2.56,-.1,.1],[2.35,.37,.2],[1.98,.38,.15]],T,.021)

def zeugma():
 loop([0,.57,.25],.33,G,th=.08)
 curve([[-.23,.35,.2],[-1.72,.12,.1],[-2.5,-.23,.08]],G,.059)
 curve([[.23,.35,.2],[1.72,.12,.1],[2.5,-.23,.08]],G,.059)
 box([-2.56,-.56,0],[.72,.52,.23],P,.12)
 arch([-2.56,-.08,.0],.25,.39,G)
 for xx in [-2.92,-2.22]:box([xx,-.54,.25],[.041,.48,.014],T,.012)
 leaf([2.35,-.36,.1],(.75,.24,.1),T,rot(0,.15,.62));leaf([3.03,-.37,.1],(.75,.24,.1),T,rot(0,-.15,-.62))
 ell([2.67,-.41,.15],.15,G,scale=(1,1.5,.9))
 for x,y in [(1.25,.9),(2.12,1.22),(3.29,.85)]:
  curve([[x-.2,y,.0],[x,y+.21,.05],[x+.17,y,0]],P,.027)

FUNCS={75:holophrasis,76:homoioteleuton,77:hypostasis,78:hypotaxis,79:iconotext,80:illeism,81:immanence,82:incommensurability,83:indexicality,84:interpellation,85:isomorphism,86:kairos,87:kenosis,88:logopoeia,89:mereology,90:metanoia,91:metempsychosis,92:mimesis,93:monadology,94:noesis,95:noema,96:noumenon,97:ontogenesis,98:paradiastole,99:paronomasia,100:peripeteia,101:pharmakon,102:pleroma,103:prosopopoeia,104:prolepsis,105:prohairesis,106:rhizome,107:simulacrum,108:syncretism,109:syzygy,110:teleopoiesis,111:zeugma}
if __name__=='__main__':
 ids=[int(x) for x in sys.argv[1:] if x.isdigit()] or list(FUNCS)
 for i in ids:
  parts.clear();f=FUNCS[i];f();save(f'{i:03d}-{f.__name__}',proof='--proof' in sys.argv)
