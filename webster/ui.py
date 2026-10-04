from __future__ import annotations
import tkinter as tk
from .orchestrator import Webster
from .voice import Voice

class App:
    def __init__(self):
        self.bot=Webster(); self.voice=Voice(); self.root=tk.Tk(); self.root.title("WEBSTER"); self.root.geometry("1100x700"); self.root.configure(bg="#09090d")
        self._build(); self._log("WEBSTER","Online. Ready.")
    def _build(self):
        self.left=tk.Frame(self.root,bg="#0d0d14",width=260); self.left.pack(side="left",fill="y")
        self.right=tk.Frame(self.root,bg="#0d0d14",width=260); self.right.pack(side="right",fill="y")
        center=tk.Frame(self.root,bg="#09090d"); center.pack(fill="both",expand=True)
        self.orb=tk.Canvas(center,width=330,height=330,bg="#09090d",highlightthickness=0); self.orb.pack(pady=45)
        for r in range(130,15,-8): self.orb.create_oval(165-r,165-r,165+r,165+r,outline="#d71920",width=2)
        self.orb.create_oval(80,80,250,250,fill="#190b0e",outline="#ff3038",width=5); self.orb.create_text(165,165,text="BINDU",fill="white",font=("Segoe UI",24,"bold"))
        self.input=tk.Entry(center,bg="#15151d",fg="white",insertbackground="white",font=("Segoe UI",14),relief="flat"); self.input.pack(fill="x",padx=35,pady=8); self.input.bind("<Return>",lambda e:self.send())
        bar=tk.Frame(center,bg="#09090d"); bar.pack(); tk.Button(bar,text="SEND",command=self.send,bg="#c9151c",fg="white",relief="flat",padx=20).pack(side="left",padx=5); tk.Button(bar,text="MIC",command=self.mic,bg="#191923",fg="white",relief="flat",padx=20).pack(side="left",padx=5)
        tk.Label(self.left,text="CONVERSATION",bg="#0d0d14",fg="#ff4b52",font=("Segoe UI",11,"bold")).pack(pady=12); self.chat=tk.Text(self.left,bg="#0d0d14",fg="#ddd",width=30,relief="flat",wrap="word"); self.chat.pack(fill="both",expand=True,padx=8,pady=8)
        tk.Label(self.right,text="AI ACTIVITY",bg="#0d0d14",fg="#ff4b52",font=("Segoe UI",11,"bold")).pack(pady=12); self.activity=tk.Text(self.right,bg="#0d0d14",fg="#aaa",width=30,relief="flat",wrap="word"); self.activity.pack(fill="both",expand=True,padx=8,pady=8)
    def _log(self,who,text): self.chat.insert("end",f"{who}: {text}\n\n"); self.chat.see("end")
    def _act(self,text): self.activity.insert("end",text+"\n"); self.activity.see("end")
    def send(self):
        text=self.input.get().strip()
        if not text:return
        self.input.delete(0,"end"); self._log("YOU",text); self._act("Thinking -> routing request"); self.root.update_idletasks(); answer=self.bot.handle(text); self._log("WEBSTER",answer); self._act("Completed -> response delivered")
    def mic(self):
        self._act("Microphone requested"); text=self.voice.listen()
        if text:self.input.delete(0,"end"); self.input.insert(0,text); self.send()
    def run(self): self.root.mainloop()
def run(): App().run()
