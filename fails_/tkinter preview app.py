'''
# Import Module
from customtkinter import *
from PIL import Image

# import darkdetect

# colurs!!
logclr = "#00BF63"
homelv = "#9014fa"
dklv = "#734f96"
ltchbl = "#ACC8E5"
fgbl = "#112A46"


# just show last 10 posts for home feed from the server feed....
# -- insta reels mod :)

# def clr():  # picks clour based on dk mode or lt mode
#    if not darkdetect.theme():
#        colr = ltchbl
#    else:
#        colr = dklv
#    return colr


def next(screen):
    screen.destroy()


def loadlogin(prevscreen):
    next(prevscreen)
    login.pack_propagate(False)  # prevent widgets from blanking the screen
    logo = CTkImage(light_image=Image.open("../Program files/Screenshot-removebg-preview.png"), size=(497, 502))
    CTkButton(login, Image=logo)

    # label for instr
    CTkLabel(
        loginframe,
        text="UserName",
        bg_color=logclr,
        fg_color=fgbl
    ).pack(pady=30)
    # entry feild:

    # username = e.get()

    CTkLabel(
        loginframe,
        text="Password",
        bg_color=logclr,
        fg_color=fgbl
    ).pack(pady=30)
    # entry feild:

    # passwd = w.get()

    CTkButton(
        login#frame,
        text="login?",
        bg=dklv,
        fg="white",
        cursor="hand2",
        activebackground=homelv,
        activeforeground=fgbl,
        corner_radius=20,
        #command=lambda: check()
    ).pack(pady=20)

    # return username, passwd


def check():
    # check later!!
    log = True   # todo:checks for passwd
    if log == True:
        login.destroy()
    return


# create root window
login = CTk()
# root window title and dimension
login.title("PROJECT-GRAMAFONE")
# root.eval("tk::PlaceWindow . centre") # --needed to center
# Set geometry (widthxheight)
x = login.winfo_screenwidth() // 2 - 500
y = int(login.winfo_screenheight() * 0.1)
login.geometry('960x540+' + str(x) + '+' + str(y))

# all widgets will be here
#loginframe = CTkFrame(login)
#loginframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nesw")
# homepageframe = CTkFrame(root, bg=homelv)
# chatframe = CTkFrame(root, bg=clr())

# frame in root window!
# for frame in (login,):  # , homepage, chat1
#    frame.grid(row=0, column=0, sticky="nesw")

# Execute CTkinter
login.mainloop()
'''