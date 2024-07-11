import time
from actualclient import *
from customtkinter import *
from PIL import Image


# from cnctflNtrfns import *


def setupcontent():
    fh = open(r"Program files/programlevelvariables.txt", "w")
    # write vAR in dict -- use eval

    passwd = username = mode = ""
    set_default_color_theme("green")
    app = CTk()
    app.resizable(False, False)
    app.geometry("500x700")
    usrnm, pswd = StringVar(value=''), StringVar(value='')

    # never put this in a fn!!!!!!!!!!
    # os.startfile()

    def ntyretrive():
        global username, passwd
        username = usrnm.get()
        passwd = pswd.get()
        if checkusr(username) == "it is Vacant!!":
            w = CTkLabel(master=app, text=checkusr(username)).pack()
            createuser(username, passwd)
            time.sleep(2)
        else:
            CTkLabel(master=app, text=checkusr(username)).pack()

    img = Image.open("Program files/Screenshot-removebg-preview.png")
    CTkButton(master=app, text="", corner_radius=32, fg_color="transparent", hover_color="#000", height=200,
              width=200, image=CTkImage(dark_image=img, light_image=img, size=(200, 200))).pack(pady=20, padx=20)
    CTkLabel(master=app, text="Username").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter Username.....", textvariable=usrnm).pack()
    CTkLabel(master=app, text="Password").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter password.....", textvariable=pswd, show="#").pack()
    CTkButton(master=app, text="Check", corner_radius=32, height=20,
              width=15, command=lambda: ntyretrive()).pack(pady=20, padx=20)

    app.mainloop()
    if mode == "Choose Mode":
        mode = "Message Client"
    dictvar = {'username': username, 'password': passwd, "mode": mode, "anuser": ""}  # add more variables as needed
    fh.write(str(dictvar))
    fh.close()

setupcontent()