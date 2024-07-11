import yaml
from customtkinter import *
from PIL import Image
import Chatstemplate as CT
import actualclient

dit = {}


def homepagecontent():
    global dit
    with open('..\Program files/programvariables.yaml', 'r') as fh:
        dit = yaml.safe_load(fh)

    def returnname():
        global dit
        text = button.cget("text")
        dit['anuser'] = text
        with open('..\Program files/programvariables.yaml', 'w') as fh:
            dit = yaml.dump(dit, fh, default_flow_style=False)
        CT.chats(username=text)

    set_default_color_theme("green")
    app = CTk()
    app.geometry("500x600")
    app.resizable(False, False)
    set_appearance_mode("dark")
    img = Image.open("..\Program files/1.png")
    CTkButton(master=app, text="", fg_color="transparent", hover_color="#000", height=50,
              width=50, image=CTkImage(dark_image=img, light_image=img, size=(50, 50))).pack()
    # the tabs....
    sclfr = CTkScrollableFrame(master=app, fg_color="#2e2d2a", width=500, height=600, corner_radius=20)
    sclfr.pack()
    for i in actualclient.displhm(username=dit["username"]):
        print(i)
        button = CTkButton(master=sclfr, text=i[2] + ":" + i[1], width=500, height=50, command=lambda: returnname())
        # Todo : button must return name of the user when clicked
        button.pack()

    app.mainloop()
