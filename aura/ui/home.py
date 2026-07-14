import customtkinter as ctk


class Home(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        welcome = ctk.CTkLabel(

            self,

            text="Good Evening, Kshitij",

            font=("Segoe UI", 28, "bold")

        )

        welcome.pack(pady=(80, 15))

        question = ctk.CTkLabel(

            self,

            text="How can I help you today?",

            font=("Segoe UI", 18)

        )

        question.pack()

        microphone = ctk.CTkButton(

            self,

            text="🎤 Speak",

            width=180,

            height=45

        )

        microphone.pack(pady=35)

        textbox = ctk.CTkEntry(

            self,

            width=500,

            placeholder_text="Type a command..."

        )

        textbox.pack()

        history = ctk.CTkTextbox(

            self,

            width=700,

            height=250

        )

        history.pack(pady=40)

        history.insert("0.0", "Welcome to AURA. Your AI Operating System. Speak. Type. Navigate.")
