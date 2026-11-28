"""Parse FSD V12 Appendix A / A2 OpenAPI 3.1 text (strip heading lines) -> CSV of operations, components summary."""
import sys, csv, json, yaml
def load(path):
    lines=open(path,encoding='utf-8').read().split('\n')
    start=next(i for i,l in enumerate(lines) if l.startswith('openapi:'))
    return yaml.safe_load('\n'.join(reindent(lines[start:])))
TOP={'openapi','info','servers','security','paths','components'}
IND={'get':4,'post':4,'put':4,'patch':4,'delete':4,'operationId':6,'tags':6,'summary':6,'parameters':6,'requestBody':6,'responses':6,'x-idempotency':6,'required':8,'content':8,'application/json':10,'schema':12}
def reindent(lines):
    # PDF/text extraction dropped leading spaces on some lines; restore by key context
    out=[];prev=''
    for l in lines:
        if l and not l.startswith(' '):
            key=l.split(':')[0].strip()
            if key in TOP: pass
            elif key.startswith('/'): l='  '+l
            elif key.startswith('"') : l=' '*8+l
            elif l.startswith('- '): l=' '*8+l
            elif key=='content' and prev.strip().startswith('"'): l=' '*10+l  # inside a response
            elif key=='application/json' and out and out[-1].strip()=='content:' and len(out[-1])-len(out[-1].lstrip())==10: l=' '*12+l
            elif key=='schema' and out and out[-1].strip()=='application/json:' and len(out[-1])-len(out[-1].lstrip())==12: l=' '*14+l
            elif key in IND: l=' '*IND[key]+l
            else: raise SystemExit('unknown unindented line: '+l)
        out.append(l); prev=l
    return out
def ops(doc, src):
    rows=[]
    for p,item in doc.get('paths',{}).items():
        for m,op in item.items():
            if m not in ('get','post','put','patch','delete'): continue
            params=[ (x.get('$ref','').split('/')[-1] if '$ref' in x else x.get('name')) for x in op.get('parameters',[])]
            rb=op.get('requestBody',{}); rbs=''
            if rb:
                s=list(rb.get('content',{}).values())[0].get('schema',{}); rbs=s.get('$ref','').split('/')[-1] or json.dumps(s)[:60]
            resp=sorted(op.get('responses',{}).keys())
            r200=op.get('responses',{}).get('200',{}); rs=''
            if isinstance(r200,dict) and 'content' in r200:
                rs=list(r200['content'].values())[0].get('schema',{}).get('$ref','').split('/')[-1]
            rows.append(dict(src=src,method=m.upper(),path=p,operationId=op.get('operationId'),tags=';'.join(op.get('tags',[])),summary=op.get('summary',''),params=';'.join(params),request=rbs,response=rs,codes=';'.join(resp),idem=op.get('x-idempotency',''),security=json.dumps(op.get('security','default'))))
    return rows
if __name__=='__main__':
    out=sys.argv[1]; allrows=[]
    for path,src in zip(sys.argv[2::2],sys.argv[3::2]):
        d=load(path); r=ops(d,src); allrows+=r
        comp=d.get('components',{})
        print(src,'paths',len(d['paths']),'ops',len(r))
        for k,v in comp.items(): print('  components.',k,len(v),list(v)[:40])
    with open(out,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0])); w.writeheader(); w.writerows(allrows)
