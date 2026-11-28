"""Group J: lightweight TF-IDF cosine similarity between V12 test texts and blueprint TCs (no external libs)."""
import re,math,json,os
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
STOP=set('a an the and or of to in on for with by from at as is are be no not any all each every per via than then into only its it this that same new one two'.split())
SYN={'tenant':'tenant','tenants':'tenant','company':'tenant','startup':'tenant','startups':'tenant','issuer':'tenant','idempotency':'idempot','idempotent':'idempot','duplicate':'dup','duplicates':'dup','replay':'dup','replayed':'dup','hold':'hold','held':'hold','holds':'hold','approval':'approv','approve':'approv','approved':'approv','approves':'approv','approver':'approv','reviewer':'approv','consent':'consent','opt-out':'consent','optout':'consent','suppression':'consent','budget':'budget','cap':'budget','quota':'budget','model':'model','models':'model','prompt':'prompt','prompts':'prompt','injection':'inject','injected':'inject','cache':'cache','cached':'cache'}
def tok(s):
    w=re.findall(r'[a-z][a-z0-9\-]+',s.lower())
    return [SYN.get(x,x[:7]) for x in w if x not in STOP and len(x)>2]
class Index:
    def __init__(self):
        idx=json.load(open(os.path.join(HERE,'j_bp_tc_index.json')))
        self.ids=list(idx); self.meta=idx
        docs=[tok(idx[i]['title']+' '+idx[i]['row']) for i in self.ids]
        df=Counter(t for d in docs for t in set(d)); N=len(docs)
        self.idf={t:math.log((N+1)/(c+1))+1 for t,c in df.items()}
        self.vecs=[self.vec(d) for d in docs]
    def vec(self,toks):
        tf=Counter(toks); v={t:(1+math.log(c))*self.idf.get(t,math.log(len(self.ids))+1) for t,c in tf.items()}
        n=math.sqrt(sum(x*x for x in v.values())) or 1
        return {t:x/n for t,x in v.items()}
    def top(self,text,k=3,prefer=None):
        q=self.vec(tok(text)); res=[]
        for i,v in zip(self.ids,self.vecs):
            s=sum(w*v.get(t,0) for t,w in q.items())
            if s>0: res.append((s,i))
        res.sort(reverse=True); return [(round(s,3),i) for s,i in res[:k]]
