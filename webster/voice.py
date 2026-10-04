from __future__ import annotations
class Voice:
    def __init__(self): self.enabled=False; self.engine=None
    def speak(self,text):
        try:
            import pyttsx3
            if self.engine is None:self.engine=pyttsx3.init()
            self.engine.say(text); self.engine.runAndWait(); return True
        except Exception:return False
    def listen(self):
        try:
            import speech_recognition as sr
            r=sr.Recognizer()
            with sr.Microphone() as source: audio=r.listen(source,timeout=5,phrase_time_limit=12)
            return r.recognize_google(audio)
        except Exception:return ""
