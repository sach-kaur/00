from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import filedialog
from tkinter import messagebox
import os
import time
import urllib.request
import mysql.connector as my

mydb = my.connect(
    host="localhost",
    user="root",
    password="9876",
    database="crm"
)
mycurs = mydb.cursor()


class dash():
    def openfile(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("Text files", "*.txt")
                                                         , ("Excel Workbook", "*.xlsx")))
        self.defaultpath.set(filename)

    def sendmsg(self, event):
        linfil = open("login.txt", "r")
        logadname = linfil.read()
        numlist = self.numbers.get()
        numbs = numlist.split(",")
        msgtyp = self.x.get()
        msgtypurl = msgtyp.replace(" ", "%20")
        # get radiobutton
        textmsg = self.msg.get(1.0, END)  # get text message
        seconds = time.time()
        dates = time.ctime(seconds)
        datesurl = dates.replace(" ", "%20")
        msg = str(textmsg)
        msgurl = msg.replace(" ", "%20")
        msgurl=msgurl.replace("\n", "%7F")


        #d/b sync
        # get srno from offline database
        mycurs.execute("SELECT MAX(sno) FROM transactions")
        offmax=mycurs.fetchone()
        offmax=int(offmax[0])

        urget="http://www.thearchsms.com/py_fetch.php?a="
        a=str(offmax)
        urlfetch=urget+a
        x = urllib.request.urlopen(urlfetch)
        x.getcode()
        a = x.read().decode("utf-8")
        b=a.split("<br>")
        minon=int(b[0])

        #check srno is same
        if(offmax==minon):
            templ=[]
            for i in range(offmax,len(b)):
                if(b[i]==str(offmax)):
                    offmax+=1
                    if(templ):
                        try:
                            query="INSERT INTO transactions (sent_by, sent_to, msg_type, date, message) VALUES (%s, %s, %s, %s, %s)"
                            data=(templ[0],templ[1],templ[2],templ[3],templ[4])
                            mycurs.execute(query, data)
                            mydb.commit()
                            del templ
                        except my.Error as e:
                            if (e):
                                pass
                else:
                    templ.append(b[i])
            
            query="INSERT INTO transactions (sent_by, sent_to, msg_type, date, message) VALUES (%s, %s, %s, %s, %s)"
            data=(templ[0],templ[1],templ[2],templ[3],templ[4])
            mycurs.execute(query, data)
            mydb.commit()



        #send msg url
        s1 = 'http://weberleads.in/http-api.php?username=hsinfotech&password=hsinfotech&senderid=ARCSMS&route=2&number='
        s2 = '&message='

        ##        global filename
        ##        print("filename=", filename)
        
        # file
        if (numlist == "" or msgtyp == "" or textmsg == ""):
            messagebox.showerror("Error", "Fill all the fields to send message.")
        elif (numlist.isspace() or textmsg.isspace()):
            messagebox.showerror("Error", "No space allowed.\nFill all the fields.")
        elif (numlist.isalpha()):
            messagebox.showerror("Error", "Enter digits only.")
        else:
            for conum in numbs:
                if (len(conum) == 10 and conum.isdigit() and int(conum[0]) > 5):
                    for conum in numbs:
                        ur = s1 + conum + s2 + msgurl
                        x = urllib.request.urlopen(ur)
                        v = str(x.read())
                        if (v != ""):
                            # offline d/b
                            query = "INSERT INTO transactions (sent_by, sent_to, msg_type, date, message) VALUES (%s, %s, %s, %s, %s)"
                            data = (logadname, conum, msgtyp, dates, msg)
                            mycurs.execute(query, data)
                            mydb.commit()
                            # online d/b

                            ur1 = "http://thearchsms.com/py_sendmsg.php?a="
                            a = logadname
                            ur2 = "&b="
                            b = conum
                            ur3 = "&c="
                            c = msgtypurl
                            ur4 = "&d="
                            d = datesurl
                            ur5 = "&e="
                            e = msgurl
                            url = ur1 + a + ur2 + b + ur3 + c + ur4 + d + ur5 + e
                            z = urllib.request.urlopen(url)
                            messagebox.showinfo("Success", "Congratulations.\nMessage sent successfully")
                        else:
                            messagebox.showerror("Not sent", "Message not sent!!")
                else:
                    messagebox.showerror("Error", "Enter valid contact numbers.")
        linfil.close()

    def __init__(self, master):
        master.title("Dashboard")
        win_width = 815
        win_height = 580
        swidth = master.winfo_screenwidth()
        sheight = master.winfo_screenheight()
        x = int((swidth / 2) - (win_width / 2))
        y = int((sheight / 2) - (win_height / 2))

        master.geometry(f"{win_width}x{win_height}+{x}+{y}")
        master.resizable(0, 0)

        font1 = Font(weight="bold", size=10)  # defining font
        font2 = Font(weight="bold", size=9)

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=('Times', '11', 'normal'), padding=(19, 5))
        style.map("TNotebook.Tab", background=[('selected', 'gray94')])

        # tabs------------------------------------

        self.tabs = ttk.Notebook(master)
        self.tabs.grid(row=0, column=1, pady=(10, 0), padx=2)

        self.semdmsgframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.semdmsgframe, text="Send Messages to Users")

        # send messages--------------------

        self.sendcontent = Frame(self.semdmsgframe, relief="groove", borderwidth=2)
        self.sendcontent.grid(row=2, column=0, pady=90, padx=90)

        # numbers
        self.num = Label(self.sendcontent, text="+91", font=font2)
        self.num.grid(row=2, column=0, pady=30, padx=(20, 0), sticky=W)

        self.numbers = ttk.Entry(self.sendcontent, width=45)
        self.numbers.grid(row=2, column=0, pady=30, padx=(20, 0), columnspan=2)

        # path entry
        self.defaultpath = StringVar()
        self.defaultpath.set("DEFINE PATH")

        self.path = ttk.Entry(self.sendcontent, width=40, textvariable=self.defaultpath)
        self.path.grid(row=2, column=2, pady=30, padx=20)

        # Browse button
        self.browse = ttk.Button(self.sendcontent, text="Upload File",
                                 command=self.openfile)  # function call without lambda function
        self.browse.grid(row=3, column=2, padx=20, sticky=N + W)

        self.typ = Label(self.sendcontent, text="Type message here.", font=font2)
        self.typ.grid(row=4, column=0, pady=(30, 0), padx=20, sticky=W)

        # message box
        self.msg = Text(self.sendcontent, height=10, width=40, wrap=WORD)
        self.msg.grid(row=5, column=0, pady=(5, 20), padx=(20, 10), columnspan=2, rowspan=2, sticky=W)

        # radio buttons
        self.x = StringVar()

        self.trmsg = Radiobutton(self.sendcontent, value="Transactional Message", variable=self.x)
        self.trmsg.config(text="Transactional Messages")
        self.trmsg.grid(row=5, column=2, padx=10)
        self.trmsg.select()

        self.promsg = Radiobutton(self.sendcontent, value="Promotional Message", variable=self.x)
        self.promsg.config(text="Promotional Messages")
        self.promsg.grid(row=5, column=2, sticky=S)

        # send btn
        self.send = ttk.Button(self.sendcontent, text="SEND")
        self.send.grid(row=6, column=2, padx=10)
        self.send.bind("<ButtonPress-1>", self.sendmsg)


win = Tk()
root = dash(win)
win.mainloop()
