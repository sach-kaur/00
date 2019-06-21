from tkinter import *
from tkinter import ttk
import os


class licence:

    def value(self):  # enabling & disabling NEXT button
        x = self.i.get()
        if (x == 1):
            a = self.nextb.config(state=NORMAL)
            print(a)
        else:
            self.nextb.config(state=DISABLED)

    def create(self):
        fo = open("agreement.txt", "w")
        fo.write("1")
        win.destroy()
        os.system("login_tab.py")

    def cancel(self):
        fill = open("agreement.txt", "w")
        fill.write("0")
        win.destroy()

    def __init__(self, master):
        master.title("License Agreement")

        win_width = 550
        win_height = 400
        swidth = master.winfo_screenwidth()
        sheight = master.winfo_screenheight()
        x = int((swidth / 2) - (win_width / 2))
        y = int((sheight / 2) - (win_height / 2))

        master.geometry("{}x{}+{}+{}".format(win_width, win_height, x, y))
        ##        master.geometry(f"{win_width}x{win_height}+{x}+{y}")
        master.resizable(0, 0)

        # labels
        self.titleframe = Frame(master)
        self.titleframe.grid(column=0, row=0, padx=0)

        self.name = Label(self.titleframe, text="License Agreement")
        self.name.config(font=("Times", 13, "bold"), fg="navy", bg="#CDEDF8")
        self.name.grid(row=0, column=0, ipady=15, ipadx=200)

        # horizontal line
        self.line = Frame(master, height=1, width=win_width, bg="grey")
        self.line.grid(row=1, column=0)

        self.read = Label(master, text="Please read the following License Agreement.")
        self.read.grid(row=2, column=0, padx=25, pady=15, sticky=W)

        # content frame
        self.cont = Frame(master, relief="groove", borderwidth=2)
        self.cont.grid(row=3, column=0, padx=20, pady=10, columnspan=2, sticky=W)

        # scrollbar
        self.scroll = ttk.Scrollbar(self.cont, orient=VERTICAL)
        self.scroll.grid(row=4, column=1, sticky=N + S)

        # license agreement
        self.agreement = Text(self.cont, yscrollcommand=self.scroll.set, width=60, height=10, wrap=WORD)
        # open file
        fileopen = open("images//terms.txt", "r")
        quote = fileopen.read()

        self.agreement.insert(END, quote)
        fileopen.close()

        self.agreement.config(state=DISABLED)
        self.agreement.grid(row=4, column=0, sticky=W)

        self.scroll.config(command=self.agreement.yview)

        # check button
        self.i = IntVar()
        self.accept = Checkbutton(master, variable=self.i, command=self.value)

        self.accept.config(text="I accept the terms and conditions as stated above")
        self.accept.grid(row=4, column=0, padx=25, sticky=W, columnspan=2)

        # horizontal line
        self.line = Frame(master, height=1, width=win_width, bg="grey")
        self.line.grid(row=5, column=0, pady=10)

        # buttons frame
        self.buttons = Frame(master)

        # next button
        self.nextb = ttk.Button(self.buttons, text="Next >>", state=DISABLED, command=self.create)
        self.nextb.grid(row=6, column=0)

        # cancel button
        self.cancel = ttk.Button(self.buttons, text="Cancel", command=self.cancel)
        self.cancel.grid(row=6, column=1, padx=5)

        self.buttons.grid(row=6, column=0, pady=10, columnspan=2, sticky=E)


win = Tk()
root = licence(win)
win.mainloop()
