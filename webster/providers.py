from __future__ import annotations
import json, urllib.request
from .config import Config

class Provider:
    def chat(self,messages,system=""):
        raise NotImplementedError

class GeminiProvider(Provider):
    def __init__(self,key,model): self.key,self.model=key,model
    def chat(self,messages,system=""):
        if not self.key: return "Gemini is not configured yet. Add GEMINI_API_KEY to .env."
        parts=[]
        if system: parts.append("SYSTEM:\n"+system)
        parts += [f"{m['role'].upper()}: {m['content']}" for m in messages]
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.key}"
        body=json.dumps({"contents":[{"role":"user","parts":[{"text":"\n\n".join(parts)}]}]}).encode()
        req=urllib.request.Request(url,body,headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=60) as r: data=json.load(r)
        return data["candidates"][0]["content"]["parts"][0]["text"]

class OpenAICompatibleProvider(Provider):
    def __init__(self,key,model,base): self.key,self.model,self.base=key,model,base.rstrip("/")
    def chat(self,messages,system=""):
        msgs=([{"role":"system","content":system}] if system else [])+messages
        body=json.dumps({"model":self.model,"messages":msgs,"temperature":0.3}).encode()
        req=urllib.request.Request(self.base+"/chat/completions",body,headers={"Content-Type":"application/json","Authorization":"Bearer "+self.key},method="POST")
        with urllib.request.urlopen(req,timeout=90) as r:data=json.load(r)
        return data["choices"][0]["message"]["content"]

def build_provider():
    if Config.provider=="gemini": return GeminiProvider(Config.google_key,Config.model)
    if Config.provider=="openrouter": return OpenAICompatibleProvider(Config.openrouter_key,Config.model,"https://openrouter.ai/api/v1")
    if Config.provider in ("openai","compatible"): return OpenAICompatibleProvider(Config.openai_key,Config.model,"https://api.openai.com/v1")
    return GeminiProvider(Config.google_key,Config.model)
