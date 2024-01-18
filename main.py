from customtkinter import *

root = CTk()
root.title("Higher or Lower - Main Menu")
root.geometry("400x700")
root.minsize(600, 400); root.maxsize(600, 400)

_arial = CTkFont(family="Arial", size=25, weight="bold")

def menu(select):
    root.destroy()
    os.system(f"python {select}.py")

def button(t, bt):
    if t: bt.configure(fg_color="#404040")
    else: bt.configure(fg_color="#242424")

start_bt = CTkLabel(root, fg_color="#242424", text="Start", font=_arial)
start_bt.place(anchor="n", relx=0.5, relwidth=1, relheight=1/3)

tutorial_bt = CTkLabel(root, fg_color="#242424", text="Tutorial", font=_arial)
tutorial_bt.place(anchor="center", relx=0.5, rely=0.5, relwidth=1, relheight=1/3)

settings_bt = CTkLabel(root, fg_color="#242424", text="Settings", font=_arial)
settings_bt.place(anchor="s", relx=0.5, rely=1, relwidth=1, relheight=1/3)

start_bt.bind("<Button-1>", lambda event: menu("game"))
start_bt.bind("<Enter>", lambda event, bt=start_bt: button(True, bt))
start_bt.bind("<Leave>", lambda event, bt=start_bt: button(False, bt))

tutorial_bt.bind("<Button-1>", lambda event: menu("tutorial"))
tutorial_bt.bind("<Enter>", lambda event, bt=tutorial_bt: button(True, bt))
tutorial_bt.bind("<Leave>", lambda event, bt=tutorial_bt: button(False, bt))

settings_bt.bind("<Button-1>", lambda event: menu("settings"))
settings_bt.bind("<Enter>", lambda event, bt=settings_bt: button(True, bt))
settings_bt.bind("<Leave>", lambda event, bt=settings_bt: button(False, bt))

root.mainloop()
