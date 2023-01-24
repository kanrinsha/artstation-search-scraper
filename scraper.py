import tkinter.messagebox
from core import Core


def do_popup(message, title):
    tkinter.messagebox.showinfo(title, message)


class Scraper:
    def __init__(self):
        self.core = Core()

    def download_by_query(self, query, amount):
        self.core.download_data_by_query(query, amount)
        do_popup(message="Scraping Complete!", title="")
