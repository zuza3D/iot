from customtkinter import *


class ArchiveFrame(CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.archive_data = []

    def fill_archive_data(self, archive_data):
        self.archive_data = list(archive_data)
        self._refresh_widgets()

    def add_new_archive_data(self, text):
        self.archive_data.insert(0, text)
        self._refresh_widgets()

    def _refresh_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        for data in self.archive_data:
            label = CTkLabel(self, text=data)
            label.pack(padx=5, pady=5)
            