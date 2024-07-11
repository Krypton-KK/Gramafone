import time
import yaml
from customtkinter import *
from PIL import Image


def setupcontent():
    dit = {'username': '', 'password': '', 'mode': '', 'anuser': '','Access State':False}
    with open('..\Program files/programvariables.yaml', 'w') as fh:
        dit = yaml.dump(dit, fh, default_flow_style=False)
    # write vAR in dict -- use eval

    passwd = username = mode = ""
    set_default_color_theme("green")
    app = CTk()
    app.resizable(False, False)
    app.geometry("400x600")
    usrnm, pswd = StringVar(value=''), StringVar(value='')

    # never put this in a fn!!!!!!!!!!
    # os.startfile()

    def ntyretrive():
        fh.close()
        global username, passwd
        username = usrnm.get()
        passwd = pswd.get()
        import actualclient
        x = actualclient.checkusr(username)
        if x == "it is Vacant!!":
            w = CTkLabel(master=app, text=x + ' pls wait adding your account ')
            w.pack()
            actualclient.createuser(username, passwd)
            w = CTkLabel(master=app, text='your account is created ("-")')
            w.pack()
            time.sleep(2)
            import homepage
            homepage.homepagecontent()
        else:
            w = CTkLabel(master=app, text=x)
            w.pack()

    img = Image.open(r"..\Program files/Screenshot-removebg-preview.png")
    CTkButton(master=app, text="", corner_radius=32, fg_color="transparent", hover_color="#000", height=200,
              width=200, image=CTkImage(dark_image=img, light_image=img, size=(200, 200))).pack(pady=20, padx=20)
    CTkLabel(master=app, text="Username").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter Username.....", textvariable=usrnm).pack()
    CTkLabel(master=app, text="Password").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter password.....", textvariable=pswd, show="#").pack()
    CTkButton(master=app, text="Check", corner_radius=32, height=20,
              width=15, command=lambda: ntyretrive()).pack(pady=20, padx=20)

    app.mainloop()
    mode = "Message Client"
    dictvar = {'username': username, 'password': passwd, "mode": mode, "anuser": "",'Access State':True}  # add more variables as needed
    with open(r'..\Program files/programvariables.yaml', 'w') as fh:
        dit = yaml.dump(dictvar, fh, default_flow_style=False)

