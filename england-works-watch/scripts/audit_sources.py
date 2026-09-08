import hashlib,json,sys,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; registry=json.loads((ROOT/'data/source_registry.json').read_text()); results=[]; failed=0
for src in registry['sources']:
    try:
        req=urllib.request.Request(src['url'],headers={'User-Agent':'EnglandWorksWatch-source-audit/0.1'}); body=urllib.request.urlopen(req,timeout=20).read(2_000_000).decode('utf-8','replace'); missing=[m for m in src.get('expected_markers',[]) if m.lower() not in body.lower()]; state='UNCHANGED' if not missing else 'REVIEW_REQUIRED'; failed+=bool(missing); results.append({'source_id':src['source_id'],'state':state,'http_bytes':len(body),'sha256':hashlib.sha256(body.encode()).hexdigest(),'missing_markers':missing})
    except Exception as exc:
        failed+=1; results.append({'source_id':src['source_id'],'state':'FETCH_FAILED','error':type(exc).__name__})
print(json.dumps({'sources':results,'blocking_count':failed},indent=2)); raise SystemExit(1 if failed else 0)
