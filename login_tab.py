from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import webbrowser
import os
##import time
import re
import urllib
import mysql.connector as my
import urllib.request

mydb = my.connect(
    host="localhost",
    user="root",
    password="9876",
    database="crm"
)
mycurs = mydb.cursor()


class logtab():

    def openlink(self, event):
        webbrowser.open_new_tab("http://www.thearchsms.com")

    def registerdata(self, event):
        user_name = self.euname.get()

        email = self.enmail.get()
        password = self.epass.get()
        cnf_pass = self.ecpass.get()
        ##        seconds = time.time()
        ##        dates = time.ctime(seconds)

        address = email
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', address)

        # validations
        if (user_name == "" and email == "" and password == "" and cnf_pass == ""):
            messagebox.showerror("Error", "Fill fields to register.")
        elif (user_name == "" or email == "" or password == "" or cnf_pass == ""):
            messagebox.showerror("Error", "Fill all the fields to register.")
        elif (user_name.isspace() or email.isspace() or password.isspace() or cnf_pass.isspace()):
            messagebox.showerror("Error", "No space allowed.\nFill all the fields to register.")
        elif (len(user_name) < 2 or user_name.isdigit()):
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
##            # get srno from offline database
##            mycurs.execute("SELECT MAX(sr_no) FROM users")
##            offmax=mycurs.fetchone()
##            offmax=int(offmax[0])
##
##            urget="http://www.thearchsms.com/py_fetch.php?a="
##            a=str(offmax)
##            urlfetch=urget+a
##            x = urllib.request.urlopen(urlfetch)
##            x.getcode()
##            a = x.read().decode("utf-8")
##            b=a.split("<br>")
##            minon=int(b[0])
##
##            #check srno is same
##            if(offmax==minon):
##                templ=[]
##                for i in range(offmax,len(b)):
##                    if(b[i]==str(offmax)):
##                        offmax+=1
##                        if(templ):
##                            try:
##                                query="INSERT INTO transactions (sent_by, sent_to, msg_type, date, message) VALUES (%s, %s, %s, %s, %s)"
##                                data=(templ[0],templ[1],templ[2],templ[3])
##                                mycurs.execute(query, data)
##                                mydb.commit()
##                                del templ
##                            except my.Error as e:
##                                if (e):
##                                    pass
##                    else:
##                        templ.append(b[i])
##                
##                query="INSERT INTO transactions (sent_by, sent_to, msg_type, date, message) VALUES (%s, %s, %s, %s, %s)"
##                data=(templ[0],templ[1],templ[2],templ[3],templ[4])
##                mycurs.execute(query, data)
##                mydb.commit()
            try:
                # offline d/b
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                data = (user_name, email, password)
                mycurs.execute(query, data)
                # online d/b
                ur1 = "http://www.thearchsms.com/py_addadmin.php?a="
                a = user_name
                ur2 = "&b="
                b = email
                ur3 = "&c="
                c = password
                url = ur1 + a + ur2 + b + ur3 + c
                x = urllib.request.urlopen(url)
                x.getcode()

                mydb.commit()
                success = messagebox.showinfo("Success", "Congratulations.\nYou have registered successfully")
                if success is not None:
                    self.euname.delete(0, END)
                    self.enmail.delete(0, END)
                    self.epass.delete(0, END)
                    self.ecpass.delete(0, END)
            except my.Error as e:
                if (e):
                    messagebox.showinfo("Unable to register", "Email already registered.")

    def getlogdata(self, event):
        mail = self.euser.get()
        pwd = str(self.elpass.get())

        q = "SELECT * FROM users WHERE email=%s and password=%s"
        d = (mail, pwd)
        mycurs.execute(q, d)
        result = mycurs.fetchone()

        if result is None:
            messagebox.showerror("Error", "Enter valid Email or Password.")
        else:
            if (mail == "" and pwd == ""):
                messagebox.showerror("Error", "Fill fields to Log In.")
            elif (mail == "" or pwd == ""):
                messagebox.showerror("Error", "Fill all the fields to Log In.")
            elif (mail.isspace() or pwd.isspace()):
                messagebox.showerror("Error", "No space allowed.\nFill all the fields to Log In.")
            elif (result):
                foo = open("login.txt", "w")
                foo.write("%s" % result[2])
                foo.close()
                os.system("dash_tabs.py")

    def __init__(self, master):
        master.title("Log In")

        # icon

        win_width = 550
        win_height = 500
        swidth = master.winfo_screenwidth()
        sheight = master.winfo_screenheight()
        x = int((swidth / 2) - (win_width / 2))
        y = int((sheight / 2) - (win_height / 2))

        ##        master.geometry("{}x{}+{}+{}".format(win_width, win_height, x, y))
        master.geometry(f"{win_width}x{win_height}+{x}+{y}")
        master.resizable(0, 0)

        font1 = Font(weight="bold", size=10)  # defining font
        font2 = Font(weight="bold", size=9)

        ttk.Style().configure("TNotebook.Tab", background="azure", font=('Times', '15', 'normal'), padding=(105, 10))

        self.tabs = ttk.Notebook(master)
        self.tabs.grid(row=0, column=1, pady=(5, 0))

        self.regisframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.regisframe, text="Register")

        self.logframe = Frame(self.tabs, bg="white")
        self.tabs.add(self.logframe, text="Log In")

        # register-------------

        # content frame
        self.regcont = Frame(self.regisframe, relief="groove", borderwidth=2)
        self.regcont.grid(row=4, column=0, pady=60, padx=55)

        self.label = Label(self.regcont, text="Please enter the following details to register.", font=font1, fg="blue")
        self.label.grid(row=4, column=0, padx=10, pady=20, columnspan=2, sticky=W)

        # fullname
        self.uname = Label(self.regcont, text="Full Name:", font=font2)
        self.uname.grid(row=5, column=0, pady=10, padx=20, sticky=E)

        self.euname = ttk.Entry(self.regcont, width=30)
        self.euname.grid(row=5, column=1, padx=(0, 20), sticky=W)

        # e-mail
        self.mail = Label(self.regcont, text="E-Mail:", font=font2)
        self.mail.grid(row=7, column=0, pady=10, padx=20, sticky=E)

        self.enmail = ttk.Entry(self.regcont, width=30)
        self.enmail.grid(row=7, column=1, padx=(0, 20), sticky=W)

        # password
        self.pwd = Label(self.regcont, text="Password:", font=font2)
        self.pwd.grid(row=10, column=0, pady=10, padx=30, sticky=E)

        self.epass = ttk.Entry(self.regcont, show="*", width=30)
        self.epass.grid(row=10, column=1, padx=(0, 20), sticky=W)

        # confirm password
        self.cpwd = Label(self.regcont, text="Confirm Password:", font=font2)
        self.cpwd.grid(row=11, column=0, pady=10, padx=30, sticky=E)

        self.ecpass = ttk.Entry(self.regcont, show="*", width=30)
        self.ecpass.grid(row=11, column=1, padx=(0, 30), sticky=W)

        self.labl = ttk.Label(self.regcont, text="By clicking on REGISTER you accept our")
        self.labl.grid(row=12, column=0, padx=(10, 0), pady=(10, 20))

        # link
        self.link = Label(self.regcont, text="Terms and Conditions", fg="red", cursor="hand2")
        self.link.grid(row=12, column=1, pady=(10, 20), sticky=W)
        self.link.bind("<Button-1>", self.openlink)

        # button
        self.regbtn = ttk.Button(self.regcont, text="Register")
        self.regbtn.grid(column=1, row=13, pady=(0, 20), sticky=W)
        self.regbtn.bind("<Button-1>", self.registerdata)

        # login tab------------------------------------

        # content frame
        self.logcont = Frame(self.logframe, relief="groove", borderwidth=2)
        self.logcont.grid(row=2, column=0, pady=120, padx=120)

        self.label = Label(self.logcont, text="Please enter your credentials to login.", font=font1, fg="blue")
        self.label.grid(row=3, column=0, padx=10, pady=20, columnspan=2)

        # username
        self.user = Label(self.logcont, text="Email:", font=font2)
        self.user.grid(row=4, column=0, pady=10, padx=20, sticky=E)

        self.euser = ttk.Entry(self.logcont, width=30)
        self.euser.grid(row=4, column=1, padx=(0, 20), sticky=W)

        # password
        self.pwd = Label(self.logcont, text="Password:", font=font2)
        self.pwd.grid(row=5, column=0, pady=10, padx=20, sticky=E)

        self.elpass = ttk.Entry(self.logcont, show="*", width=30)
        self.elpass.grid(row=5, column=1, padx=(0, 20), sticky=W)

        self.logbtn = ttk.Button(self.logcont, text="Log In")
        self.logbtn.grid(column=1, row=13, padx=20, pady=10, sticky=W)
        self.logbtn.bind("<Button-1>", self.getlogdata)


win = Tk()
root = logtab(win)
win.mainloop()
