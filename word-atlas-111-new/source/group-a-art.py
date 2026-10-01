"""Thirty-seven new concept sculptures, rendered locally with deterministic geometry."""
from artlib import *
from scipy.interpolate import CubicSpline
import argparse
PALETTE=['gold','teal','violet','coral','blue','pearl','mint']
def path(points,n=300):
 p=np.array(points,dtype=float);t=np.linspace(0,1,len(p));return CubicSpline(t,p)(np.linspace(0,1,n))
def strand(points,c='gold',r=.045):tube(path(points),r,color(c),24)
def rect(c,w,h,col='pearl',thick=.035):
 x,y,z=c
 for a,b in [((x-w,y-h,z),(x+w,y-h,z)),((x+w,y-h,z),(x+w,y+h,z)),((x+w,y+h,z),(x-w,y+h,z)),((x-w,y+h,z),(x-w,y-h,z))]:line(a,b,thick,col)
def bead(c,r=.16,col='gold'):sphere(c,r,col,.022)
def gear(c,r,col,teeth=12,phase=0,thick=.06):
 t=np.linspace(0,2*np.pi,600);rr=r*(1+.075*np.cos(teeth*t+phase));p=np.stack([rr*np.cos(t),rr*np.sin(t),np.zeros_like(t)],-1)+c;tube(p,thick,color(col),24)
 ring(c,r*.72,col,thick=.018)
def plate(c,half,col,R=None):box(c,half,col,min(half)*.28,R)
def beamchain(points,c='pearl',r=.06):
 for a,b in zip(points,points[1:]):line(a,b,r,c)
 for p in points:bead(p,r,c)
def ell(c,rx,ry,col,thick=.04,zamp=0):
 t=np.linspace(0,2*np.pi,400);p=np.stack([rx*np.cos(t),ry*np.sin(t),zamp*np.sin(t*2)],-1)+c;tube(p,thick,color(col),24)
def surface(x,y,z,c):
 p=np.stack([x,y,z],-1);n=norm(np.cross(np.gradient(p,axis=0),np.gradient(p,axis=1)));n[n[:,:,2]<0]*=-1;addgrid(p,n,color(c))
def ablaut():
 for j,(x,col) in enumerate(zip([-2.6,0,2.6],['gold','teal','coral'])):
  # Same inherited casing; differently shaped internal vowel chambers.
  for zz in [-.28,.28]:ell([x,0,zz],.87,1.23,'pearl',.045)
  for yy in [-1.17,1.17]:line([x,yy,-.28],[x,yy,.28],.047,'pearl')
  u=np.linspace(0,np.pi,140);v=np.linspace(0,2*np.pi,100);U,V=np.meshgrid(u,v,indexing='ij')
  rr=.52*np.sin(U)*(1+.22*np.cos((j+1)*U+.4*j));X=x+rr*np.cos(V);Y=1.02*np.cos(U);Z=.1+rr*np.sin(V);surface(X,Y,Z,col)
  ring([x,0,.17],.61,col,rot(.7,.2,.25*j),.026)
 strand([[-3.8,-1.48,-.5],[-1.6,-1.35,-.5],[1.6,-1.35,-.5],[3.8,-1.48,-.5]],'silver',.019)
def aboulia():
 # An elaborate intact preparation with one initiating gap.
 plate([0,-1.25,-.1],[3.45,.11,.5],'silver')
 for x in [-2.9,2.9]:plate([x,.03,-.14],[.10,1.16,.28],'pearl')
 plate([0,1.17,-.14],[3.0,.10,.28],'pearl')
 for x,r,c in [(-2.1,.52,'teal'),(-.85,.64,'gold'),(1.32,.88,'pearl')]:
  gear([x,-.03,.04],r,c,14);bead([x,-.03,.04],.11,c)
  for a in np.linspace(0,2*np.pi,5)[:-1]:line([x,-.03,.04],[x+r*.64*np.cos(a),-.03+r*.64*np.sin(a),.04],.024,c)
 strand([[-.29,-.04,.1],[.12,.28,.35],[.4,.77,.35],[.32,1.0,.15]],'coral',.066)
 bead([.47,-.04,.1],.10,'gold');ring([.22,1.0,.15],.11,'coral',thick=.032)
 arrow([-3.7,-.03,.12],[-3.06,-.03,.12],.039,'teal',.17)
def acatalepsy():
 for k in range(4):
  y=-.85+k*.49;strand([[-3.4,y,-.2],[-2.65,y,.05],[-1.93,y*.88,.48],[-1.57,y*.74,.22]],'gold',.11)
 strand([[-3.25,-1.12,-.1],[-2.4,-1.25,.08],[-1.5,-.85,.38]],'gold',.15)
 for j,(x,y,r,c) in enumerate([(.1,.1,.82,'pearl'),(1.95,.67,.58,'silver'),(2.35,-.84,.39,'teal')]):
  plate([x,y,0],[r,r,.20],c,rot(.2,.4,.77))
  for a in np.linspace(0,2*np.pi,7)[:-1]:line([x,y,.4],[x+r*1.25*np.cos(a),y+r*1.25*np.sin(a),-.1],.015,c)
 for x in [1.18,3.24]:line([x,-1.42,-.7],[x,1.43,-.7],.028,'violet')
def acedia():
 rect([0,0,-.55],2.0,1.38,'silver',.07)
 plate([-.78,-.74,-.25],[.5,.06,.35],'pearl');plate([-.78,-.38,-.47],[.49,.34,.055],'pearl')
 for j,x in enumerate(np.linspace(-3.7,3.7,9)):
  if abs(x)<2.15:continue
  bead([x,1.11-.24*np.cos(x),-.2],.17,'gold')
 t=np.linspace(0,2*np.pi,1100);x=3.43*np.cos(t)*(1+.04*np.sin(9*t));y=1.4*np.sin(t)*(.83+.08*np.cos(11*t));z=.35+.18*np.sin(5*t)
 tube(np.stack([x,y,z],-1),.046,color('coral'),24)
 strand([[-1.7,-1.04,.3],[-.75,.52,.4],[.42,-.61,.3],[1.8,.85,.3],[2.4,.85,.3]],'gold',.04)
 line([.45,-1.32,-.55],[.45,1.34,-.55],.033,'silver')
def adumbration():
 for k,x in enumerate([-2.92,-.94,1.12,3.08]):
  col=['silver','violet','teal','gold'][k]
  for a in np.linspace(0,np.pi,2+k):
   ring([x,0,0],.81,col,rot(a,.35),.023+.008*k,arc=(.35,5.8) if k<2 else (0,2*np.pi))
  if k==3:sphere([x,0,0],.75,col,.035,rot(.4,.5,.2))
  else:
   for y in np.linspace(-.55,.55,2+k):line([x-.57,y,0],[x+.57,y,.16],.014,col)
 strand([[-3.65,-1.24,-.2],[-1.2,-1.1,-.2],[1.4,-1.12,-.2],[3.7,-1.28,-.2]],'pearl',.018)
def aisthesis():
 for j,(x,y,c) in enumerate([(-3.2,.82,'gold'),(-3.13,-.87,'coral'),(-.9,1.12,'teal'),(-.83,-1.13,'violet')]):
  sphere([x,y,0],.43,c,.055*j,rot(.3,.6,.2),(.95,.8,1))
  strand([[x+.35,y,0],[x+.8,y*.8,.2],[1.4,y*.25,.15],[2.15,0,.2]],c,.04)
 sphere([2.6,0,.15],.71,'pearl',.025,rot(.4,.6,.2))
 ring([2.6,0,.15],1.01,'gold',rot(.55,.3),.044)
 for a in np.linspace(0,2*np.pi,11)[:-1]:bead([2.6+1.2*np.cos(a),1.2*np.sin(a),-.12],.07,'pearl')
def aleatoricism():
 # A deliberately built decision tree terminating in different realized outputs.
 root=np.array([-3.6,0,0]);bead(root,.25,'gold')
 for j,y in enumerate([-.98,0,.98]):
  branch=np.array([-1.9,y,0]);strand([root,[-2.9,y*.2,.2],branch],PALETTE[j],.055);bead(branch,.13,PALETTE[j])
  for k,dy in enumerate([-.32,.32]):
   end=np.array([-.35,y+dy,.1]);line(branch,end,.028,PALETTE[j]);bead(end,.083,PALETTE[j])
 rect([2.15,0,-.48],1.66,1.48,'pearl',.029)
 rng=np.random.default_rng(11107)
 for j in range(11):
  c=[.85+rng.random()*2.5,-1.05+rng.random()*2.1,rng.random()*.4]
  if j%3==0:plate(c,[.19,.19,.16],PALETTE[j%7],rot(.2,.3,rng.random()*2))
  else:bead(c,.12+(.04*(j%3)),PALETTE[j%7])
 for y in [-.97,0,.97]:arrow([-.07,y,.06],[.47,y,.06],.025,'silver',.15)
def alexithymia():
 # Rich differentiated interior behind an articulation bottleneck.
 for j in range(7):
  a=j*2*np.pi/7;p=[-2.2+.63*np.cos(a),.66*np.sin(a),.3*np.sin(a)];bead(p,.3,PALETTE[j])
  strand([p,[-1.1,p[1]*.68,.3],[.0,p[1]*.16,.32]],PALETTE[j],.035)
 ring([-2.2,0,0],1.05,'pearl',rot(.55,.2),.045)
 for y in [-.51,.51]:plate([.14,y,0],[.14,.35,.4],'silver')
 for j,(x,y) in enumerate([(1.37,.7),(2.76,.55),(1.87,-.84),(3.38,-.71)]):
  rect([x,y,0],.43,.31,'pearl',.031)
  line([x-.43,y-.31,0],[x-.13,y-.31,.18],.045,PALETTE[j])
 strand([[.33,.0,.23],[.75,.0,.22],[1.02,.37,.2]],'gold',.041)
def allesthesia():
 for k,x in enumerate([-2.2,2.2]):
  col='pearl' if k==0 else 'silver';ell([x,0,0],.95,1.39,col,.045)
  for y in np.linspace(-1.05,1.05,5):line([x-.64,y,-.18],[x+.64,y,-.18],.018,col)
  line([x,-1.34,-.16],[x,1.34,-.16],.017,col)
 bead([-2.62,.71,.17],.19,'gold');ring([-2.62,.71,.17],.33,'gold',thick=.025)
 bead([2.62,-.71,.17],.19,'coral');ring([2.62,-.71,.17],.34,'coral',thick=.025)
 strand([[-2.5,.73,.32],[-1.3,1.4,.5],[.2,.14,.7],[1.3,-1.27,.5],[2.5,-.71,.32]],'gold',.043)
 for x,y in [(-2.62,-.71),(2.62,.71)]:ring([x,y,0],.13,'silver',thick=.022)
def allochrony():
 for j,(x,c,phase) in enumerate([(-1.95,'gold',.1),(1.95,'teal',np.pi)]):
  for r in [1.05,1.4]:ring([x,0,0],r,'silver',rot(.15,.35),.019)
  for a in np.linspace(0,2*np.pi,13)[:-1]:
   p=np.array([1.24*np.cos(a),1.24*np.sin(a),0])@rot(.15,.35).T+[x,0,0];bead(p,.055,'silver')
  ring([x,0,.18],1.24,c,rot(.15,.35),.13,arc=(phase,phase+2.18))
  line([x,0,0],[x+.94*np.cos(phase+1),.94*np.sin(phase+1),.2],.04,c);bead([x,0,0],.10,c)
 line([-3.7,-1.52,-.35],[3.7,-1.52,-.35],.021,'pearl')
 for xx in np.linspace(-3.5,3.5,15):line([xx,-1.57,-.35],[xx,-1.47,-.35],.013,'pearl')
def amphiboly():
 for y in [-.65,.65]:
  for k,x in enumerate(np.linspace(-3.45,3.45,5)):plate([x,y,.1],[.32,.22,.19],PALETTE[k],rot(.1,.2,.07))
  for x in np.linspace(-3.1,2.65,4):line([x,y,0],[x+1.07,y,0],.027,'silver')
 strand([[-3.45,.93,0],[-2.45,1.46,.1],[-.6,1.4,.1],[0,.93,0]],'gold',.04)
 strand([[0,.93,0],[1.6,1.35,.1],[3.45,.93,0]],'teal',.04)
 strand([[-3.45,-.93,0],[-1.0,-1.44,.1],[1.72,-.93,0]],'gold',.04)
 strand([[1.72,-.93,0],[2.7,-1.28,.1],[3.45,-.93,0]],'teal',.04)
def anamnesis():
 for j in range(5):
  plate([-2.42,-1.15+j*.25,-.1-j*.06],[1.1,.062,.58],PALETTE[j],rot(.15,.35,-.045*j))
 t=np.linspace(-np.pi*2,2*np.pi,650);q=np.linspace(0,1,len(t));p=np.stack([-1.5+3.4*q+.56*np.cos(t),-.65+1.5*q,.56*np.sin(t)],-1);tube(p,.055,color('gold'),28)
 nodes=[[1.98,.96,.2],[3.1,.86,.1],[2.62,-.16,.25],[3.65,-.72,.1],[1.45,-.91,.1]]
 for a,b in [(0,1),(0,2),(1,2),(2,3),(2,4)]:line(nodes[a],nodes[b],.035,'pearl')
 for i,p in enumerate(nodes):bead(p,.19,PALETTE[i])
def anamorphosis():
 # Rays of one distorted circle become a circular terminal cross-section.
 y=np.linspace(0,2*np.pi,25)
 for k,t in enumerate(y[:-1]):
  a=[-3.5,1.35*np.sin(t),.85*np.cos(t)];b=[2.9,.85*np.sin(t),.85*np.cos(t)]
  line(a,b,.018,'gold' if k%3==0 else 'silver')
 ell([-3.5,0,0],.20,1.35,'violet',.058,.85)
 ring([2.9,0,0],.85,'gold',rot(0,.30,0),.082)
 for j in range(5):
  x=-2.45+j*1.1;ell([x,0,0],.12,.85+(2.9-x)/6.4*.5,'silver',.019,.85)
 bead([-3.8,-1.32,.2],.15,'coral');arrow([-3.6,-1.32,.2],[-2.8,-1.32,.2],.028,'coral',.14)
def anaphora():
 for j,y in enumerate([1.04,.35,-.35,-1.04]):
  bead([-3.35,y,.1],.21,'gold');line([-3.05,y,0],[-2.55,y,0],.046,'gold')
  strand([[-2.5,y,0],[-1.05,y+.19*np.sin(j),.2],[.6,y+.08,.1],[2.73-.3*j,y,0]],PALETTE[j+1],.061)
  bead([2.73-.3*j,y,0],.13,PALETTE[j+1])
 bead([3.65,0,.2],.24,'pearl')
 for y in [-1.04,.35,1.04]:strand([[3.45,0,.1],[2.9,y*.4,-.2],[-2.82,y,-.2]],'silver',.016)
def anastrophe():
 for j,x in enumerate([-2.7,0,2.7]):
  plate([x,-.78,0],[.43,.31,.23],PALETTE[j],rot(.15,.25,.12*j))
  plate([x,.78,0],[.43,.31,.23],PALETTE[2-j],rot(.15,.25,.12*(2-j)))
 for p,col in [([[-2.7,-.78,.15],[-1.35,.18,.8],[1.35,.22,.8],[2.7,.78,.15]],'gold'),([[2.7,-.78,.15],[1.35,-.15,.4],[-1.35,-.15,.4],[-2.7,.78,.15]],'violet')]:strand(p,col,.061)
 line([0,-.38,.0],[0,.38,.0],.04,'teal')
 for y in [-1.26,1.26]:line([-3.43,y,-.4],[3.43,y,-.4],.015,'silver')
def aniconism():
 # No effigy occupies the lavishly articulated center.
 for w,h,c in [(3.5,1.48,'gold'),(3.25,1.24,'pearl'),(1.35,1.06,'teal')]:rect([0,0,-.3],w,h,c,.043)
 for s in [-1,1]:
  for j in range(4):
   x=s*(1.76+j*.42)
   for yy in [-.8,0,.8]:
    t=np.linspace(0,2*np.pi,250);r=.22*(1+.19*np.cos(6*t));tube(np.stack([x+r*np.cos(t),yy+r*np.sin(t),np.full_like(t,.05)],-1),.029,color('gold'),20)
  for y in [-1.22,1.22]:line([s*1.5,y,.0],[s*3.1,y,.0],.024,'teal')
 line([-1.11,-1.02,.0],[1.11,-1.02,.0],.027,'gold')
def antanaclasis():
 # The same curving token appears in a stepped context and a flowing one.
 for x in [-2.3,2.3]:
  t=np.linspace(-np.pi*.65,np.pi*.85,500);p=np.stack([x+.73*np.cos(t),.78*np.sin(t),.18+.13*np.cos(t)],-1);tube(p,.105,color('gold'),32)
 for j in range(4):plate([-2.3,-1.08+j*.13,-.25],[1.25-j*.17,.052,.44],'pearl')
 for k in range(5):
  t=np.linspace(-1.22,1.22,300);p=np.stack([2.3+t,-1.02+k*.14+.065*np.sin(t*5+k),np.full_like(t,-.15)],-1);tube(p,.032,color('teal'),20)
 line([0,-1.3,-.3],[0,1.3,-.3],.014,'silver');bead([0,0,0],.12,'violet')
def antimetabole():
 for x,y,c in [(-3.1,.97,'gold'),(-3.1,-.97,'teal'),(3.1,.97,'teal'),(3.1,-.97,'gold')]:
  if c=='gold':sphere([x,y,.05],.37,c,.08)
  else:plate([x,y,.05],[.35,.32,.22],c,rot(.2,.4,.3))
 t=np.linspace(0,1,750)
 for s,c,z in [(1,'gold',.25),(-1,'teal',-.1)]:
  p=np.stack([-2.65+5.3*t,s*.97*np.cos(np.pi*t),z+.45*np.sin(np.pi*t)],-1);ribbon(p,.13,c,twist=np.pi*.7*s)
 for x in [-3.65,3.65]:line([x,-1.39,-.4],[x,1.39,-.4],.03,'pearl')
def antiphrasis():
 plate([0,-1.3,0],[2.45,.10,.58],'pearl');plate([0,-1.07,0],[.73,.12,.39],'gold')
 # Stately base, ludicrously unstable load, poised with deliberate compositional grace.
 for j,(x,y,ang) in enumerate([(-.4,-.6,-.31),(.0,-.03,.27),(.72,.53,-.28),(1.51,.9,.47)]):plate([x,y,.1+j*.05],[.58,.27,.29],PALETTE[j],rot(.10,.25,ang))
 gear([-2.65,.55,0],.50,'gold',9,thick=.034)
 for a in [0,np.pi/3,2*np.pi/3]:line([-2.65+.65*np.cos(a),.55+.65*np.sin(a),0],[-2.65+.9*np.cos(a),.55+.9*np.sin(a),0],.016,'gold')
 strand([[1.9,1.15,.0],[2.65,1.02,.0],[3.06,.33,.0]],'coral',.029)
def antistrophe():
 for j,y in enumerate([-.8,0,.8]):
  for s in [-1,1]:
   t=np.linspace(0,1,400);x=s*(.34+3.13*t);yy=y+.17*np.sin(2*np.pi*t);z=.15*np.cos(2*np.pi*t)
   tube(np.stack([x,yy,z],-1),.044,color(PALETTE[j]),24)
  bead([3.62,y,.05],.19,'gold');bead([-3.62,y,.05],.11,PALETTE[j])
 line([0,-1.35,-.3],[0,1.35,-.3],.022,'pearl')
 ring([0,0,.0],.20,'pearl',thick=.036)
def aphanisis():
 # Progressively absent outer identity; interior warmth remains distinct.
 for j,x in enumerate(np.linspace(-3.35,3.35,6)):
  if j==0:sphere([x,.06,0],.66,'pearl',.042,rot(.2,.4,.2),(1,1.43,.62))
  else:
   for k in range(max(1,7-j)):
    a=(k+.3)*np.pi/(max(1,7-j));R=rot(0,a,.04*j)
    t=np.linspace(.12,np.pi*1.98,300);p=np.stack([.66*np.cos(t),.94*np.sin(t),np.zeros_like(t)],-1)@R.T+[x,.06,0]
    tube(p,.025 if j<4 else .015,color('silver'),20)
  if j<4:bead([x,-.15,.12],.24-.025*j,'coral')
 line([-3.85,-1.26,-.2],[3.8,-1.26,-.2],.015,'violet')
 bead([2.67,-1.25,.12],.18,'gold');ring([2.67,-1.25,.12],.32,'gold',thick=.021)
def apocatastasis():
 # Segments travel from a scattered field into one visibly jointed architecture.
 for j in range(9):
  a=j*2*np.pi/9;radius=1.11;center=[2.4,0,.0]
  ring(center,radius,PALETTE[j%7],rot(.18,.22),.12,arc=(a+.035,a+2*np.pi/9-.035))
  p=np.array([radius*np.cos(a),radius*np.sin(a),0])@rot(.18,.22).T+center;bead(p,.066,'pearl')
 for j,(x,y,a) in enumerate([(-3.38,-.78,.4),(-2.92,.86,1.5),(-1.87,-.19,3.7),(-.8,1.04,4.7),(-.54,-.83,5.5)]):
  ring([x,y,0],.38,PALETTE[j],rot(.25,.4,.2*j),.09,arc=(a,a+1.55))
  strand([[x+.3,y,-.14],[.2,y*.83,-.38],[1.16,y*.45,-.2]],'silver',.013)
 ring([2.4,0,-.2],.67,'pearl',rot(.18,.22),.034)
def aposiopesis():
 x=np.linspace(-3.75,.56,1000);u=(x+3.75)/4.31;y=-.5+.96*np.sin(u*np.pi*.64)+.11*np.sin(u*5*np.pi);z=.22*np.sin(u*3*np.pi)
 ribbon(np.stack([x,y,z],-1),.19,'gold',twist=np.pi*1.15)
 # Physical cap accentuates a stopping edge, not a mere occlusion.
 end=np.array([x[-1],y[-1],z[-1]]);bead(end,.085,'pearl')
 for j,xx in enumerate([1.13,1.72,2.39,3.08,3.6]):bead([xx,.41-.06*j,-.1],.095*(.86**j),'silver')
 for k in range(4):
  t=np.linspace(-3.8,.1-.2*k,300);tube(np.stack([t,np.full_like(t,-1.17+.11*k),np.full_like(t,-.3)],-1),.014,color('silver'),16)
def apperception():
 rng=np.random.default_rng(2401)
 for j,(x,y) in enumerate([(-3.5,.95),(-3.55,-.5),(-2.6,.1),(-2.14,1.03),(-1.82,-.95),(-.95,.41)]):
  c=PALETTE[j];plate([x,y,0],[.2,.23,.18],c,rot(.4,.3,float(rng.random())))
  strand([[x+.18,y,0],[-.65,y*.66,-.15],[.56,y*.45,.0]],c,.026)
 rect([.59,0,.08],.15,1.35,'pearl',.062)
 for j in range(3):
  for k in range(2):plate([1.43+j*.84,-.43+k*.86,.05],[.31,.31,.21],PALETTE[j*2+k],rot(.12,.18,.0))
 rect([2.27,0,-.2],1.38,.99,'gold',.026)
def appoggiatura():
 for j,y in enumerate(np.linspace(-1.12,.28,5)):line([-3.8,y,-.45],[3.8,y,-.45],.019,'silver')
 for x in [-3,-1.65,1.1,2.83]:bead([x,-.77,.0],.14,'pearl')
 # Accented leaning tone hangs above and to the left of its stepwise resolution.
 sphere([-.42,.8,.2],.36,'gold',.035,rot(.2,.4),(.9,.76,.8))
 sphere([1.0,.32,.14],.28,'teal',.032,rot(.1,.5),(.94,.8,.8))
 strand([[-.42,.8,.18],[-.15,1.22,.25],[.6,.93,.26],[1.0,.34,.18]],'gold',.048)
 line([-.07,.88,.08],[-.07,1.5,.08],.038,'gold')
 line([1.26,.38,.04],[1.26,1.07,.04],.033,'teal')
 plate([.25,-1.42,-.25],[3.58,.09,.39],'pearl')
def arche():
 plate([0,-1.30,-.2],[1.16,.18,.52],'pearl')
 # Explanatory support is below, while consequences branch into unequal heights.
 roots=[[-3.3,.35,0],[-1.8,1.14,.15],[0,1.54,.0],[1.72,1.04,.05],[3.3,.2,.0]]
 for j,end in enumerate(roots):
  strand([[0,-1.16,0],[.22*end[0],-.53,.2],[.72*end[0],.16,.1],end],PALETTE[j],.068)
  if j%2:plate(end,[.30,.22,.25],PALETTE[j],rot(.2,.3,.15))
  else:bead(end,.23,PALETTE[j])
 for j,x in enumerate([-3.1,-2.1,-1.4,1.4,2.1,3.1]):
  strand([[0,-1.42,-.12],[x*.5,-1.53,-.12],[x,-1.45,-.08]],'silver',.018)
def asyndeton():
 # Distinct open forms form a procession; no literal connective edges.
 for j,x in enumerate(np.linspace(-3.6,3.6,7)):
  col=PALETTE[j];y=.14*np.sin(j*1.2);s=.62+.10*np.sin(j)
  t=np.linspace(-1.1,1.15,250);p=np.stack([x+.24*np.sin(t*2.3+j*.25),y+s*t,.18*np.cos(t*2)],-1)
  tube(p,.105,color(col),32,ripple=.03)
  bead([x,-1.21,.0],.061,'pearl')
 for k in range(6):bead([-3+k*1.2,-1.19,-.0],.020,'silver')
def ataraxia():
 # Broad outer waves remain active around a quiet low central bowl.
 for j in range(5):
  t=np.linspace(-3.88,3.88,850);y=(.88+.13*j)*np.sin(t*.76+.22*j);z=-.47+.06*j
  tube(np.stack([t,y,np.full_like(t,z)],-1),.025,color(PALETTE[(j+1)%7]),20)
 u=np.linspace(.05,1.3,100);v=np.linspace(0,2*np.pi,150);U,V=np.meshgrid(u,v,indexing='ij')
 X=1.35*np.sin(U)*np.cos(V);Y=-.64+.73*(1-np.cos(U));Z=.48+1.35*np.sin(U)*np.sin(V);surface(X,Y,Z,'pearl')
 ell([0,-.08,.6],1.30,.15,'gold',.033)
 sphere([0,.36,.6],.24,'gold',.015);ring([0,.37,.6],.45,'silver',rot(.8,.2),.019)
def autotelism():
 # A broad trefoil-like path is one continuous object with internal return.
 t=np.linspace(0,2*np.pi,1600);x=2.55*np.sin(t)+.72*np.sin(2*t);y=.97*np.cos(t)-.39*np.cos(2*t);z=.43*np.sin(3*t)
 p=np.stack([x,y,z],-1);ribbon(p,.16,'gold',twist=np.pi*4,phase=.4)
 for a in [0,2*np.pi/3,4*np.pi/3]:
  pt=np.array([2.55*np.sin(a)+.72*np.sin(2*a),.97*np.cos(a)-.39*np.cos(2*a),.43*np.sin(3*a)])
  bead(pt,.18,'teal')
 ring([0,-.04,-.2],.52,'pearl',rot(.8,.4),.035)
def bathos():
 for j,x in enumerate([-3.2,-2.2,-1.2]):
  plate([x,-.23,.0],[.16,1.09,.26],'pearl')
  plate([x,.91,.0],[.27,.09,.33],'gold')
  plate([x,-1.36,.0],[.33,.08,.36],'pearl')
 strand([[-3.5,1.22,.15],[-2.25,1.5,.15],[-.75,1.2,.15],[.7,.3,.15],[2.0,-1.15,.15]],'gold',.079)
 plate([2.74,-1.30,.08],[.38,.16,.30],'teal')
 line([2.46,-1.13,.22],[2.99,-1.13,.22],.018,'pearl')
 for x in [2.55,2.93]:bead([x,-1.48,.13],.055,'silver')
 strand([[2.16,-1.18,.14],[2.29,-1.13,.15],[2.41,-1.14,.13]],'gold',.024)
def bricolage():
 # A made bridge retains its disparate objects and material histories.
 for x in [-3.12,3.08]:plate([x,-1.13,-.08],[.62,.35,.5],'silver',rot(.05,.15,.08))
 plate([-2.35,-.43,.12],[.77,.13,.30],'pearl',rot(.16,.3,.13))
 gear([-1.28,-.31,.10],.45,'gold',11,thick=.067)
 plate([-.2,-.22,.1],[.65,.16,.30],'teal',rot(.1,.1,-.12))
 ring([.79,-.15,.1],.48,'coral',rot(.25,.15),.074)
 plate([1.68,-.28,.13],[.62,.09,.33],'violet',rot(.13,.1,-.15))
 plate([2.68,-.52,.1],[.5,.18,.33],'pearl',rot(.1,.2,-.11))
 strand([[-3.2,-.17,.15],[-2.12,.72,.25],[.03,1.12,.35],[2.1,.65,.24],[3.3,-.25,.12]],'gold',.046)
 for x in [-2.5,-.2,1.68,2.8]:line([x,-.2,.18],[x,.87-.05*x*x,.25],.028,'silver')
 bead([-1.35,.24,.22],.115,'mint');bead([.74,.36,.19],.11,'blue')
def catabasis():
 for j in range(11):
  x=-3.5+j*.50;y=1.2-j*.235
  plate([x,y,.1],[.30,.09,.39],'pearl' if j<6 else 'silver',rot(.08,.1))
  if j<10:line([x+.2,y-.08,-.2],[x+.2,y-.22,-.2],.039,'gold')
 for y in [.48,.62,.76]:line([-3.89,y,-.6],[3.9,y,-.6],.015,'silver')
 rect([2.72,-.84,-.2],.76,.62,'violet',.092)
 line([2.71,-1.44,-.2],[2.71,-.3,-.2],.015,'silver')
 bead([-.22,-.13,.39],.17,'gold');strand([[-.2,-.23,.33],[.25,-.73,.29],[.48,-.9,.25]],'gold',.055)
def catachresis():
 # Literal frame borrows a growing support and leaf at an improper joint.
 plate([-1.03,.10,.1],[1.65,.11,.55],'pearl')
 for x in [-2.28,-.45]:line([x,-.02,.02],[x,-1.32,.02],.095,'pearl')
 for x in [-2.28,.16]:line([x,.16,-.35],[x,1.27,-.35],.085,'pearl')
 line([-2.28,1.27,-.35],[.16,1.27,-.35],.093,'pearl')
 strand([[.56,.02,.03],[1.15,-.76,.13],[1.8,-1.22,.10],[2.94,-1.13,.13]],'gold',.11)
 strand([[1.19,-.71,.16],[1.97,.2,.30],[2.83,.74,.15]],'gold',.075)
 u=np.linspace(0,np.pi,100);v=np.linspace(-1,1,45);U,V=np.meshgrid(u,v,indexing='ij');X=2.0+.94*np.cos(U);Y=.77+.42*np.sin(U)*V;Z=.25+.20*np.sin(U)*(1-V*V)
 surface(X,Y,Z,'teal');strand([[1.1,.78,.27],[2.04,.78,.43],[2.92,.78,.28]],'gold',.022)
 for y in [-1.3,-1.42]:strand([[1.8,y,.07],[2.75,y+.07,.10],[3.6,y-.02,.06]],'gold',.03)
def cataphora():
 ring([-3.05,0,0],.70,'gold',rot(.1,.22),.084)
 for j,x in enumerate([-1.53,-.4,.76]):plate([x,0,0],[.20,.24,.15],'silver',rot(.15,.25,.12))
 sphere([2.83,0,.0],.71,'gold',.049,rot(.3,.6,.1))
 arrow([-2.05,.89,.14],[2.11,.89,.14],.031,'teal',.20)
 strand([[2.83,-.78,.0],[2.06,-1.22,.08],[-1.86,-1.17,.08],[-3.05,-.78,.0]],'pearl',.035)
 for a in [1.6,3.7,5.3]:bead([2.83+.93*np.cos(a),.93*np.sin(a),-.1],.072,'teal')
def catharsis():
 for j,c in enumerate(['gold','teal','coral','violet','blue']):
  t=np.linspace(0,1,800);x=-3.8+3.77*t;y=.83*np.sin(t*(5+j*.2)+j*1.18)*(1-.72*t);z=.3*np.cos(t*6+j)
  tube(np.stack([x,y,z],-1),.047,color(c),24)
  t=np.linspace(0,1,650);x=.22+3.55*t;y=(j-2)*(.06+.37*t);z=.10*np.sin(t*4+j)
  tube(np.stack([x,y,z],-1),.047,color(c),24)
 rect([.1,0,.05],.11,1.38,'pearl',.090)
 for y in [-1.54,1.54]:plate([.1,y,-.05],[.35,.09,.31],'gold')
def chora():
 # A receptive folded surface whose curvature organizes without becoming its contents.
 u=np.linspace(-3.75,3.75,200);v=np.linspace(-1.1,1.1,90);U,V=np.meshgrid(u,v,indexing='ij')
 X=U;Y=V+.17*np.sin(U*1.2);Z=-.42+.50*(V*V)+.19*np.cos(U*1.5)*np.cos(V*2)
 surface(X,Y,Z,'pearl')
 for side in [0,-1]:tube(np.stack([X[:,side],Y[:,side],Z[:,side]],-1),.027,color('gold'),20)
 for j,(x,y) in enumerate([(-2.6,.21),(-.86,-.2),(.85,.14),(2.6,-.13)]):
  if j%2:plate([x,y,.31],[.31,.28,.21],PALETTE[j],rot(.3,.4,.4))
  else:sphere([x,y,.3],.34,PALETTE[j],.06,rot(.2,.5,.1))
 for j,x in enumerate(np.linspace(-3.3,3.3,12)):
  p=path([[x,-.86,.0],[x+.08,0,-.31],[x,.91,.09]],160);tube(p,.012,color('silver'),16)
def chronotope():
 # A route encounters spatial frames carrying unequal depths of accumulated time.
 x=np.linspace(-3.95,3.95,1300);y=-.55+.35*np.sin(x*1.05);z=.12+.05*np.cos(x)
 p=np.stack([x,y,z],-1);ribbon(p,.17,'gold',twist=.2)
 for j,xx in enumerate([-2.73,-.54,1.6,3.19]):
  for k in range(j+1):
   zz=-.31-k*.18;yy=.21+.10*k
   rect([xx,yy,zz],.59,.96,'pearl' if k==0 else 'silver',.045 if k==0 else .025)
  for k in range(j+1):bead([xx-.35+k*.20,1.27,.02],.048,PALETTE[j])
  line([xx,-1.43,-.55],[xx,1.45,-.55],.012,'silver')
 bead([-3.54,-.35,.24],.14,'teal');bead([.57,-.36,.24],.14,'coral')

FUNCS=[ablaut,aboulia,acatalepsy,acedia,adumbration,aisthesis,aleatoricism,alexithymia,allesthesia,allochrony,amphiboly,anamnesis,anamorphosis,anaphora,anastrophe,aniconism,antanaclasis,antimetabole,antiphrasis,antistrophe,aphanisis,apocatastasis,aposiopesis,apperception,appoggiatura,arche,asyndeton,ataraxia,autotelism,bathos,bricolage,catabasis,catachresis,cataphora,catharsis,chora,chronotope]
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('ids',nargs='*',type=int);parser.add_argument('--proof',action='store_true');args=parser.parse_args()
 for i in args.ids or range(1,38):
  parts.clear();f=FUNCS[i-1];f();save(f'{i:03d}-{f.__name__}',args.proof)
