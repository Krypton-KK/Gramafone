import yaml
from customtkinter import *
from PIL import Image

# from cnctflNtrfns import *
# import homepage

username = passwd = mode = ""
state = ""
app2 = None


def logincontent():
    global username, passwd, mode
    dit = {'username': '', 'password': '', 'mode': 'Message Client', 'anuser': '', 'Access State': False}
    with open(r'..\Program files/programvariables.yaml', 'w') as fh:
        yaml.dump(dit, fh, default_flow_style=False)
    # write vAR in dict -- use eval

    set_default_color_theme("green")
    app = CTk()
    app.resizable(False, False)
    app.geometry("400x600")
    usrnm, pswd = StringVar(value=''), StringVar(value='')

    def ntyretrive():
        global username, passwd
        username = usrnm.get()
        passwd = pswd.get()
        check(username, passwd)

    def check(usernme, pawd):
        global app2
        app2 = CTk()
        app2.resizable(False, False)
        app2.geometry("400x400")
        print('created app')
        import actualclient
        if actualclient.sessncheck(usernme, pawd):
            CTkLabel(master=app2, text="Access Granted").pack(pady=20, padx=20)
            CTkButton(master=app2, text="continue?", command=lambda: redirecthomepage(), corner_radius=32,
                      fg_color="transparent", hover_color="#000", height=200, width=200).pack(pady=20, padx=20)
            app2.mainloop()

    def redirecthomepage():
        global app2
        app.destroy()
        app2.destroy()
        mode = "Message Client"
        print('inserting the values')
        dictvar = {'username': username, 'password': passwd, "mode": mode, "anuser": "", 'Access State': True}
        # add more variables as needed
        with open(r'..\Program files/programvariables.yaml', 'w') as fh:
            yaml.dump(dictvar, fh, default_flow_style=False)
        import homepage
        homepage.homepagecontent()

    def redirectsetup():
        app.destroy()
        import setupscreen
        setupscreen.setupcontent()

    img = Image.open(r"..\Program files/Screenshot-removebg-preview.png")
    CTkButton(master=app, text="", corner_radius=32, fg_color="transparent", hover_color="#000", height=200,
              width=200, image=CTkImage(dark_image=img, light_image=img, size=(200, 200))).pack(pady=20, padx=20)
    CTkLabel(master=app, text="Username").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter Username.....", textvariable=usrnm).pack()
    CTkLabel(master=app, text="Password").pack(pady=20, padx=20)
    CTkEntry(master=app, placeholder_text="Enter password.....", textvariable=pswd, show="#").pack()
    CTkButton(master=app, text="Check", corner_radius=32, height=20,
              width=15, command=lambda: ntyretrive()).pack(pady=20, padx=20)
    CTkButton(master=app, text="New Here? register now!", corner_radius=32, height=20,
              width=15, command=lambda: redirectsetup()).pack(pady=20, padx=20)
    app.mainloop()


logincontent()
