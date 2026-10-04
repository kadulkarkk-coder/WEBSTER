from enum import Enum
class Risk(str,Enum): SAFE="safe"; LOW="low"; MEDIUM="medium"; HIGH="high"; BLOCKED="blocked"
class Security:
    def classify(self, name:str)->Risk:
        n=name.lower()
        if any(x in n for x in ("shutdown","delete_all","format_disk","credential","password_dump")): return Risk.HIGH
        if any(x in n for x in ("camera","microphone","send_email","call","message")): return Risk.MEDIUM
        if any(x in n for x in ("shell","terminal","write_file","edit_file")): return Risk.LOW
        return Risk.SAFE
    def approve(self,name:str,callback=None):
        r=self.classify(name)
        if r in (Risk.SAFE,Risk.LOW): return True
        return bool(callback and callback(name,r))
