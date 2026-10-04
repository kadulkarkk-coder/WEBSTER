from __future__ import annotations
import json, threading
from datetime import datetime
from pathlib import Path

class Memory:
    def __init__(self, path: Path):
        self.path=path; self.lock=threading.RLock(); self.items=[]
        self._load()
    def _load(self):
        try: self.items=json.loads(self.path.read_text(encoding="utf-8"))
        except Exception: self.items=[]
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        tmp=self.path.with_suffix(".tmp"); tmp.write_text(json.dumps(self.items,ensure_ascii=False,indent=2),encoding="utf-8"); tmp.replace(self.path)
    def add(self,text:str,kind="episodic",importance=0.5):
        with self.lock:
            self.items.append({"text":text,"kind":kind,"importance":importance,"time":datetime.now().isoformat(timespec="seconds")})
            self.items=self.items[-1000:]; self._save()
    def search(self,query:str,limit=8):
        q=set(query.lower().split())
        scored=[]
        for x in self.items:
            words=set(x["text"].lower().split()); score=len(q & words)+float(x.get("importance",0))
            if score: scored.append((score,x))
        return [x for _,x in sorted(scored,key=lambda z:z[0],reverse=True)[:limit]]
    def recent(self,limit=12): return self.items[-limit:]
