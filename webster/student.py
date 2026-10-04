from __future__ import annotations
import json
from pathlib import Path
class StudentBrain:
    def __init__(self,path:Path):
        self.path=path; self.data=self._load()
    def _load(self):
        try:return json.loads(self.path.read_text(encoding="utf-8"))
        except:return {"subjects":{},"tasks":[],"mistakes":[],"missions":[]}
    def _save(self): self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps(self.data,indent=2),encoding="utf-8")
    def add_subject(self,name): self.data["subjects"].setdefault(name,{"chapters":[],"weak_topics":[]}); self._save()
    def add_task(self,text,due=""): self.data["tasks"].append({"text":text,"due":due,"done":False}); self._save()
    def complete_task(self,index):
        if 0<=index<len(self.data["tasks"]): self.data["tasks"][index]["done"]=True; self._save()
    def add_mistake(self,subject,topic,note): self.data["mistakes"].append({"subject":subject,"topic":topic,"note":note}); self._save()
    def summary(self): return self.data
