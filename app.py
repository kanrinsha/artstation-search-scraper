import tkinter as tk
import tkinter.font as tkFont
from configparser import ConfigParser
from scraper import Scraper
import tkinter.messagebox


class App:
    def __init__(self, root):
        self.configur = ConfigParser()
        self.configur.read('config.ini')

        # setting title
        root.title("Artstation Scraper")
        # setting window size
        width=544
        height=186
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_150=tk.Button(root)
        GButton_150["anchor"] = "center"
        GButton_150["bg"] = "#000000"
        ft = tkFont.Font(family='Times',size=10)
        GButton_150["font"] = ft
        GButton_150["fg"] = "#ffffff"
        GButton_150["justify"] = "center"
        GButton_150["text"] = "Scrape"
        GButton_150.place(x=250,y=140,width=70,height=25)
        GButton_150["command"] = self.GButton_150_command

        GMessage_61=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_61["font"] = ft
        GMessage_61["fg"] = "#000000"
        GMessage_61["justify"] = "center"
        GMessage_61["text"] = "Query"
        GMessage_61.place(x=130,y=60,width=67,height=30)

        GMessage_802=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_802["font"] = ft
        GMessage_802["fg"] = "#000000"
        GMessage_802["justify"] = "right"
        GMessage_802["text"] = "Album Name"
        GMessage_802.place(x=120,y=20,width=70,height=40)

        GMessage_734=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_734["font"] = ft
        GMessage_734["fg"] = "#000000"
        GMessage_734["justify"] = "center"
        GMessage_734["text"] = "Amount"
        GMessage_734.place(x=120,y=100,width=90,height=30)

        self.GLineEdit_769=tk.Entry(root)
        self.GLineEdit_769["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_769["font"] = ft
        self.GLineEdit_769["fg"] = "#000000"
        self.GLineEdit_769["justify"] = "center"
        self.GLineEdit_769["text"] = "epic album"
        self.GLineEdit_769.place(x=200,y=20,width=169,height=30)
        self.GLineEdit_769.insert(0, self.configur.get("general", "album_name"))

        self.GLineEdit_980=tk.Entry(root)
        self.GLineEdit_980["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_980["font"] = ft
        self.GLineEdit_980["fg"] = "#000000"
        self.GLineEdit_980["justify"] = "center"
        self.GLineEdit_980["text"] = "monkeys"
        self.GLineEdit_980.place(x=200,y=60,width=169,height=30)

        self.GLineEdit_63=tk.Entry(root)
        self.GLineEdit_63["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_63["font"] = ft
        self.GLineEdit_63["fg"] = "#000000"
        self.GLineEdit_63["justify"] = "center"
        self.GLineEdit_63["text"] = "10"
        self.GLineEdit_63.place(x=250,y=100,width=70,height=25)

    def GButton_150_command(self):
        if self.GLineEdit_63.get() == "":
            tkinter.messagebox.showerror(message="Please input amount")
            return

        if int(self.GLineEdit_63.get()) == 0 or int(self.GLineEdit_63.get()) > 100:
            tkinter.messagebox.showerror(message="Amount cannot be zero or greater than 100")
            return

        if self.GLineEdit_980.get() == "":
            tkinter.messagebox.showerror(message="Query cannot be empty")
            return

        if self.GLineEdit_769.get() == "":
            tkinter.messagebox.showerror(message="Album name cannot be empty")
            return

        print("Commencing scraping!")
        print(self.GLineEdit_980.get())
        print(self.GLineEdit_63.get())

        self.configur.set("general", "album_name", self.GLineEdit_769.get())
        with open('config.ini', 'w') as configfile:  # save
            self.configur.write(configfile)

        scraper = Scraper()
        scraper.download_by_query(query=self.GLineEdit_980.get(), amount=self.GLineEdit_63.get())


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
