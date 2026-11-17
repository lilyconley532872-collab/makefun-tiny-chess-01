import json,os,sys,urllib.request,urllib.error
ENV_URL=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
NODE_BUDGET=int(os.environ.get("NODE_BUDGET","30000"))
VAL=[0,100,320,330,500,900,0]
KN_OFF=(-33,-31,-18,-14,14,18,31,33)
KG_OFF=(-17,-16,-15,-1,1,15,16,17)
DIAG=(-17,-15,15,17)
ORTH=(-16,-1,1,16)
def q():
 t=[[0]*64 for _ in range(7)]
 for r in range(8):
  for f in range(8):
   i=r*8+f
   c=min(f,7-f)+min(r,7-r)
   t[1][i]=[0,0,5,10,20,35,60,0][r]+(10 if f in(3,4)and 2<=r<=4 else 0)
   t[2][i]=6*c-24
   t[3][i]=4*c-10
   t[4][i]=(12 if r==6 else 0)+(5 if r==0 and f in(3,4)else 0)
   t[5][i]=2*c-8
   t[6][i]=[25,30,15,0,0,15,30,25][f]if r==0 else max(-50,-15*r)
 return t
PST=q()
EGK=[8*(min(f,7-f)+min(r,7-r))-28 for r in range(8)for f in range(8)]
class K:
 def __init__(S):
  S.A=[0]*128
  S.W=1
  S.C=0
  S.E=-1
  S.H=0
  S.Y={1:4,-1:116}
  S.I=[]
  S.J=[]
 def F(S,fen):
  parts=fen.split()
  S.A=[0]*128
  rows=parts[0].split("/")
  for ri,row in enumerate(rows):
   r=7-ri
   f=0
   for ch in row:
    if ch.isdigit():
     f+=int(ch)
    else:
     pc="PNBRQK".index(ch.upper())+1
     if ch.islower():
      pc=-pc
     sq=r*16+f
     S.A[sq]=pc
     if abs(pc)==6:
      S.Y[1 if pc>0 else-1]=sq
     f+=1
  S.W=1 if parts[1]=="w"else-1
  S.C=0
  if len(parts)>2:
   if"K"in parts[2]:S.C|=1
   if"Q"in parts[2]:S.C|=2
   if"k"in parts[2]:S.C|=4
   if"q"in parts[2]:S.C|=8
  S.E=-1
  if len(parts)>3 and parts[3]!="-":
   S.E=(ord(parts[3][0])-97)+(int(parts[3][1])-1)*16
  S.H=int(parts[4])if len(parts)>4 else 0
  S.I=[]
  S.J=[S.Z()]
 def Z(S):
  return hash((tuple(S.A),S.W,S.C,S.E))
 def T(S,sq,by):
  A=S.A
  if by==1:
   for s in(sq-15,sq-17):
    if not(s&0x88)and A[s]==1:
     return True
  else:
   for s in(sq+15,sq+17):
    if not(s&0x88)and A[s]==-1:
     return True
  for o in KN_OFF:
   s=sq+o
   if not(s&0x88)and A[s]==2*by:
    return True
  for o in KG_OFF:
   s=sq+o
   if not(s&0x88)and A[s]==6*by:
    return True
  for o in DIAG:
   s=sq+o
   while not(s&0x88):
    p=A[s]
    if p:
     if p==3*by or p==5*by:
      return True
     break
    s+=o
  for o in ORTH:
   s=sq+o
   while not(s&0x88):
    p=A[s]
    if p:
     if p==4*by or p==5*by:
      return True
     break
    s+=o
  return False
 def G(S,caps_only=False):
  A,W=S.A,S.W
  n=[]
  d=16 if W==1 else-16
  sr=1 if W==1 else 6
  prr=6 if W==1 else 1
  for sq in range(128):
   if sq&0x88:
    continue
   p=A[sq]
   if p==0 or(p>0)!=(W==1):
    continue
   t=abs(p)
   r=sq>>4
   if t==1:
    if not caps_only or r==prr:
     s=sq+d
     if A[s]==0:
      if r==prr:
       for pr in(5,4,3,2):
        n.append((sq,s,pr))
      elif not caps_only:
       n.append((sq,s,0))
       if r==sr:
        s2=sq+2*d
        if A[s2]==0:
         n.append((sq,s2,0))
    for df in(-1,1):
     s=sq+d+df
     if s&0x88:
      continue
     q=A[s]
     if q and(q>0)!=(W==1):
      if r==prr:
       for pr in(5,4,3,2):
        n.append((sq,s,pr))
      else:
       n.append((sq,s,0))
     elif s==S.E:
      n.append((sq,s,0))
   elif t==2 or t==6:
    offs=KN_OFF if t==2 else KG_OFF
    for o in offs:
     s=sq+o
     if s&0x88:
      continue
     q=A[s]
     if q==0:
      if not caps_only:
       n.append((sq,s,0))
     elif(q>0)!=(W==1):
      n.append((sq,s,0))
    if t==6 and not caps_only:
     if W==1 and sq==4:
      if S.C&1 and A[5]==0 and A[6]==0 and A[7]==4 and not S.T(4,-1)and not S.T(5,-1)and not S.T(6,-1):
       n.append((4,6,0))
      if S.C&2 and A[3]==0 and A[2]==0 and A[1]==0 and A[0]==4 and not S.T(4,-1)and not S.T(3,-1)and not S.T(2,-1):
       n.append((4,2,0))
     elif W==-1 and sq==116:
      if S.C&4 and A[117]==0 and A[118]==0 and A[119]==-4 and not S.T(116,1)and not S.T(117,1)and not S.T(118,1):
       n.append((116,118,0))
      if S.C&8 and A[115]==0 and A[114]==0 and A[113]==0 and A[112]==-4 and not S.T(116,1)and not S.T(115,1)and not S.T(114,1):
       n.append((116,114,0))
   else:
    offs=[]
    if t==3 or t==5:offs+=DIAG
    if t==4 or t==5:offs+=ORTH
    for o in offs:
     s=sq+o
     while not(s&0x88):
      q=A[s]
      if q==0:
       if not caps_only:
        n.append((sq,s,0))
      else:
       if(q>0)!=(W==1):
        n.append((sq,s,0))
       break
      s+=o
  return n
 def M(S,mv):
  f,t,pr=mv
  A=S.A
  pc=A[f]
  cap=A[t]
  ep_cap=-1
  if abs(pc)==1 and t==S.E and A[t]==0:
   ep_cap=t-16 if S.W==1 else t+16
   cap=A[ep_cap]
   A[ep_cap]=0
  S.I.append((mv,cap,ep_cap,S.C,S.E,S.H))
  A[t]=pr*S.W if pr else pc
  A[f]=0
  if abs(pc)==6 and abs(t-f)==2:
   if t==6:A[5],A[7]=4,0
   elif t==2:A[3],A[0]=4,0
   elif t==118:A[117],A[119]=-4,0
   elif t==114:A[115],A[112]=-4,0
  if abs(pc)==6:
   S.Y[S.W]=t
  if f==4 or t==4:S.C&=~3
  if f==0 or t==0:S.C&=~2
  if f==7 or t==7:S.C&=~1
  if f==116 or t==116:S.C&=~12
  if f==112 or t==112:S.C&=~8
  if f==119 or t==119:S.C&=~4
  S.E=-1
  if abs(pc)==1 and abs(t-f)==32:
   S.E=(f+t)//2
  S.H=0 if abs(pc)==1 or cap else S.H+1
  S.W=-S.W
  S.J.append(S.Z())
  return not S.T(S.Y[-S.W],S.W)
 def U(S):
  mv,cap,ep_cap,castle,ep,half=S.I.pop()
  f,t,pr=mv
  A=S.A
  S.W=-S.W
  pc=A[t]
  A[f]=(1 if S.W==1 else-1)if pr else pc
  A[t]=cap if ep_cap<0 else 0
  if ep_cap>=0:
   A[ep_cap]=cap
  if abs(pc)==6 and abs(t-f)==2:
   if t==6:A[5],A[7]=0,4
   elif t==2:A[3],A[0]=0,4
   elif t==118:A[117],A[119]=0,-4
   elif t==114:A[115],A[112]=0,-4
  if abs(pc)==6:
   S.Y[S.W]=f
  S.C,S.E,S.H=castle,ep,half
  S.J.pop()
 def L(S):
  S.I.append((None,0,-1,S.C,S.E,S.H))
  S.E=-1
  S.H+=1
  S.W=-S.W
  S.J.append(S.Z())
 def D(S):
  _,_,_,castle,ep,half=S.I.pop()
  S.W=-S.W
  S.E,S.H=ep,half
  S.J.pop()
 def P(S):
  out=[]
  for mv in S.G():
   if S.M(mv):
    out.append(mv)
   S.U()
  return out
 def V(S):
  A=S.A
  s=0
  nonpawn=0
  bishops=[0,0]
  wpawns=[]
  bpawns=[]
  prq=0
  minors=0
  knights=0
  lb=0
  db=0
  for sq in range(128):
   if sq&0x88:
    continue
   p=A[sq]
   if not p:
    continue
   t=abs(p)
   w=p>0
   r,f=sq>>4,sq&7
   rel=(r*8+f)if w else((7-r)*8+f)
   if t==6:
    continue
   if t==1 or t==4 or t==5:
    prq+=1
   elif t==2:
    minors+=1
    knights+=1
   elif t==3:
    minors+=1
    if(r+f)%2==0:
     db+=1
    else:
     lb+=1
   v=VAL[t]+PST[t][rel]
   s+=v if w else-v
   if t!=1:
    nonpawn+=VAL[t]
    if t==3:
     bishops[0 if w else 1]+=1
   elif w:
    wpawns.append((r,f))
   else:
    bpawns.append((r,f))
  if prq==0 and(minors<=1 or(knights==0 and(lb==0 or db==0))):
   return 0
  bmin=[99]*8
  wmax=[-1]*8
  wcnt=[0]*8
  bcnt=[0]*8
  for r,f in bpawns:
   if r<bmin[f]:bmin[f]=r
   bcnt[f]+=1
  for r,f in wpawns:
   if r>wmax[f]:wmax[f]=r
   wcnt[f]+=1
  for r,f in wpawns:
   ok=True
   for ff in(f-1,f,f+1):
    if 0<=ff<=7 and bmin[ff]>r:
     ok=False
   if ok:
    s+=12+14*r
   if wcnt[f]>1:
    s-=8
   if not((f>0 and wcnt[f-1])or(f<7 and wcnt[f+1])):
    s-=8
  for r,f in bpawns:
   ok=True
   for ff in(f-1,f,f+1):
    if 0<=ff<=7 and wmax[ff]<r:
     ok=False
   if ok:
    s-=12+14*(7-r)
   if bcnt[f]>1:
    s+=8
   if not((f>0 and bcnt[f-1])or(f<7 and bcnt[f+1])):
    s+=8
  phase=min(nonpawn,6400)
  for sgn in(1,-1):
   ksq=S.Y[sgn]
   r,f=ksq>>4,ksq&7
   rel=(r*8+f)if sgn==1 else((7-r)*8+f)
   kv=(PST[6][rel]*phase+EGK[rel]*(6400-phase))//6400
   s+=kv if sgn==1 else-kv
  if bishops[0]>=2:s+=30
  if bishops[1]>=2:s-=30
  return s if S.W==1 else-s
MATE=100000
TT={}
KILLERS={}
NODES=[0]
ABORT=[False]
def O(b,n,u=None,ply=0):
 def key(mv):
  f,t,pr=mv
  s=0
  cap=b.A[t]
  if cap:
   s+=10000+VAL[abs(cap)]*10-VAL[abs(b.A[f])]//10
  if pr:
   s+=9000+VAL[pr]
  if u and mv==u:
   s+=100000
  k=KILLERS.get(ply)
  if k and mv in k:
   s+=5000
  return-s
 return sorted(n,key=key)
def Q(b,a,w,ply):
 NODES[0]+=1
 if NODES[0]>NODE_BUDGET:
  ABORT[0]=True
  return 0
 if b.H>=100:
  return 0
 if ply>64:
  return b.V()
 c=b.T(b.Y[b.W],-b.W)
 if not c:
  stand=b.V()
  if stand>=w:
   return stand
  if stand>a:
   a=stand
 x=-MATE-1 if c else a
 for mv in O(b,b.G(caps_only=not c),ply=ply):
  if not b.M(mv):
   b.U()
   continue
  s=-Q(b,-w,-a,ply+1)
  b.U()
  if ABORT[0]:
   return 0
  if s>x:
   x=s
  if s>=w:
   return s
  if s>a:
   a=s
 if c and x==-MATE-1:
  return-MATE+ply
 return x
def N(b,d,a,w,ply):
 if b.H>=100:
  return 0
 h=b.J[-1]
 if h in b.J[:-1]:
  return 0
 c=b.T(b.Y[b.W],-b.W)
 if c:
  d+=1
 if d<=0:
  return Q(b,a,w,ply)
 NODES[0]+=1
 if NODES[0]>NODE_BUDGET:
  ABORT[0]=True
  return 0
 if d>=3 and not c:
  ev=b.V()
  if ev>=w:
   b.L()
   s=-N(b,d-3,-w,-w+1,ply+1)
   b.D()
   if ABORT[0]:
    return 0
   if s>=w:
    return w
 a0=a
 u=None
 ent=TT.get(h)
 if ent:
  s,fl,mv,ed=ent
  if ed>=d:
   if s>MATE-1000:
    s-=ply
   elif s<-MATE+1000:
    s+=ply
   if fl==0:
    return s
   if fl==1 and s>=w:
    return s
   if fl==2 and s<=a:
    return s
  u=mv
 n=O(b,b.G(),u,ply)
 x=-MATE-1
 v=None
 for mv in n:
  if not b.M(mv):
   b.U()
   continue
  s=-N(b,d-1,-w,-a,ply+1)
  b.U()
  if ABORT[0]:
   return 0
  if s>x:
   x=s
   v=mv
  if s>a:
   a=s
  if a>=w:
   k=KILLERS.setdefault(ply,[])
   if mv not in k:
    k.insert(0,mv)
    del k[2:]
   break
 if x==-MATE-1:
  return-MATE+ply if b.T(b.Y[b.W],-b.W)else 0
 if x<=a0:
  fl=2
 elif x>=w:
  fl=1
 else:
  fl=0
 store=x
 if store>MATE-1000:
  store+=ply
 elif store<-MATE+1000:
  store-=ply
 TT[h]=(store,fl,v,d)
 return x
def R(b,legal):
 if len(legal)==1:
  return legal[0]
 v=legal[0]
 NODES[0]=0
 ABORT[0]=False
 for d in range(1,10):
  if ABORT[0]:
   break
  a=-MATE-1
  cb=v
  cs=-MATE-1
  for mv in O(b,legal,v,0):
   if not b.M(mv):
    b.U()
    continue
   s=-N(b,d-1,-MATE-1,-a,1)
   b.U()
   if ABORT[0]:
    break
   if s>cs:
    cs=s
    cb=mv
   if s>a:
    a=s
  if ABORT[0]:
   break
  v=cb
  if cs>MATE-1000:
   break
 return v
def X(mv):
 f,t,pr=mv
 s="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)
 if pr:
  s+="nbrq"[pr-2]
 return s
def y(b,u):
 f=(ord(u[0])-97)+(int(u[1])-1)*16
 t=(ord(u[2])-97)+(int(u[3])-1)*16
 pr="nbrq".index(u[4])+2 if len(u)==5 else 0
 for mv in b.G():
  if mv[0]==f and mv[1]==t and mv[2]==pr:
   b.M(mv)
   return True
 return False
def p(path,body):
 req=urllib.request.Request(ENV_URL+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(req)as res:
   return json.load(res)
 except urllib.error.HTTPError as e:
  sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")
def m():
 b=K()
 hist=K()
 started=False
 applied=0
 while True:
  g=p("/game",{})
  if g["status"]=="done":
   break
  if not started:
   hist.F(g["start_fen"])
   applied=0
   started=True
   TT.clear()
   KILLERS.clear()
  while applied<len(g["moves"]):
   y(hist,g["moves"][applied])
   applied+=1
  b.F(g["fen"])
  b.J=list(hist.J)
  while g["status"]=="your_move":
   legal=b.P()
   env_legal=set(g["legal_moves"])
   ours=[mv for mv in legal if X(mv)in env_legal]
   mv=R(b,ours if ours else legal)
   g=p("/move",{"game":g["game"],"move":X(mv)})
   if g["status"]=="your_move":
    while applied<len(g["moves"]):
     y(hist,g["moves"][applied])
     applied+=1
    b.F(g["fen"])
    b.J=list(hist.J)
  started=False
 return g
m()
