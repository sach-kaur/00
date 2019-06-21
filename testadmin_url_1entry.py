import urllib.request
import mysql.connector as my

mydb = my.connect(
    host="localhost",
    user="root",
    password="9876",
    database="crm"
)
mycurs = mydb.cursor()
# get srno from offline database
mycurs.execute("SELECT MAX(sr_no) FROM users")
offmax = mycurs.fetchone()
offmax = int(offmax[0])

urget = "http://www.thearchsms.com/py_fetchadmin.php?a="
a = str(offmax)
urlfetch = urget + a
x = urllib.request.urlopen(urlfetch)
x.getcode()
a = x.read().decode("utf-8")
b = a.split("<br>")
print("b=",b, "\n")
minon = int(b[0])
print("min online", minon)
print("max offline", offmax)

# check srno is same
offmax+=1
if (offmax == minon):
    print("first if")
    templ = []
    for i in range(offmax-1, len(b)):
        print("in if",templ)
        if (b[i] == str(offmax)):
##            offmax += 1
            print("second if")
            if (templ):
                print("third if")
                try:
                    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                    data = (templ[0], templ[1], templ[2])
                    mycurs.execute(query, data)
                    mydb.commit()
                    del templ
                except my.Error as e:
                    if (e):
                        print("error")
            else:
                pass
        else:
            templ.append(b[i])

    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    data = (templ[0], templ[1], templ[2])
    mycurs.execute(query, data)
    mydb.commit()
