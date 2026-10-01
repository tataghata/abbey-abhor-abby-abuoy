"""Thirty-seven original concept sculptures; procedural local geometry, no image model."""
from artlib import *
import argparse

def path(x,y,z=0):
 x=np.asarray(x);return np.stack([x,np.broadcast_to(y,x.shape),np.broadcast_to(z,x.shape)],axis=-1)
def bez(a,b,c,d,n=200):
 t=np.linspace(0,1,n)[:,None];return (1-t)**3*np.array(a)+3*t*(1-t)**2*np.array(b)+3*t*t*(1-t)*np.array(c)+t**3*np.array(d)
def frame(cx,cy,w,h,col='pearl',z=0,r=.045):
 for a,b in [((cx-w,cy-h,z),(cx+w,cy-h,z)),((cx+w,cy-h,z),(cx+w,cy+h,z)),((cx+w,cy+h,z),(cx-w,cy+h,z)),((cx-w,cy+h,z),(cx-w,cy-h,z))]:line(a,b,r,col)
def ellipse(cx,cy,rx,ry,col='pearl',z=0,r=.035,arc=(0,2*np.pi)):
 t=np.linspace(*arc,250);tube(path(cx+rx*np.cos(t),cy+ry*np.sin(t),z),r,color(col),24)
def leaf(center,length,width,col='teal',rotation=None,open=.25):
 u=np.linspace(0,1,100);v=np.linspace(-1,1,35);U,V=np.meshgrid(u,v,indexing='ij')
 p=np.stack([(U-.5)*length,np.sin(np.pi*U)*V*width,open*np.sin(np.pi*U)*(1-V*V)],axis=-1)
 n=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)));n[n[:,:,2]<0]*=-1
 if rotation is not None:p=p@rotation.T;n=n@rotation.T
 addgrid(p+center,n,color(col))
def smallperson(x,y,c='pearl',s=1,z=0):
 sphere([x,y+.30*s,z],.11*s,c);line([x,y+.12*s,z],[x,y-.25*s,z],.055*s,c)
 for a in [-1,1]:line([x,y-.16*s,z],[x+a*.15*s,y-.48*s,z],.035*s,c);line([x,y+.04*s,z],[x+a*.18*s,y-.11*s,z],.033*s,c)
def tile(x,y,c='pearl',sx=.28,sy=.38,z=0,angle=0):box([x,y,z],[sx,sy,.075],c,.04,rot(.13,-.15,angle))

def concrescence():
 # Contributions become one leaf event; their different veins stay legible.
 R=rot(.22,-.10,.22);leaf([1.50,0,0],4.25,1.12,'pearl',R,.28)
 cols=['gold','teal','coral','violet','blue','mint']
 for j,c in enumerate(cols):
  yy=-1.28+j*.51;pp=bez([-3.85,yy,-.1],[-2.2,yy,.3],[-.8,.08,0],[2.7,.50,.34],240)
  tube(pp,.043,c,24)
  sphere(pp[0],.115,c)
  for k in [80,120,165]:
   p=pp[k];tube(bez(p,p+[.1,.1,.03],p+[.3,(-1)**j*.4,.05],p+[.45,(-1)**j*.52,.08],70),.018,c,16)

def conatus():
 for x,y,a in [(-.3,1.12,.12),(.10,-1.08,-.13),(1.30,.96,-.12),(1.45,-.94,.09),(-1.42,.95,.14),(-1.22,-1.13,-.09)]:box([x,y,-.05],[.62,.41,.33],'silver',.09,rot(.1,.3,a))
 p=bez([-3.80,-1.02,0],[-1.7,-.80,.3],[-1.6,.80,.4],[3.75,1.14,.1],350);tube(p,np.linspace(.17,.027,len(p)),'gold',32)
 for k in range(25,300,27):
  q=p[k];sg=(-1)**k;tube(bez(q,q+[.22,-.25,.05],q+[.31,-.42,.08],q+[.52,-.46,.09],60),np.linspace(.035,.005,60),'pearl',16)
 leaf([3.32,1.17,.10],.9,.25,'mint',rot(.3,0,.55),.08)

def counterfactuality():
 for y in [-.85,.85]:
  for x in [-2.35,2.35]:box([x,y,-.18],[1.44,.16,.16],'silver',.05)
  for x in [-3.5,-2.8,-2.1,1.95,2.65,3.35]:sphere([x,y,.12],.07,'pearl')
  frame(-.32,y,.50,.42,'pearl',-.05,.044)
 box([-.3,.85,-.12],[.46,.12,.09],'gold',.025)
 box([-.71,-.44,-.12],[.12,.49,.09],'coral',.025,rot(0,0,-.28))
 arrow([.45,.85,.12],[1.16,.85,.12],.035,'gold');arrow([-1.30,-.85,.12],[-.94,-.85,.12],.035,'coral')
 # Identical environmental anchors isolate one causal difference.
 for y in [-.85,.85]:ring([-3.58,y,.2],.15,'teal',thick=.025)

def defamiliarization():
 # Familiar spoon becomes a huge landscape of metallic contour and one liquid planet.
 u=np.linspace(0,np.pi/2,100);v=np.linspace(0,2*np.pi,150);U,V=np.meshgrid(u,v,indexing='ij')
 p=np.stack([-1.65+1.72*np.sin(U)*np.cos(V),1.17*np.sin(U)*np.sin(V),-.50*np.cos(U)],axis=-1)
 n=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)));n[n[:,:,2]<0]*=-1;addgrid(p,n,color('pearl'))
 ellipse(-1.65,0,1.72,1.17,'silver',0,.06)
 pp=bez([-.06,.0,-.04],[1.1,.00,.08],[2.42,.26,.04],[3.85,.29,0],200);ribbon(pp,.19,'pearl',.13)
 sphere([-1.75,-.05,.10],.34,'teal',.005);ring([-1.75,-.05,-.08],.62,'teal',rot(.68,0,.2),.02)
 for x,y,r in [(-2.62,.28,.12),(-1.12,.42,.09),(-2.18,-.65,.06)]:sphere([x,y,.04],r,'gold')

def dehiscence():
 for j,cx in enumerate([-2.7,0,2.7]):
  angle=.04+j*.20
  for sign in [-1,1]:leaf([cx,sign*.06*j,-.06],1.95,.60,'gold' if sign==1 else 'mint',rot(.4*sign,-.18,sign*angle),.31)
  tube(bez([cx-.98,0,0],[cx-.2,.2,.2],[cx+.3,-.2,.2],[cx+.99,0,0],150),.028,'pearl',18)
  for k in range(3+j):
   xx=cx-.53+k*.24;yy=(k%2-.5)*.16+j*(k%2*.25);sphere([xx,yy,.32+j*.10],.095,'coral')
  if j==2:
   for xx,yy in [(3.38,.89),(3.7,1.29),(2.4,1.19)]:sphere([xx,yy,.1],.08,'gold');line([xx,yy,.1],[xx+.12,yy+.2,.1],.012,'pearl')

def derealization():
 # A coherent domestic interior recedes behind a detached planar screen.
 frame(0,.10,3.25,1.35,'silver',-.7,.036)
 box([0,-.67,-.15],[2.18,.10,.67],'pearl',.045,rot(.05,.12,0))
 for x in [-1.82,1.82]:line([x,-.65,-.13],[x,-1.30,-.10],.065,'silver')
 for x in [-2.70,2.70]:frame(x,.36,.32,.55,'silver',-.55,.035)
 ellipse(.23,-.52,.35,.11,'gold',.47,.02)
 # Foreground pane is a wavering outline, without equating detachment with hallucination.
 t=np.linspace(-1.60,1.60,300)
 for x in [-3.8,3.8]:tube(path(x+.025*np.sin(5*t),t,.50),.025,'teal',20)
 for y in [-1.6,1.6]:tube(path(np.linspace(-3.8,3.8,300),y+.022*np.sin(np.linspace(-3.8,3.8,300)*4),.5),.025,'teal',20)
 for x in [-.55,0,.55]:tube(path(x+.035*np.sin(t*4),t,.42),.009,(.29,.34,.40),12)

def diachronicity():
 line([-3.95,-1.1,-.3],[3.95,-1.1,-.3],.065,'gold')
 for j,cx in enumerate([-2.96,-.99,.99,2.96]):
  col=['pearl','coral','silver','teal'][j];box([cx,-.26,-.18],[.70,.78,.27],col,.035)
  if j==0:
   line([cx-.78,.54,.12],[cx,1.22,.12],.075,'gold');line([cx,1.22,.12],[cx+.78,.54,.12],.075,'gold')
  elif j==1:
   box([cx+.38,.93,-.2],[.12,.43,.15],'coral',.025)
  elif j==2:
   box([cx,.64,0],[.79,.10,.35],'gold',.03)
  else:
   box([cx,1.0,-.25],[.73,.48,.25],'teal',.025)
  for xx in [cx-.35,cx+.35]:
   for yy in [-.6,.10]:frame(xx,yy,.16,.20,'pearl',.14,.02)
  if j==3:
   for xx in [cx-.35,cx+.35]:frame(xx,1.0,.15,.22,'pearl',.05,.018)

def differance():
 for j in range(7):
  cx=-3.2+j*1.02;cy=.21*np.sin(j)
  frame(cx,cy,.42,1.16, ['silver','pearl'][j%2],-.40+j*.09,.014)
  t=np.linspace(.34+j*.12,5.25-j*.13,210);pp=path(cx+.35*np.cos(t),cy+.81*np.sin(t),-.18+j*.09);tube(pp,.042,['teal','gold','violet'][j%3],24)
  if j<6:line([cx+.48,cy,-.2],[cx+.86,.21*np.sin(j+1),-.2],.009,'silver')

def disanalogy():
 for cx in [-2.03,2.03]:
  line([cx,-1.16,0],[cx,.13,0],.115,'pearl');
  for s in [-1,1]:
   pp=bez([cx,-.08,0],[cx+s*.44,.35,.06],[cx+s*.5,.45,.06],[cx+s*.86,.97,.03],120)
   tube(pp,.075,'teal' if cx<0 else 'gold',24)
   for j in range(3):
    q=pp[35+j*23];line(q,q+[s*.43,.30,0],.035,'teal' if cx<0 else 'gold')
 if True:
  for y in [-.8,-.45,-.1]:ring([2.03,y,.04],.14,'coral',rot(np.pi/2,0,0),.025)
  # One consequential fracture makes the superficial correspondence fail.
  box([2.87,.94,.07],[.13,.08,.09],'coral',.015,rot(0,0,.7));arrow([.0,.2,0],[.57,.2,0],.032,'silver')
 for s in [-1,1]:tube(bez([-2.03,-1.16,0],[-2.1+s*.1,-1.26,.1],[-2.03+s*.5,-1.38,0],[-2.03+s*.83,-1.48,0],100),.055,'teal',20)

def dissensus():
 ellipse(0,.14,2.55,1.04,'silver',-.2,.065,arc=(.10,5.66))
 for t in np.linspace(.28,5.45,11):
  x=2.78*np.cos(t);y=1.14*np.sin(t);tile(x,y,'pearl',.14,.16,.08,-t)
 for x,y,c in [(3.60,-.7,'gold'),(2.78,-.20,'coral'),(1.83,-.83,'teal'),(.85,-.41,'violet')]:
  tile(x,y,c,.18,.19,.20,.2);line([x,y+.18,.2],[x,y+.41,.2],.045,c)
  arrow([x+.20,y-.2,.10],[x-.25,y-.12,.10],.022,c,.13)
 # Arrival alters the perimeter instead of just occupying assigned seats.
 tube(bez([2.5,-.46,-.2],[2.35,-1.6,-.15],[.92,-1.59,-.15],[.1,-.94,-.2],150),.033,'gold',22)

def dithyramb():
 x=np.linspace(-3.65,3.65,500)
 for j,c in enumerate(['coral','gold','violet','teal','pearl']):
  y=.54*np.sin(x*1.35+j*.8)+.13*x+(j-2)*.14;z=.22*np.cos(x*1.35+j*.8)
  ribbon(path(x,y,z),.075+j*.01,c,twist=np.pi*(1+j*.18),phase=j*.2)
 for j,x in enumerate(np.linspace(-3.25,3.25,9)):
  y=.78*np.sin(x*1.3)+.13*x;sphere([x,y+.23,.17],.10,['gold','pearl','coral'][j%3]);line([x,y+.12,.17],[x+.1,y-.20,.17],.034,'pearl')

def ekphrasis():
 frame(-2.04,0,1.46,1.30,'gold',-.15,.10)
 sphere([-2.1,.23,-.13],.46,'pearl',.035,squash=(.80,1.15,.3));box([-2.1,-.58,-.2],[.73,.36,.15],'silver',.07)
 for j,c in enumerate(['teal','pearl','coral']):
  p=bez([-1.65,-.30+j*.20,.15],[-.02,1.3-j*.2,.30],[1.2,-1.35+j*.30,.15],[3.82,.40+j*.32,.05],350);ribbon(p,.06,c,twist=j*.85)
 for x in [1.05,1.67,2.31,2.95,3.58]:sphere([x,.10+.36*np.sin(x*2.8),.2],.045,'gold')

def echolalia():
 for j,cx in enumerate([-2.72,0,2.72]):
  for k in range(3):ellipse(cx,.1,.28+k*.29,.46+k*.28,['teal','gold','coral'][j],-.06,.032,(-1.10,1.10))
  sphere([cx-.32,.10,.03],.15,['teal','gold','coral'][j])
  if j<2:arrow([cx+.97,-.91,.04],[cx+1.63,-.65,.04],.032,'pearl',.15)
 # Distinct response markers show reuse functioning in a changing context.
 tile(-2.95,-1.02,'teal',.22,.12);tile(-.28,-1.02,'gold',.32,.12);tile(2.35,-1.02,'coral',.42,.12)

def eidolon():
 box([0,-1.25,-.10],[2.9,.12,.57],'silver',.05,rot(.12,.15,0))
 for j in range(6):
  cx=(j-2.5)*.22;z=-.3+j*.1
  ellipse(cx,.60,.37+j*.025,.49,'pearl' if j==3 else 'silver',z,.018,(-.7,4.65))
  pp=bez([cx-.74,-1.04,z],[cx-.71,.0,z],[cx-.1,.25,z],[cx-.05,.18,z],120);tube(pp,.019,'silver',16)
  pp=bez([cx+.80,-1.04,z],[cx+.66,.04,z],[cx+.13,.24,z],[cx+.09,.17,z],120);tube(pp,.019,'silver',16)
 ring([-2.9,.30,-.1],.36,'gold',thick=.023,arc=(.1,4.6));ring([2.94,.30,-.1],.36,'gold',thick=.023,arc=(.3,4.8))

def ekstasis():
 frame(-1.75,0,1.20,1.04,'silver',-.3,.045)
 sphere([-1.76,0,-.14],.35,'pearl',.02)
 for j,c in enumerate(['teal','gold','violet','coral']):
  y=(j-1.5)*.39;p=bez([-1.75,y,-.05],[-.35,y*2,.22],[1.2,y*1.4,.42],[3.5,y*.55,.15],280);ribbon(p,.085,c,twist=np.pi*1.2,phase=j*.3)
 ring([2.66,0,.14],.84,'gold',rot(.44,-.38,.2),.035)
 sphere([2.71,0,.18],.16,'gold')

def elenchus():
 verts=[[-2.65,-.91,0],[-.4,1.19,0],[2.55,-.91,0]]
 for j,p in enumerate(verts):sphere(p,.23,['teal','gold','coral'][j])
 for j in range(3):
  a=np.array(verts[j]);b=np.array(verts[(j+1)%3]);v=norm(b-a);arrow(a+v*.35,b-v*.35,.049,'pearl',.24)
 arrow([1.29,-.82,.30],[-.73,-.82,.30],.043,'coral',.24)
 for x in [-3.7,3.7]:ring([x,.06,0],.28,'silver',thick=.022)
 sphere([-.5,-.87,.30],.13,'coral');line([-.61,-.98,.48],[-.37,-.73,.48],.024,'pearl');line([-.61,-.73,.48],[-.37,-.98,.48],.024,'pearl')

def enallage():
 for j,x in enumerate(np.linspace(-3.55,3.55,8)):
  if j!=4:tile(x,0,'pearl',.31,.44,0)
  else:sphere([x,0,.05],.37,'gold',.02)
  if j<7:line([x+.40,0,-.12],[x+.63,0,-.12],.034,'silver')
 tile(.50,1.10,'gold',.31,.32,-.06,.25)
 arrow([.54,.83,.08],[.51,.52,.08],.03,'gold',.14)
 arrow([.67,-.54,.08],[1.28,-1.14,.08],.033,'coral',.14)
 tile(1.68,-1.13,'silver',.25,.30,-.05,-.15)

def energeia():
 for cx in [-2.22,2.10]:
  t=np.linspace(0,np.pi,220);upper=path(cx+1.13*np.cos(t),.67*np.sin(t),.07);lower=path(cx+1.13*np.cos(t),-.67*np.sin(t),.07)
  tube(upper,.055,'pearl',24)
  if cx>0:tube(lower,.055,'pearl',24);sphere([cx,0,.08],.36,'teal');sphere([cx,0,.39],.13,'gold')
  else:line([cx-1.13,0,.07],[cx+1.13,0,.07],.055,'silver')
 for j in range(5):
  yy=-1.3+j*.65;line([3.85,yy,-.08],[3.14,yy*.45,.06],.024,'gold')
 arrow([-.49,-.98,.0],[.36,-.98,.0],.032,'gold',.18)

def entelechy():
 # A completed lyre at rest: possessed capacity without compulsory performance.
 for x in [-1.22,1.22]:tube(bez([x,-1.03,0],[x*1.6,-.10,0],[x*1.1,1.16,0],[x*.73,1.25,0],150),.15,'pearl',32)
 box([0,-1.0,-.05],[1.30,.24,.28],'gold',.14)
 line([-.99,1.24,0],[.99,1.24,0],.10,'gold')
 for x in np.linspace(-.79,.79,9):line([x,-.79,.11],[x,1.22,.10],.009,'silver')
 for cx in [-3.12,3.12]:ring([cx,0,0],.41,'teal',rot(.3,.3,0),.025)
 line([-3.12,-.41,0],[-3.12,.41,0],.02,'teal');line([2.71,0,0],[3.53,0,0],.02,'teal')

def enthymeme():
 # Reasoning bridge whose central load-bearing assumption is deliberately singled out.
 for x in [-3.03,3.03]:box([x,-.37,-.02],[.55,.85,.25],'pearl',.08)
 p=bez([-3.02,.42,.06],[-1.3,1.42,.06],[1.3,1.42,.06],[3.02,.42,.06],400)
 for i,j in [(0,155),(245,400)]:tube(p[i:j],.12,'teal',32)
 tube(p[155:245],.115,'gold',32)
 for x in [-.66,.66]:ring([x,1.13,.13],.18,'gold',rot(0,np.pi/2,0),.03)
 for x in [-1.22,-.65,0,.65,1.22]:line([x,-.83,-.16],[x,-.36,-.16],.016,'silver')
 arrow([0,-.27,.03],[0,.78,.03],.035,'gold',.20)

def epanalepsis():
 for cx in [-3.49,3.49]:ring([cx,.0,.02],.41,'gold',thick=.09);sphere([cx,0,.04],.13,'teal')
 x=np.linspace(-2.94,2.94,500);tube(path(x,.63*np.sin(x*1.48),.1*np.sin(x*2.9)),.048,'pearl',26)
 for j,x in enumerate(np.linspace(-2.6,2.6,9)):sphere([x,.63*np.sin(x*1.48),.1*np.sin(x*2.9)],.09,['teal','violet','coral'][j%3])
 tube(bez([3.43,-.48,-.18],[2.45,-1.62,-.18],[-2.45,-1.62,-.18],[-3.43,-.48,-.18],200),.018,'gold',18)

def epenthesis():
 for j,x in enumerate([-3.35,-2.30,-1.25,1.25,2.30,3.35]):
  tile(x,0,'pearl',.37,.48,0)
  if j!=2 and j!=5:line([x+.37,0,0],[x+.68,0,0],.043,'silver')
 sphere([0,0,.07],.32,'gold',.06)
 for s in [-1,1]:tube(bez([s*.90,0,0],[s*.75,0,.1],[s*.5,0,.1],[s*.37,0,.08],70),.06,'gold',24)
 sphere([0,1.20,.05],.20,'gold');arrow([0,.88,.05],[0,.46,.05],.026,'gold',.15)
 for x in [-3.35,3.35]:ring([x,-.92,.05],.16,'teal',thick=.027)

def epiphenomenon():
 # A driven lower assembly and dependent upper halo; influence is shown one way.
 for cx in [-2.6,-.83,.94,2.71]:
  ring([cx,-.62,0],.55,'pearl',rot(.12,.2,0),.08)
  for t in np.linspace(0,2*np.pi,8,endpoint=False):line([cx,-.62,0],[cx+.5*np.cos(t),-.62+.5*np.sin(t),0],.025,'silver')
 line([-3.63,-.63,-.07],[3.65,-.63,-.07],.045,'gold')
 for cx in [-2.3,0,2.3]:arrow([cx,.06,-.2],[cx,.48,-.2],.02,'silver',.12)
 t=np.linspace(-3.6,3.6,450);ribbon(path(t,.93+.14*np.cos(t*1.4),.1*np.sin(t*2)),.055,'violet',twist=np.pi)

def episteme():
 for cx in [-2.05,2.05]:frame(cx,0,1.51,1.16,'gold',-.12,.044)
 for j,x in enumerate([-2.99,-2.05,-1.11]):
  for k,y in enumerate([-.69,0,.69]):
   tile(x,y,['teal','pearl','coral'][k],.20,.18,.05)
 for j,x in enumerate([1.12,2.05,2.98]):
  for k,y in enumerate([-.69,0,.69]):
   sphere([x,y,.05],.15,['teal','pearl','coral'][j]);
 for y in [-.34,.34]:line([-3.45,y,-.05],[-.65,y,-.05],.023,'silver')
 for x in [1.58,2.52]:line([x,-1.06,-.05],[x,1.06,-.05],.023,'silver')
 arrow([-.33,0,0],[.33,0,0],.023,'gold',.14)

def epizeuxis():
 # Adjacency, exact identity, and heightened pulse: no intervening units.
 for cx in [-2.25,0,2.25]:
  u=np.linspace(.06,1,90);v=np.linspace(0,2*np.pi,140);U,V=np.meshgrid(u,v,indexing='ij');rr=.24+.48*U*U
  p=np.stack([cx+rr*np.cos(V),.86-1.62*U,rr*np.sin(V)],axis=-1);n=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)));addgrid(p,n,color('gold'))
  ring([cx,-.76,0],.72,'pearl',rot(np.pi/2,0,0),.04);sphere([cx,-.83,.05],.13,'coral');ring([cx,.95,0],.17,'gold',thick=.045)

def equifinality():
 box([3.04,-.32,-.08],[.65,.88,.30],'pearl',.1)
 for j,c in enumerate(['coral','gold','teal']):
  y0=-1.15+j*1.15;x=np.linspace(-3.8,2.85,430);u=(x+3.8)/6.65
  if j==0:y=y0*(1-u)+.18*np.sin(u*5*np.pi)*(1-u)
  elif j==1:y=.8*np.sin(np.pi*u)**2
  else:y=y0*(1-u)-.48*np.sin(np.pi*u*2)*(1-u)
  tube(path(x,y,.35+.13*np.sin(np.pi*u+j)),.055,c,28);sphere([x[0],y[0],.36],.12,c)
 ring([3.05,0,.36],.36,'gold',thick=.038);sphere([3.05,0,.35],.14,'teal')

def eschaton():
 for j in range(7):
  x=-3.55+j*.75;scale=.20+j*.07
  box([x,-.34+j*.03,-.1],[.20,.07,scale],'silver' if j<4 else 'pearl',.025,rot(.12,.25,0))
 p=bez([-3.88,-.66,-.03],[-2.22,-.74,0],[.68,-.17,0],[3.08,0,0],300);ribbon(p,.26,'pearl',.08)
 for k,r in enumerate([1.42,1.14,.85]):ellipse(2.55,.08,r*.60,r,'gold' if k==0 else 'pearl',-.08+k*.13,.026)
 for j in range(11):
  a=-1.45+j*.29;line([2.55+.70*np.cos(a),.08+1.32*np.sin(a),-.24],[3.92,.09+1.30*np.sin(a),-.24],.01,'gold')

def eucatastrophe():
 p=bez([-3.82,1.10,0],[-2.3,.6,.12],[-1.9,-1.32,.13],[.02,-1.29,.10],250);ribbon(p,.13,'silver',.65)
 p=bez([.02,-1.29,.10],[.64,-1.30,.21],[.50,1.10,.16],[3.78,1.14,.12],290);ribbon(p,.145,'gold',-.5)
 for x in [-1.5,-.80,-.10,.60,1.3]:box([x,-1.53,-.30],[.22,.12,.22],'coral',.04,rot(.15,.20,x*.15))
 # A prepared outside strand joins at the reversal, making the turning point concrete.
 pp=bez([3.75,-.40,-.04],[2.10,-.90,.1],[1.30,-1.1,.1],[.21,-1.18,.13],230);tube(pp,.048,'teal',28)
 sphere([.21,-1.18,.19],.14,'gold')

def exaptation():
 # One inherited feather structure acquires a new lifting relation.
 for cx,ang in [(-2.22,.32),(1.69,-.10)]:
  R=rot(.1,.2,ang);center=np.array([cx,0,0]);shaft=np.array([[-1.15,0,0],[1.15,0,0]])@R.T+center;line(shaft[0],shaft[1],.047,'gold')
  for j,t in enumerate(np.linspace(-.95,.94,23)):
   width=.77*(1-(t/1.2)**2)
   for s in [-1,1]:
    a=np.array([t,0,.03])@R.T+center;b=np.array([t+.26,s*width,.06])@R.T+center;line(a,b,.026,'pearl' if cx<0 else 'teal')
 if True:
  for y in [-1.25,-1.0]:tube(bez([.35,y,-.1],[1.5,y+.20,.02],[2.72,y+.25,.02],[3.76,y+.35,0],200),.023,'silver',20)
  arrow([1.95,-.70,.05],[1.95,.15,.05],.033,'gold',.19)

def exergue():
 sphere([-.58,0,-.07],1.48,'gold',.004,rot(0,.12,0),squash=(1,1,.17))
 ring([-.58,0,.24],1.39,'pearl',thick=.035)
 # Upper relief: a stylized branch, deliberately no fake inscription.
 line([-.72,-.42,.27],[-.42,.79,.27],.045,'pearl')
 for j in range(5):
  y=-.27+j*.22
  for s in [-1,1]:leaf([-.57+s*.20,y+.12,.26],.52,.13,'pearl',rot(0,0,s*.52),.04)
 line([-1.67,-.81,.23],[.49,-.81,.23],.028,'coral')
 for x in np.linspace(-1.28,.09,10):line([x,-1.16,.23],[x,-.95,.24],.019,'silver')
 # Magnified companion compartment gives the marginal field interpretive weight.
 frame(2.71,-.23,.88,.42,'gold',.03,.043)
 line([.59,-.89,.05],[1.75,-.60,.05],.018,'pearl');line([.83,-.63,.05],[1.75,.12,.05],.018,'pearl')

def exophora():
 R=rot(.15,-.20,-.08)
 for c in [(-2.47,-.19,0),(-1.02,-.19,0)]:box(c,[.68,.87,.045],'pearl',.024,R)
 for y in np.linspace(-.66,.28,5):line([-2.96,y,.18],[-2.11,y,.18],.012,'silver')
 frame(2.6,.08,.95,1.24,'gold',-.08,.09);line([2.6,-1.11,-.08],[2.6,1.29,-.08],.041,'pearl');line([1.67,.11,-.08],[3.53,.11,-.08],.041,'pearl')
 p=bez([-1.26,-.07,.20],[.11,1.05,.25],[.81,.82,.25],[2.4,.36,.20],220);tube(p,.053,'teal',30);cone(p[-15],p[-1],.18,'teal')

def facticity():
 box([-2.31,-.86,-.07],[1.10,.25,.56],'silver',.08,rot(.16,.14,0))
 for x in [-3.11,-2.46,-1.81]:
  tube(bez([x,-.86,0],[x-.1,-1.20,.12],[x+.20,-1.36,.10],[x+.29,-1.54,0],80),.045,'gold',20)
 smallperson(-2.25,.14,'pearl',1.36,.10)
 for j,c in enumerate(['gold','teal','coral']):
  p=bez([-1.24,-.64,.03],[.15,-.41,.04],[.59,(j-1)*1.22,.07],[3.73,(j-1)*1.20,.02],220);ribbon(p,.09,c,twist=(j-1)*.26)
  if j==2:box([1.48,.80,.01],[.20,.36,.21],'silver',.05)

def fissiparity():
 # Three distinct viable stages, not arbitrary breakage.
 sphere([-2.70,0,0],.66,'teal',.006,rot(.1,.12,0),squash=(1.56,.74,.45))
 for cx in [-.49,.49]:sphere([cx,0,0],.47,'teal',.006,squash=(1.05,.85,.47))
 line([-.17,0,0],[.17,0,0],.075,'gold')
 for cy in [-.62,.62]:sphere([2.82,cy,0],.47,'teal',.006,rot(0,.1,.13),squash=(1.57,.76,.45))
 for cx,cy in [(-3.4,.03),(-.74,.03),(.74,.03),(2.26,-.59),(2.26,.65)]:
  for yy in [-.095,.095]:sphere([cx,cy+yy,.30],.035,'gold')
 arrow([-1.69,-1.02,0],[-.85,-1.02,0],.025,'pearl',.15);arrow([.78,-1.02,0],[1.69,-1.02,0],.025,'pearl',.15)

def fulguration():
 pts=np.array([[-1.8,1.48,.03],[-1.35,.96,.03],[-1.62,.78,.03],[-.61,.27,.03],[-.82,.09,.03],[.44,-.60,.03],[.2,-.75,.03],[1.13,-1.36,.03]])
 for j in range(len(pts)-1):line(pts[j],pts[j+1],.034 if j<4 else .024,'pearl')
 for k,end in [(1,[-3.34,.76,.0]),(3,[1.61,.39,0]),(4,[-2.8,-.83,0]),(5,[2.7,-1.01,0])]:
  a=pts[k];b=np.array(end);m=(a+b)/2+np.array([.1,.22,0]);line(a,m,.018,'gold');line(m,b,.011,'pearl')
 for j,x in enumerate(np.linspace(-3.9,3.9,39)):
  h=.10+.20*(.5+.5*np.sin(j*2.8));line([x,-1.57,-.06],[x+.06*np.sin(j),-1.57+h,-.06],.007,'teal')

def gnosis():
 # Recognition reorganizes the same chamber; no factual supernatural claim.
 frame(-.4,0,3.2,1.44,'silver',-.30,.06)
 for i in range(5):frame(-1.40+i*.32,.01,1.05-i*.11,1.23-i*.13,'pearl' if i<4 else 'gold',-.2+i*.12,.037)
 for j,y in enumerate([-.76,0,.76]):
  p=bez([-.10,y,.08],[.98,y*.6,.08],[2.08,y*1.6,.09],[3.40,y*1.7,.06],180);tube(p,.023,'gold',20)
 for x,y,c in [(1.63,.76,'teal'),(2.41,-.55,'coral'),(2.88,.60,'pearl')]:tile(x,y,c,.21,.25,.08,.09)

def hendiadys():
 # Two equal coordinated ribbons make one draped surface.
 x=np.linspace(-3.64,3.64,600);u=(x+3.64)/7.28
 for j,c in enumerate(['gold','teal']):
  yy=(j-.5)*.37+.48*np.sin(u*2*np.pi);zz=(1 if j==0 else -1)*.24*np.sin(u*4*np.pi)
  ribbon(path(x,yy,zz),.25,c,twist=np.pi*1.3,phase=j*np.pi)
 for x in [-3.66,3.66]:line([x,-.92,-.09],[x,.92,-.09],.056,'pearl')
 # The same common hem physically joins the parallel terms.
 p=bez([-3.62,-.42,.03],[-1.55,-1.48,.02],[1.55,-1.48,.02],[3.62,-.42,.03],280);tube(p,.031,'pearl',20)

def heterotopia():
 for cx in [-2.9,-.98,.98,2.9]:frame(cx,0,.90,1.24,'pearl',-.22,.035)
 # Garden, ship, archive, memorial: different institutions/times under one roof.
 line([-3.0,-.95,0],[-3.0,.22,0],.055,'gold')
 for x,y in [(-3.24,.18),(-2.85,.49),(-3.03,.76)]:sphere([x,y,.0],.25,'teal',.035,squash=(1,1,.5))
 tube(bez([-1.67,-.28,.05],[-1.5,-1.02,.08],[-.4,-1.02,.08],[-.27,-.28,.05],160),.056,'gold',24);line([-.97,-.50,.04],[-.97,.88,.04],.037,'gold');leaf([-.80,.32,.08],.89,.34,'pearl',rot(.03,0,1.25),.08)
 for x in [.48,.80,1.12,1.44]:
  for y in [-.62,.0,.62]:tile(x,y,['coral','gold','silver'][int((y+.62)/.62)],.10,.19,.03)
 box([2.91,-.60,.0],[.54,.18,.22],'silver',.045);sphere([2.91,.28,0],.30,'pearl',.025,squash=(.7,1.3,.5))
 line([-3.89,1.38,-.24],[3.89,1.38,-.24],.053,'gold')
 for x in [-1.94,0,1.94]:line([x,-1.23,-.17],[x,-.79,-.17],.085,'gold')

FUNCS={38:concrescence,39:conatus,40:counterfactuality,41:defamiliarization,42:dehiscence,43:derealization,44:diachronicity,45:differance,46:disanalogy,47:dissensus,48:dithyramb,49:ekphrasis,50:echolalia,51:eidolon,52:ekstasis,53:elenchus,54:enallage,55:energeia,56:entelechy,57:enthymeme,58:epanalepsis,59:epenthesis,60:epiphenomenon,61:episteme,62:epizeuxis,63:equifinality,64:eschaton,65:eucatastrophe,66:exaptation,67:exergue,68:exophora,69:facticity,70:fissiparity,71:fulguration,72:gnosis,73:hendiadys,74:heterotopia}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('ids',nargs='*',type=int);parser.add_argument('--proof',action='store_true');args=parser.parse_args()
 for index in args.ids or FUNCS:
  parts.clear();func=FUNCS[index];func();save(f'{index:03d}-{func.__name__}',args.proof)
