from customtkinter import *


class TitleFrame(CTkFrame):
    def __init__(self, master, title_text, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title_label = CTkLabel(self, text=title_text, font=("Arial", 22))
        self.title_label.pack(padx=10, pady=10)

    def set_title(self, new_title):
        self.title_label.configure(text=new_title)