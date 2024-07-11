from customtkinter import *
app = CTk()
app.geometry('300x300')

scfr = CTkScrollableFrame(app, fg_color="#373634", width=500, height=400, corner_radius=20)
scfr.pack()
for i in range(5):
    CTkLabel(master=scfr, text="Message Client", corner_radius=32, height=20, width=500).pack(padx=30,pady=40)
app.mainloop()