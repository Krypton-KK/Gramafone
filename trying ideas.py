r"""string = b"this=#-94YSSstr"
print(string)
sl = list(str(string))
print(sl)
for i in range(2,len(string)):
    sl[i] = chr(ord(sl[i])+10)
print(sl)
for i in range(2,len(string)):
    sl[i] = chr(ord(sl[i])-10)
print(sl)
print("".join(sl))
"""
# todo:message packets - done....
r'''def pack():
    string = "kk is a good boy"
    n, w = 5, 0
    packet = {}
    if len(string) < 10:
        n = 3
    # packet-ing algorithm - slice every n terms and store in dictionary
    for i in range(0, (len(string) // 5) + 1):
        slic = string[w:w + n]
        w += n
        packet[i] = slic
    return packet
print(pack())'''

# todo:packets to list
r'''dict = {1:10,2:20,3:30}
print(list(dict.items()))'''

# todo:remote connections!! -- done

r'''
Drivername = "SQL SERVER"
Servername = r"192.168.0.109\GRAMAFONE"
Databasename = "Messages"
user = "KK"
paswd = "Kavin"

connectionString = f"""
driver={{{Drivername}}};
driver={Servername};
database={Databasename};
user={user}
password={paswd}
Trust_Connection=yes;
"""

connection = ocn.connect(driver=Drivername,
                         server=Servername,
                         database=Databasename,
                         user=user,
                         password=paswd,
                         Trust_Connection="yes")
print(connection)'''

r'''import customtkinter

app = customtkinter.CTk()
app.geometry("500x500")
tabview = customtkinter.CTkTabview(master=app)
tabview.pack(padx=20, pady=20)

tabview.add("tab 1")  # add tab at the end
tabview.add("tab 2")  # add tab at the end
tabview.set("tab 2")  # set currently visible tab

button = customtkinter.CTkButton(master=tabview.tab("tab 1"))
button.pack(padx=20, pady=20)

app.mainloop()'''

r'''
class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


app = App()
app.mainloop()
'''

r'''[x] = ["50,20,30"]
print(type(x))
lst = list(eval(x))
print(type(eval(x)))
print(type(lst))'''

r"""import cv2
img = cv2.imread(r"Program files/arrow-icon-vector-removebg-preview-modified.png")
img_str = cv2.imencode('.jpg', img)[0].to_bytes()
cv2.imshow("penguins", img)
cv2.waitKey(0)
print(img)
nparr = np.fromstring(img_str, np.frombuffer(img_str))
img2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow("penguins", img2)
cv2.waitKey(0)"""


r'''Drivername = "SQL SERVER"
Servername = r"192.168.0.109\GRAMAFONE"
Databasename1 = "Messages"
Databasename2 = "users"
user = "kk"
paswd = "Kavin"
username ="GRAMAFONEANNOUNCEMENTS"
passwd ='instagramisuseless@2023#'
uscon = ocn.connect(driver=Drivername, server=Servername, database=Databasename2, user=user, password=paswd,
                       Trust_Connection="yes")
msgcon = ocn.connect(driver=Drivername, server=Servername, database=Databasename1, user=user, password=paswd,
                       Trust_Connection="yes")

msgcur = msgcon.cursor()
usid = c.getuid(username=username)
userlist = c.getuslst(username=username)
msgcur.execute('select distinct(touid),DOP from Messages where touid in %s and fruid = %s order by DOP desc'
                   % (userlist, usid))
x = msgcur.fetchall()
if not x:  # new account
    x = []
    x.append(userlist)
print(x)
for i in range(len(x)):
    uscon.cursor().execute("select usnm from usernid where usid=%s" % x[i][0])
    w = uscon.cursor().fetchall()
    x[i] += (w,)
'''

from datetime import datetime
print(datetime.now())
print(type(datetime.strptime(str(datetime.now()),'%Y-%d-%m %H:%M:%S.%f')))
