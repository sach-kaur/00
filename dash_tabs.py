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
    filename = ""

    def logout(self):
        destroy()
        os.system("login_tabs.py")

    # send messages functions--------------
    def openfile(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("Text files", "*.txt")))#,("Excel Workbook", "*.xlsx")))
        self.defaultpath.set(filename)

    def sendmsg(self, event):

        numlist = self.numbers.get()
        numbs = numlist.split(",")

        msgtyp = self.x.get()  # get radiobutton

        textmsg = self.msg.get(1.0, END)  # get text message

        seconds = time.time()
        dates = time.ctime(seconds)

        s1 = 'http://weberleads.in/http-api.php?username=hsinfotech&password=hsinfotech&senderid=ARCSMS&route=2&number='
        n = str(numlist)
        s2 = '&message='
        msg = str(textmsg)
        msg = msg.replace(" ", "%20")
        msg = msg.replace("\n", "%7F")
        for conum in numbs:
            ur = s1 + conum + s2 + msg
            x = urllib.request.urlopen(ur)
            x.getcode()
            v = str(x.read())
        if (v != ""):
            messagebox.showinfo("Success", "Congratulations!\nMessage sent successfully.")
        else:
            pass

        # file upload numbers
        global filename
        fileopen = open(filename, "r")
        numsfile = fileopen.read()

        nums = numsfile.split("\n")
        for nos in nums:
            ur2 = s1 + nos + s2 + msg
            x = urllib.request.urlopen(ur2)
            x.getcode()
            a = str(x.read())
        if (a != ""):
            messagebox.showinfo("Success", "Congratulations!\nMessage sent successfully.")
        else:
            pass

        nums.clear()
        fileopen.close()

        linfil = open("login.txt", "r")
        logadname = linfil.read()

        # validations
        if (numlist == "" and msgtyp == "" and textmsg == ""):
            messagebox.showerror("Error", "Fill all fields.")
        elif (numlist == "" or msgtyp == "" or textmsg == ""):
            messagebox.showerror("Error", "Fill all the fields to send message.")
        elif (numlist.isspace() or textmsg.isspace()):
            messagebox.showerror("Error", "No space allowed.\nFill all the fields.")
        else:
            for conum in numbs:
                if (len(conum) == 10 and conum.isdigit() and int(conum[0]) > 5):
                    query = "INSERT INTO transactions (sent_by, sent_to, msg_type, date, message) VALUES (%s, %s, %s, %s, %s)"
                    data = (logadname, conum, msgtyp, dates, msg)
                    mycurs.execute(query, data)
                    mydb.commit()
                    sent=messagebox.showinfo("Success", "Congratulations.\nMessage sent successfully")
                    if sent is not None:
                        self.numlist.delete(0, END)
                        self.textmsg.delete(0, END)
                else:
                    messagebox.showerror("Error", "Enter valid contact numbers.")
        linfil.close()

    # create users-------------------------------------

    def createadmin(self, event):
        admin_name = self.ecadname.get()
        email = self.encadmail.get()
        password = self.ecadpass.get()
        cnf_pass = self.ecadcpass.get()

        address = email
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', address)

        # validations
        if (admin_name == "" and email == "" and password == "" and cnf_pass == ""):
            messagebox.showerror("Error", "Fill fields to register new admin.")
        elif (admin_name == "" or email == "" or password == "" or cnf_pass == ""):
            messagebox.showerror("Error", "Fill all the fields to register new admin.")
        elif (admin_name.isspace() or email.isspace() or password.isspace() or cnf_pass.isspace()):
            messagebox.showerror("Error", "No space allowed.\nFill all the fields to register new admin.")
        elif (len(admin_name) < 2 or admin_name.isdigit()):
            messagebox.showerror("Error", "Username should have minimum 2 ALPHABETS.")
        elif (match == None):
            messagebox.showerror("Error", "Enter valid E-Mail address.")
        elif (len(password) < 8):
            messagebox.showerror("Error", "Password should have minimum 8 characters.")
        elif (password.isdigit() or password.isalpha()):
            messagebox.showerror("Error", "Password should be Alphanumeric.")
        elif (cnf_pass != password):
            messagebox.showerror("Error", "Password and Confirm Password should match.")

        else:
            try:
                #offline d/b
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                data = (admin_name, email, password)
                mycurs.execute(query, data)
                mydb.commit()
                #online d/b
                ur1="http://www.thearchsms.com/py_addadmin.php?a="
                a=admin_name
                ur2="&b="
                b=email
                ur3="&c="
                c=password
                url = ur1+a+ur2+b+ur3+c
                x = urllib.request.urlopen(url)
                x.getcode()
                success = messagebox.showinfo("Success", "Congratulations.\nYou have registered successfully")
                if success is not None:
                    self.ecadname.delete(0, END)
                    self.encadmail.delete(0, END)
                    self.ecadpass.delete(0, END)
                    self.ecadcpass.delete(0, END)
            except my.Error as e:
                if (e):
                    messagebox.showinfo("Unable to register", "Email or Contact already registered.")

    # user transaction details functions---------------

    def search(self, event):
        print("search user")
        self.sh_user = self.ename.get()

    def generate(self, event):
        self.sh_user = self.ename.get()
        self.cu_pack = self.epack.cget("text")
        # l.cget("text")
        print(self.sh_user)
        print(self.cu_pack)

        clfile = open("%s.txt" % self.sh_user, "w")
        clfile.write("%s" % self.cu_pack)
        clfile.close()

    # get names from listbox
    def listitem(self, event):
        items = self.lists.curselection()
        for naam in items:
            print(self.lists.get(naam))

    # generate log file
    def generatelog(self, event):
        pass
        mycurs.execute("SELECT * FROM users")
        res = mycurs.fetchall()
        for dat in res:
            logfile = open("logfile.txt", "a")
            logfile.write("%s\t\t" % dat[1])
            logfile.write("%s\t\t" % dat[2])
            logfile.write("%s\n" % dat[3])

    def __init__(self, master):
        master.title("Dashboard")
        win_width = 815
        win_height = 635
        swidth = master.winfo_screenwidth()
        sheight = master.winfo_screenheight()
        x = int((swidth / 2) - (win_width / 2))
        y = int((sheight / 2) - (win_height / 2))

        master.geometry(f"{win_width}x{win_height}+{x}+{y}")
        master.resizable(0, 0)

        font1 = Font(weight="bold", size=10)  # defining font
        font2 = Font(weight="bold", size=9)

        self.tname=Label(master, text="ARCH SMS", font=('Times', '20', 'bold'),bg="#CDEDF8",fg="navy")
        self.tname.grid(row=0,column=0,columnspan=2, ipady=12,sticky=E+W)

        #logout button
        self.logout = ttk.Button(master, text="Log Out", command=self.logout)
        self.logout.place(x=700,y=20)

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=('Times', '11', 'normal'), padding=(19, 5))
        style.map("TNotebook.Tab", background=[('selected', 'gray94')])

        # tabs------------------------------------

        self.tabs = ttk.Notebook(master)
        self.tabs.grid(row=1, column=0,columnspan=2)

        self.semdmsgframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.semdmsgframe, text="Send Messages to Clients")

        self.usermgtframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.usermgtframe, text="Admin Management")

        self.historyframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.historyframe, text="Log History")

        self.usertranframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.usertranframe, text="Users' Transaction Details")

        self.clientdetsframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.clientdetsframe, text="Clients' Details")

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

        # user management--------------------------------------------------

        self.usermgtcont = Frame(self.usermgtframe, relief="groove", borderwidth=2)
        self.usermgtcont.grid(row=2, column=0, padx=200, pady=110)

        # create admin
        self.cadmin = Label(self.usermgtcont, text="Create New Admins", font=font1, fg="blue")
        self.cadmin.grid(row=3, column=0, pady=20, columnspan=2)

        # fullname
        self.cadname = Label(self.usermgtcont, text="Full Name:", font=font2)
        self.cadname.grid(row=5, column=0, pady=10, padx=20, sticky=E)

        self.ecadname = ttk.Entry(self.usermgtcont, width=30)
        self.ecadname.grid(row=5, column=1, padx=(0, 50), sticky=W)

        # e-mail
        self.cadmail = Label(self.usermgtcont, text="E-Mail:", font=font2)
        self.cadmail.grid(row=7, column=0, pady=10, padx=20, sticky=E)

        self.encadmail = ttk.Entry(self.usermgtcont, width=30)
        self.encadmail.grid(row=7, column=1, padx=(0, 50), sticky=W)

        # password
        self.cadpwd = Label(self.usermgtcont, text="Password:", font=font2)
        self.cadpwd.grid(row=8, column=0, pady=10, padx=20, sticky=E)

        self.ecadpass = ttk.Entry(self.usermgtcont, show="*", width=30)
        self.ecadpass.grid(row=8, column=1, padx=(0, 50), sticky=W)

        # confirm password
        self.cadcpwd = Label(self.usermgtcont, text="Confirm Password:", font=font2)
        self.cadcpwd.grid(row=9, column=0, pady=10, padx=20, sticky=E)

        self.ecadcpass = ttk.Entry(self.usermgtcont, show="*", width=30)
        self.ecadcpass.grid(row=9, column=1, padx=(0, 50), sticky=W)

        self.crbtn = ttk.Button(self.usermgtcont, text="Create User")
        self.crbtn.grid(row=10, column=1, pady=(10, 20), sticky=W)
        self.crbtn.bind("<Button-1>", self.createadmin)

        # log history----------------------------------------
        self.logtext = Frame(self.historyframe, relief="groove", borderwidth=2)
        self.logtext.grid(row=2, column=0, padx=60, pady=50)
        self.historyframe.bind("<Enter>", self.generatelog)

        # scrollbar
        self.scroll = ttk.Scrollbar(self.logtext, orient=VERTICAL)
        self.scroll.grid(row=2, column=1, pady=10, sticky=N + S)

        # log file
        self.history = Text(self.logtext, yscrollcommand=self.scroll.set, width=80, height=25)
        fopen = open("logfile.txt", "r")
        rec = fopen.read()

        self.history.insert(END, rec)
        fopen.close()

        self.history.config(state=DISABLED)
        self.history.grid(row=2, column=0, padx=(10, 0), pady=10)

        self.scroll.config(command=self.history.yview)

        # user transaction details---------------------------------------

        self.usertrancont = Frame(self.usertranframe, relief="groove", borderwidth=2)
        self.usertrancont.grid(row=2, column=0, pady=50, padx=90)

        # name of client
        self.name = Label(self.usertrancont, text="E-Mail:", font=font2)
        self.name.grid(row=2, column=0, pady=(30, 10), padx=10, sticky=E)

        self.ename = ttk.Entry(self.usertrancont, width=30)
        self.ename.grid(row=2, column=1, pady=(30, 10), padx=10)

        # search users
        self.searchbtn = ttk.Button(self.usertrancont, text="Search User")
        self.searchbtn.grid(row=2, column=2, pady=(30, 10))
        self.searchbtn.bind("<Button-1>", self.search)

        # current pack
        self.curt_pack = Label(self.usertrancont, text="Current Pack:", font=font2)
        self.curt_pack.grid(row=3, column=0, pady=10, padx=10, sticky=E)

        self.epack = Label(self.usertrancont, text="pack")
        self.epack.grid(row=3, column=1, pady=10, padx=22, sticky=W)

        # transactional pack btn
        self.tran = ttk.Button(self.usertrancont, text="Transactional Messages")
        self.tran.grid(row=4, column=0, padx=10, pady=20, ipadx=5)

        # promotional pack btn
        self.promo = ttk.Button(self.usertrancont, text="Promotional Messages")
        self.promo.grid(row=4, column=1, padx=10, pady=20, ipadx=8)

        # otp pack btn
        self.otp = ttk.Button(self.usertrancont, text="OTP Messages", state=DISABLED)
        self.otp.grid(row=4, column=2, padx=10, pady=20, ipadx=20)

        # generate file
        self.gen_file = ttk.Button(self.usertrancont, text="Generate User's File")
        self.gen_file.grid(row=5, column=2, padx=10, pady=(0, 20), ipadx=5)
        self.gen_file.bind("<Button-1>", self.generate)

        # labels
        self.usname = Label(self.usertrancont, text="Sent To", font=font2)
        self.usname.grid(row=6, column=0, padx=30, sticky=W)

        self.usdetails = Label(self.usertrancont, text="Message Details", font=font2)
        self.usdetails.grid(row=6, column=1, padx=10, sticky=W)

        # data frame
        self.data = Frame(self.usertrancont)
        self.data.grid(row=7, column=0, columnspan=3, pady=(2, 20))

        # scrollbar
        self.scroll = ttk.Scrollbar(self.data, orient=VERTICAL)
        self.scroll.grid(row=7, column=1, pady=(0, 10), sticky=N + S)

        # listbox
        self.lists = Listbox(self.data, width=25, selectmode=SINGLE, yscrollcommand=self.scroll.set)
        for i in range(1, 50):
            self.lists.insert(END, "num" + str(i))

        self.scroll.config(command=self.lists.yview)

        self.lists.grid(row=7, column=0, padx=(20, 0), pady=(0, 10), sticky=E)
        self.lists.bind("<Button-1>", self.listitem)

        # scrollbar
        self.scroll2 = ttk.Scrollbar(self.data, orient=VERTICAL)
        self.scroll2.grid(row=7, column=3, pady=(0, 10), padx=(0, 20), sticky=N + S)

        # text area
        self.info = Text(self.data, height=10, width=47, yscrollcommand=self.scroll2.set)
        self.info.grid(row=7, column=2, pady=(0, 10))

        self.scroll2.config(command=self.info.yview)

        # client details-------------------------------------

        self.clcont = Frame(self.clientdetsframe, relief="groove", borderwidth=2)
        self.clcont.grid(row=2, column=0, pady=200, padx=200)

        # name of client
        self.name = Label(self.clcont, text="E-Mail:", font=font2)
        self.name.grid(row=2, column=0, pady=(30, 10), padx=10, sticky=E)

        self.ename = ttk.Entry(self.clcont, width=30)
        self.ename.grid(row=2, column=1, pady=(30, 10), padx=10)

        # search users
        self.searchbtn = ttk.Button(self.clcont, text="Search Client Information")
        self.searchbtn.grid(row=2, column=2, pady=(30, 10), padx=20)
        self.searchbtn.bind("<Button-1>", self.search)


win = Tk()
root = dash(win)
win.mainloop()
