from customtkinter import *


class FormFrame(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.name_label = CTkLabel(self, text="Nazwa:")
        self.name_label.pack(padx=5, pady=5)
        self.name_entry = CTkEntry(self)
        self.name_entry.pack(padx=5, pady=5)

        self.price_label = CTkLabel(self, text="Cena:")
        self.price_label.pack(padx=5, pady=5)

        vcmd = self.register(self.validate_price_input)
        self.price_entry = CTkEntry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.price_entry.pack(padx=5, pady=5)

        self.img_path_label = CTkLabel(self, text="")
        self.img_path_label.pack(padx=5, pady=5)

        self.file_button = CTkButton(self, text='Wybierz zdjęcie ')
        self.file_button.pack(pady=10)

        self.add_button = CTkButton(self, text="Dodaj produkt")
        self.add_button.pack(pady=5)

    def set_img_path_label_text(self, new_text):
        self.img_path_label.configure(text=new_text)

    def clear_form(self):
        self.name_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.set_img_path_label_text("")

    @staticmethod
    def validate_price_input(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
