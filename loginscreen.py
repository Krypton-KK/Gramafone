from customtkinter import *
from PIL import Image
from actualclient import *

# from cnctflNtrfns import *
# import homepage

username = passwd = mode = ""
state = ""


def logincontent():
    global username, passwd, mode
    fh = open(r"Program files/programlevelvariables.txt", "w")
    # write vAR in dict -- use eval

    set_default_color_theme("green")
    app = CTk()
    app.resizable(False, False)
    app.geometry("500x700")
    usrnm, pswd = StringVar(value=''), StringVar(value='')
    cbvar = StringVar(value="Choose Mode")  # set initial value

    def cbretrive(choice):
        global mode
        print("combobox dropdown clicked:", choice)
        mode = choice

    def ntyretrive():
        global username, passwd
        username = usrnm.get()
        passwd = pswd.get()
        check(username, passwd)

    def check(usernme, pawd):
        app2 = CTk()
        app2.resizable(False, False)
        app2.geometry("50x50")
        sndlt = Image.open("Program files/arrow-icon-vector-removebg-preview.png")
        snddk = Image.open("Program files/arrow-icon-vector-removebg-preview-modified.png")
        if sessncheck(usernme, pawd):
            CTkLabel(master=app, text="Access Granted").pack(pady=20, padx=20)
            CTkButton(master=app, text="", corner_radius=32, fg_color="transparent", hover_color="#000", height=200,
                      width=200, image=CTkImage(dark_image=snddk, light_image=sndlt, size=(200, 200))).pack(pady=20,
                                                                                                        padx=20)
            redirecthomepage()

    def redirecthomepage():
        app.destroy()
        global state
        state = "Access Granted"

    def redirectsetup():
        app.destroy()
        import setupscreen
        setupscreen.setupcontent()

    img = Image.open("Program files/Screenshot-removebg-preview.png")
    CTkButton(master=app, text="", corner_radius=32, fg_color="transparent", hover_color="#000", height=200,
              width=200, image=CTkImage(dark_image=img, light_image=img, size=(200, 200))).pack(pady=20, padx=20)
    CTkLabel(master=app, text="Username").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter Username.....", textvariable=usrnm).pack()
    CTkLabel(master=app, text="Password").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter password.....", textvariable=pswd, show="#").pack()
    CTkComboBox(master=app, values=["Message Client", "Posts", "All In One"], command=cbretrive,
                variable=cbvar).pack(pady=20, padx=20)
    CTkButton(master=app, text="Check", corner_radius=32, height=20,
              width=15, command=lambda: ntyretrive()).pack(pady=20, padx=20)
    CTkButton(master=app, text="New Here? register now!", corner_radius=32, height=20,
              width=15, command=lambda: redirectsetup()).pack(pady=20, padx=20)
    app.mainloop()
    if mode == "Choose Mode":
        mode = "Message Client"
    dictvar = {'username': username, 'password': passwd, "mode": mode, "anuser": ""}  # add more variables as needed
    fh.write(str(dictvar))
    fh.close()
    return "ACCESS GRANTED"

logincontent()