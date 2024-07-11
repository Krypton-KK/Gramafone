from customtkinter import *
from PIL import Image
import Chatstemplate as CT
import actualclient
# import actualserver
# from cnctflNtrfns import *


def homepagecontent():
    fh = open("Program files/programlevelvariables.txt", "r")
    stng = fh.read()
    fh.close()
    dit = eval(stng)

    def returnname():
        fh = open("Program files/programlevelvariables.txt", "w")
        text = button.cget("text")
        dit['anuser'] = text
        fh.write(dit)
        CT.chats(username=text)

    set_default_color_theme("green")
    app = CTk()
    app.geometry("500x600")
    app.resizable(False, False)
    set_appearance_mode("dark")
    img = Image.open("Program files/1.png")
    CTkButton(master=app, text="", fg_color="transparent", hover_color="#000", height=50,
              width=50, image=CTkImage(dark_image=img, light_image=img, size=(50, 50))).pack()
    # the tabs....
    tabview = CTkTabview(master=app, width=500, height=450, anchor="ew")
    tabview.pack(padx=20, pady=20)
    if dit["mode"] in ("Message Client", "Posts"):
        tabview.add(dit["mode"])
        tabview.set(dit["mode"])
        sclfr = CTkScrollableFrame(master=tabview.tab(dit["mode"]), fg_color="black", width=500, height=400,
                                     corner_radius=20).pack()
    else:  # if dit["mode"] is "All In One":
        tabview.add("Posts")  # add tab at the end
        tabview.add("Message Client")  # add tab at the end
        tabview.set("Message Client")  # set currently visible tab
        sclfrps = CTkScrollableFrame(master=tabview.tab("Posts"), fg_color="black", width=500, height=400,
                                     corner_radius=20).pack()
        sclfr = CTkScrollableFrame(master=tabview.tab("Message Client"), fg_color="black", width=500, height=400,
                                   corner_radius=20).pack()

    if dit["mode"] == "Message Client":
        for i in actualclient.displhm(username=dit["username"]):
            button = CTkButton(master=sclfr, text=i[2] + ":" + i[1], width=500, height=20, command=lambda:returnname())
            # Todo : button must return name of the user when clicked
            button.pack()
    # todo: elif dit['mode'] == "Posts":  # tweet like functionality

    '''else:
        for i in dsplyhm(username=dit["username"]):
            button = CTkButton(master=sclfr, text=i[2] + ":" + i[1], width=500, height=20)
            button.pack()
        # added later'''

    app.mainloop()
