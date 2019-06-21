from tkinter import *
import os


class agree:

    def __init__(self, master):
        exists = os.path.exists("agreement.txt")

        if (exists):
            fo = open("agreement.txt", "r")
            agree = fo.read()

            if (agree == '1'):
                master.destroy()
                os.system("login_tab.py")
            else:
                master.destroy()
                os.system("license.py")

        else:
            master.destroy()
            os.system("license.py")


win = Tk()
root = agree(win)
win.mainloop()
