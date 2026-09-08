from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import os, re, sqlite3

def runtime_dir()->Path:
    p=Path(os.getenv('EWW_RUNTIME_DIR','/data' if Path('/data').exists() else 'runtime')); p.mkdir(parents=True,exist_ok=True); return p

def _db():
    c=sqlite3.connect(runtime_dir()/'analytics.sqlite')
    c.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT,occurred_at TEXT NOT NULL,tool TEXT NOT NULL,outcome TEXT NOT NULL,billable INTEGER NOT NULL,payment_state TEXT,actor_class TEXT NOT NULL,declared_client TEXT,latency_ms REAL)'); c.commit(); return c

def _safe(v:Any,max_len=80):
    if not isinstance(v,str) or not v.strip(): return None
    return re.sub(r'[^A-Za-z0-9._:/+@-]','_',v.strip())[:max_len]

def classify_actor(meta:dict[str,Any]|None):
    meta=meta or {}; source=str(meta.get('englandworkswatch/actor','')).strip().lower(); actor=source if source in {'owned_ci','declared_external'} else 'unattributed'
    ci=meta.get('io.modelcontextprotocol/clientInfo'); name=ci.get('name') if isinstance(ci,dict) else None
    return actor,_safe(name)

def record(tool:str,outcome:str,*,billable:bool,payment_state:str|None=None,meta:dict[str,Any]|None=None,latency_ms:float|None=None):
    actor,client=classify_actor(meta)
    with _db() as c: c.execute('INSERT INTO events(occurred_at,tool,outcome,billable,payment_state,actor_class,declared_client,latency_ms) VALUES(?,?,?,?,?,?,?,?)',(datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),tool,outcome,int(billable),payment_state,actor,client,latency_ms))

def summary():
    try:
        with _db() as c: rows=c.execute('SELECT tool,outcome,billable,payment_state,actor_class FROM events').fetchall()
    except sqlite3.Error: rows=[]
    return {'total_events':len(rows),'by_tool':dict(Counter(r[0] for r in rows)),'by_outcome':dict(Counter(r[1] for r in rows)),'by_actor_class':dict(Counter(r[4] for r in rows)),'paid_funnel':dict(Counter((r[3] or 'none') for r in rows if r[2])),'privacy':'No employer/worker facts, raw MCP metadata, payment signatures, private keys or seed phrases are stored.'}
