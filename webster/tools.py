from __future__ import annotations
import os, subprocess, webbrowser, urllib.parse, urllib.request, json
from dataclasses import dataclass
from .security import Security

@dataclass
class ToolResult:
    ok: bool; text: str

class Tools:
    def __init__(self,security): self.security=security
    def open_url(self,url): webbrowser.open(url); return ToolResult(True,"Opened the browser.")
    def search(self,q):
        url="https://html.duckduckgo.com/html/?q="+urllib.parse.quote(q)
        try:
            with urllib.request.urlopen(url,timeout=15) as r: html=r.read().decode("utf-8","ignore")
            import re
            links=re.findall(r'nuddg=([^&"]+)',html)[:5]
            return ToolResult(True,"\n".join(urllib.parse.unquote(x) for x in links) or "No results found.")
        except Exception as e:return ToolResult(False,f"Search failed: {e}")
    def launch(self,target):
        try: os.startfile(target); return ToolResult(True,f"Launched {target}.")
        except Exception as e:return ToolResult(False,str(e))
    def terminal(self,cmd,approved=False):
        if not approved:return ToolResult(False,"Terminal action requires approval.")
        try:
            p=subprocess.run(cmd,shell=True,capture_output=True,text=True,timeout=30)
            return ToolResult(p.returncode==0,(p.stdout or p.stderr).strip()[:6000])
        except Exception as e:return ToolResult(False,str(e))
