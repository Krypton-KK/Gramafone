from customtkinter import *
from PIL import Image
# import os
from cnctflNtrfns import *
from actualclient import *
import homepage


txtmsg = touid = img = data = None
r'''sndlt = Image.open("../Program files/arrow-icon-vector-removebg-preview.png")
snddk = Image.open("../Program files/arrow-icon-vector-removebg-preview-modified.png")
bkdk = Image.open(r"..\Program files/ziX5zyxxT-1294087685-modified.png")
bklt = Image.open(r"..\Program files/ziX5zyxxT-1294087685.png")'''


def chats(username):
    global fruid, touid, img, data, txtmsg
    with open(r'..\Program files/programvariables.yaml', 'r') as fh:
        dit = yaml.safe_load(fh)
    anuser = dit["anuser"]
    actuser = dit["username"]
    fruid = getuid(username=actuser)
    touid = getuid(username=username)
    # must get from messages----load only last 40, or it will lag, I think so
    app = CTk()  # set_appearance_mode("dark")
    app.geometry("500x620")
    app.resizable(False, False)

    def opnfle():
        root = CTk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.destroy()
        print(file_path)
        send(file_path, "", mode='i')

    def changescene():
        app.destroy()

    def send(filepath, txtmsg, mode='t'):
        print(txtmsg)
        global fruid, touid
        if mode == 't':
            if type(txtmsg) is list:
                for i in txtmsg:
                    sendmsg(i, fruid, touid)
            elif type(txtmsg) is str:
                sendmsg(txtmsg, fruid, touid)
        elif mode == 'i':
            sendfile(filepath, fruid, touid, txtmsg)
        refresh(fruid, touid, txtmsg)

    def display(resultset):
        cnt = 1
        for i in resultset:
            print(i)
            print(cnt)
            frusr = i[1]
            message = msgdecryptor(st2=i[2].encode(), gnkey=eval(i[4]))
            im_pil = None
            if i[3]:
                imgarr = eval(i[3])  # filebytes
                file = open(r'tmp\tmp.png'.rstrip(), "wb")
                file.write(imgarr)
                #  imgcv = cv2.cvtColor(imgarr, cv2.COLOR_BGR2RGB)
                im_pil = Image.open(r'../tmp\tmp.png')
                os.remove(os.getcwd() + r'../tmp\tmp.png')  # delete the file
            if frusr == actuser:
                CTkLabel(scfr, text=(frusr + ":\n" + message), image=CTkImage(light_image=im_pil, dark_image=im_pil),
                         bg_color="#516a22", corner_radius=20).pack(pady=10)
            else:
                CTkLabel(scfr, text=(str(frusr) + ":\n" + str(message)), bg_color="#7ca2b9", corner_radius=20).pack(pady=10)
            cnt += 1

    def refresh(fruid, touid, txtmsg):
        frusr = getusername(fruid)
        message = txtmsg
        print(message)
        if frusr == actuser:
            CTkLabel(scfr, text=(frusr + ":\n" + message), bg_color="#516a22", corner_radius=20).pack(pady=10)
        else:
            CTkLabel(scfr, text=(frusr + ":\n" + message), bg_color="#7ca2b9", corner_radius=20).pack(pady=10)

    # bkpic = CTkImage(dark_image=bkdk, light_image=bklt, size=(20, 20))
    bkbtn = CTkButton(master=app, text="Message Client", corner_radius=32, height=30, width=500,
                      command=lambda: changescene())  # image=bkpic,
    # bkbtn.image = bkpic
    bkbtn.pack()
    CTkLabel(master=app, text="Currently Texting: " + anuser, corner_radius=32, height=40, width=500).pack()
    scfr = CTkScrollableFrame(app, fg_color="#2e2d2a", width=500, height=400, corner_radius=20)
    scfr.pack()
    resultset = collectmsgs(touid, fruid)

    def ntyretrive():
        global data
        lst = []
        ct = 1
        data = enry.get()
        print(data)
        while len(data) > 4294967295:  # using LONGBLOB datatype ~ 4gb
            ct += 1
            ele = data[:4294967295]
            data = data[4294967295:]
            lst.append(ele)
        else:
            if ct > 1:
                CTkLabel(master=scfr, text=f"msg it too large so msg is sent in {ct} parts")
                data = lst
        send(filepath=None, txtmsg=data)

    CTkButton(master=app, text="Select Image", corner_radius=32, height=35, width=500,
              command=lambda: opnfle()).pack()
    enry = CTkEntry(master=app, placeholder_text="message", width=500)
    enry.pack(pady=5)
    # sndpic = CTkImage(dark_image=snddk, light_image=sndlt, size=(20, 20))
    sndbtn = CTkButton(master=app, text="Send Message", corner_radius=32, height=30, width=500, compound="right",
                       command=lambda: ntyretrive())  # image=sndpic,
    # sndbtn.image = sndpic
    sndbtn.pack()
    display(resultset)
    app.mainloop()


# redesign the refresh fn
