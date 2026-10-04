from __future__ import annotations
from .config import Config
from .memory import Memory
from .providers import build_provider
from .security import Security
from .tools import Tools
from .student import StudentBrain

SYSTEM='''You are WEBSTER, a calm, capable Windows personal assistant. Be concise but useful. You may plan actions, but never claim an action happened unless the tool confirms it. Respect permissions for camera, microphone, external communication, files and terminal. You are also a student study assistant: explain rather than simply doing schoolwork for the student.'''

class Webster:
    def __init__(self):
        self.memory=Memory(Config.data_dir/"memory.json")
        self.student=StudentBrain(Config.data_dir/"student.json")
        self.security=Security(); self.tools=Tools(self.security); self.provider=build_provider()
    def _tool_intent(self,text):
        t=text.lower()
        if t.startswith(("search ","google ","look up ")): return "search",text.split(" ",1)[1]
        if t.startswith(("open http://","open https://")): return "url",text.split(" ",1)[1]
        if t.startswith("launch "): return "launch",text[7:].strip()
        return None,None
    def handle(self,text,approve=None):
        self.memory.add(text,"episodic",0.2)
        name,arg=self._tool_intent(text)
        if name:
            if name=="search": result=self.tools.search(arg)
            elif name=="url": result=self.tools.open_url(arg)
            else: result=self.tools.launch(arg)
            answer=result.text
        else:
            context="\n".join(x["text"] for x in self.memory.search(text,5))
            prompt=text+ ("\nRelevant memory:\n"+context if context else "")
            try: answer=self.provider.chat([{"role":"user","content":prompt}],SYSTEM)
            except Exception as e: answer=f"I couldn't reach the AI provider: {e}"
        self.memory.add(answer,"response",0.1)
        return answer
