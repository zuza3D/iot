from customtkinter import *

from view.archive_frame import ArchiveFrame
from view.form_frame import FormFrame
from view.auction_frame import AuctionFrame
from view.title_frame import TitleFrame


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Portal aukcyjny")
        self.geometry("1100x600")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.form_title_frame = TitleFrame(self, title_text="Formularz dodawania aukcji")
        self.form_title_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 10), sticky="nsew")
        self.form_frame = FormFrame(self)
        self.form_frame.grid(row=1, column=0, padx=(0, 10), pady=(10, 10), sticky="nsew")

        self.auction_title_frame = TitleFrame(self, title_text="Aktualna oferta")
        self.auction_title_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky="nsew")
        self.auction_frame = AuctionFrame(self, border_width=2, border_color="#1f6aa5")
        self.auction_frame.grid(row=1, column=1, padx=(0, 10), pady=(10, 10), sticky="nsew")

        self.archive_title_frame = TitleFrame(self, title_text="Archiwum aukcji")
        self.archive_title_frame.grid(row=0, column=2, padx=(0, 10), pady=(10, 10), sticky="nsew")
        self.archive_frame = ArchiveFrame(self)
        self.archive_frame.grid(row=1, column=2, padx=(0, 10), pady=(10, 10), sticky="nsew")

    @staticmethod
    def open_file_dialog():
        return filedialog.askopenfilename()
